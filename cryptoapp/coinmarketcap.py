import json
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

class CoinMarketCapScraper:
    BASE_URL = "https://coinmarketcap.com/currencies/"

    def __init__(self):
        options = Options()
        options.headless = True
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    def scrape_coin_data(self, coin_name):
        url = f"{self.BASE_URL}{coin_name.lower()}/"
        self.driver.get(url)

        price = self._extract_price()

        data = {
            "price": price,
        }

        return json.dumps(data)  # Convert data dictionary to JSON format

    def _extract_price(self):
        try:
            price_element = self.driver.find_element(By.XPATH, '//*[@id="section-coin-overview"]/div[2]/span')
            price = price_element.text
            return price
        except Exception as e:
            print(f"An error occurred while extracting the price: {e}")
            return None

    def close(self):
        self.driver.quit()

if __name__ == "__main__":
    scraper = CoinMarketCapScraper()
    coin_name = "bitcoin"
    try:
        data = scraper.scrape_coin_data(coin_name)
        print(f"Scraped data for {coin_name}: {data}")
    finally:
        scraper.close()
