                
1. High-level diagram of current architecture

                         ┌─────────────────────┐
                         │        User         │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │     FastAPI API     │
                         │      app/api.py     │
                         └──────────┬──────────┘
                                    │
                    ┌───────────────┼────────────────┐
                    │               │                │
                    ▼               ▼                ▼
             ┌────────────┐  ┌──────────────┐ ┌──────────────┐
             │    RAG     │  │ Coordinator  │ │ Autonomous   │
             │ Endpoint   │  │    Agent     │ │ Research     │
             └─────┬──────┘  └──────┬───────┘ │ Agent        │
                   │                │         └──────┬───────┘
                   │                │                │
                   │          ┌─────▼─────┐          ▼
                   │          │ Planner / │   ┌──────────────┐
                   │          │ Executor  │   │ Research     │
                   │          └─────┬─────┘   │ Planner      │
                   │                │         └──────┬───────┘
                   │                ▼                │
                   │          ┌───────────┐          ▼
                   │          │   Tools   │   ┌──────────────┐
                   │          └─────┬─────┘   │ RAG Retrieval│
                   │                │         └──────┬───────┘
                   └────────────────┼────────────────┘
                                    ▼
                         ┌─────────────────────┐
                         │   Vector Retrieval  │
                         │ SentenceTransformer │
                         │ + vector_db.json    │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   Retrieved Context │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │ Evidence Synthesizer│
                         │      Local LLM      │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │ Evidence Evaluator  │
                         └──────────┬──────────┘
                                    │
                           Enough evidence?
                              │           │
                             No          Yes
                              │           │
                              ▼           ▼
                        More research   Research
                                       Reporter
                                          │
                                          ▼
                                  ┌──────────────┐
                                  │ API Response │
                                  └──────────────┘


Cross cutting systems supporting the workflow

Configuration ─────► .env + app/config.py

Logging ───────────► logs/agent.log

Memory ────────────► conversation + long-term + failure memory

Evaluation ────────► reflection + critic + evaluation history

Containerization ──► Dockerfile

2. Purpose of each major folder
----------------------------------------------------------------------------------------------------------------------------- |
| `app/`        | Application entry layer. Contains FastAPI, API schemas, configuration and logging setup.                                      |
| `agents/`     | AI agent implementations such as autonomous research, research planning, evidence synthesis, critic and collaboration agents. |
| `core/`       | Core orchestration infrastructure such as coordinator, executor, router, task manager and tool registry.                      |
| `planning/`   | Planning logic including advanced planning, goal decomposition, dynamic planning and recursive task generation.               |
| `rag/`        | Retrieval-Augmented Generation infrastructure: ingestion, embeddings, semantic search, vector retrieval and RAG interface.    |
| `memory/`     | Agent memory systems including conversation memory, long-term memory and failure memory.                                      |
| `evaluation/` | Quality-control layer: reflection, evidence evaluation, critic logic, evaluation scoring and evaluation history.              |
| `tools/`      | Individual callable capabilities such as GitHub repository analysis, summarization and prompt optimization.                   |
| `data/`       | Persistent application data such as documents, vector database, evaluations and memory files.                                 |
| `logs/`       | Runtime logs for requests, agent execution, errors and autonomous research activity.                                          |
| `tests/`      | Import tests, smoke tests, collaboration tests and autonomous research tests.                                                 |

Seperation of concerns:

agents/ knows how agents behave.

rag/ knows how information is retrieved.

memory/ knows how information is remembered.

evaluation/ knows how results are judged.

app/ knows how users access the system.

3. Research Request Flow

Example:
POST /research/full

{
    "query": "NumPy"
}

STAGE 1 - API
FAST API recieves 
POST /research/full
in
app/api.py
it calls:
run_autonomous_research("NumPy")

STAGE 2 - Autonomous research
Control moves to:
agents/autonomous_research_agent.py
A new:
ResearchState begins and stores the following:
* goal
* questions
* evidence
* iterations
* completion state

Conceptually:
Goal = NumPy

Evidence = []

Iteration = 0

STAGE 3 - Research Planning
Agent asks:
agents/research_planner.py

To decide: Why should I investigate?

Local LLM may generate questions such as:
What are NumPy's core data structures?

How do NumPy vectorized operations improve performance?

STAGE 4 - RAG Retrieval
Each question goes through:
rag/rag.py which calls rag/vector_store.py

The query is converted into am embedding using:
all-MiniLM-L6-v2
 
