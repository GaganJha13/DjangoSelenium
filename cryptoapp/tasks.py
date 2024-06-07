from celery import shared_task, group
from .coinmarketcap import CoinMarketCapScraper

@shared_task
def scrape_coin(coin_name):
    scraper = CoinMarketCapScraper()
    try:
        data = scraper.scrape_coin_data(coin_name)
        return { "coin": coin_name, "output": data }
    except Exception as e:
        return { "coin": coin_name, "error": str(e) }
    finally:
        scraper.close()
