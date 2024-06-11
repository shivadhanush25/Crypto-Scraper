from celery import shared_task
from .models import Job, Task
from .coinmarketcap import CoinMarketCap

@shared_task
def scrape_coin_data(job_id, coin):
    job = Job.objects.get(id=job_id)
    task = job.tasks.get(coin=coin)
    task.status = 'in_progress'
    task.save()

    scraper = CoinMarketCap()
    result = scraper.fetch_coin_data(coin)
    scraper.close()

    task.result = result
    task.status = 'completed' if 'error' not in result else 'failed'
    task.save()