and the compared with the embedding stored in:
data/vector_db.json

Suppose the query is:
Why are NumPy arrays faster than Python lists?

Semantic search might retreive:
Score: 0.81
Source: numpy.txt

NumPy arrays differ from Python lists because...

STAGE 5 - Evidence Synthesis
The raw chunks are passed to:
agents/evidence_synthesizer.py

Instead of exposing several raw chunks directly. The local LLM synthesizer may look something like:

NumPy arrays are faster and more memory-efficient than
Python lists because NumPy uses optimized low-level code
and vectorized operations.

So we have:
Raw retrieval
      ↓
Evidence synthesis
      ↓
Readable evidence

STAGE 6 - Evidence Evaluation
Evidence goes to: evaluation/evidence_evaluator.py which asks: Do we have enough valid evidence?

For example:
Valid evidence: 2

Confidence: 70%

Decision:
Continue research.

The agent loops:
Planner
   ↓
RAG
   ↓
Synthesis
   ↓
Evaluation
   ↓
More research

Until eventually:
Valid evidence: 4

Confidence: 85%

Decision:
Research complete.

STAGE 7 - Report generation
Evidence is passed to: agents/research_reporter.py which generates the final:

AUTONOMOUS RESEARCH REPORT

Goal

Summary

Evidence Collected

Confidence

Recommendation

STAGE 8 - API Response
The report returns through FAST API
Research Agent
      ↓
app/api.py
      ↓
JSON Response
      ↓
User

The complete request path therefore becomes:

Client
  ↓
FastAPI
  ↓
Autonomous Research Agent
  ↓
Research Planner
  ↓
RAG
  ↓
Vector Search
  ↓
Retrieved Context
  ↓
Evidence Synthesizer
  ↓
Evidence Evaluator
  ↓
        ┌── Insufficient ──► Research again
        │
        └── Sufficient
               ↓
        Research Reporter
               ↓
          API Response
               ↓
              User

4. THREE INDEPENDENT FUTURE SERVICES
A. Retrieval / Knowlegde services
Today, the following are inside the main application:
rag/
data/documents/
data/vector_db.json

In the future:
                Knowledge Service
                       │
         ┌─────────────┼──────────────┐
         ▼             ▼              ▼
   Document       Embedding      Vector Search
   Ingestion       Service
                       │
                       ▼
               Vector Database

API Examples below:
POST /documents

POST /search

POST /reindex

The seperate is important because at some point, different applications can easiy share the same resources in the retrieval infrastructure, for example:

Marketing Agent ─────┐
Customer Service ────┼──► Knowledge Service
Research Agent ──────┘

B. Agent Orchestration Services

Move agent/ planning/ core/ into an independent orchestration service.

Architecture:

API
 ↓
Agent Orchestrator
 │
 ├── Planner
 ├── Research Agent
 ├── Tool Selector
 ├── Executor
 ├── Critic
 └── Reflection


C. Long-Running Research Worker
Most probably the first service to seperate in production
Currently:

User
 ↓
POST /research/full
 ↓
Research Agent
 ↓
20–60 seconds
 ↓
Response

Better Architecture
User
 ↓
POST /research
 ↓
API
 ↓
Job Queue
 ↓
Return Job ID immediately

      ┌────────────────────────┐
      │ Background Worker      │
      │                        │
      │ Research Planner       │
      │       ↓                │
      │ RAG                    │
      │       ↓                │
      │ Evidence Synthesis     │
      │       ↓                │
      │ Report Generation      │
      └───────────┬────────────┘
                  ↓
             Results Store

User recieves: 
{
  "job_id": "research_10294",
  "status": "processing"
}

and later requests:

GET /research/research_10294 to receive the completed request.

THE FUTURE ARCHITECTURE

                         USERS
                           │
                           ▼
                     API Gateway
                           │
             ┌─────────────┼─────────────┐
             │             │             │
             ▼             ▼             ▼
         RAG API       Agent API    Research API
             │             │             │
             ▼             ▼             ▼
       Knowledge       Agent        Job Queue
        Service      Orchestrator        │
             │             │             ▼
             │             │       Research Worker
             │             │             │
             └─────────────┼─────────────┘
                           │
                   ┌───────┴────────┐
                   ▼                ▼
              Vector DB          LLM Service


The important thing is that we've structured the code so that these pieces can later be separated rather than needing to rewrite the entire system.

