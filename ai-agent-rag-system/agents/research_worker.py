from agents.autonomous_research_agent import (
    run_autonomous_research
)
from core.job_store import update_job
from app.logging_config import logger


def process_research_job(job_id, query):
    try:
        logger.info(
            "Research job started | job_id=%s | query=%s",
            job_id,
            query
        )

        update_job(
            job_id,
            status="running"
        )

        result = run_autonomous_research(query)

        update_job(
            job_id,
            status="completed",
            result=result
        )

        logger.info(
            "Research job completed | job_id=%s",
            job_id
        )

    except Exception as error:
        logger.exception(
            "Research job failed | job_id=%s",
            job_id
        )

        update_job(
            job_id,
            status="failed",
            error=str(error)
        )