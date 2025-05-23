import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from config import logging
from tasks.mailing import mailing_tick
from tasks.giveaways import giveaway_results_tick

logger = logging.getLogger(__name__)

async def run_scheduler():
    logger.info("Scheduler started")

    scheduler = AsyncIOScheduler(job_defaults={'coalesce': False, 'max_instances': 3})
    
    scheduler.add_job(mailing_tick, 'interval', seconds=1, id="mailing-tick")
    # scheduler.add_job(giveaway_results_tick, 'interval', seconds=15, id="results-tick")
    
    scheduler.start()

    try:
        await asyncio.Event().wait()  # держит цикл вечно
    except (KeyboardInterrupt, SystemExit):
        logger.warning("Scheduler stopped manually.")

if __name__ == '__main__':
    asyncio.run(run_scheduler())
