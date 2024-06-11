import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

class CoinMarketCap:
    BASE_URL = 'https://coinmarketcap.com/currencies/'

    def __init__(self):
        options = Options()
        options.headless = True
        self.driver = webdriver.Chrome(service=Service('/path/to/chromedriver'), options=options)

    def fetch_coin_data(self, coin):
        url = f'{self.BASE_URL}{coin}/'
        self.driver.get(url)
        time.sleep(5)  # wait for the page to load
        
        # Scrape the necessary data
        data = {}
        try:
            data['price'] = self.driver.find_element(By.CSS_SELECTOR, 'div.priceValue').text
            data['market_cap'] = self.driver.find_element(By.CSS_SELECTOR, 'div.statsValue').text
            # Add more scraping logic as needed
        except Exception as e:
            data['error'] = str(e)
        
        return data

    def close(self):
        self.driver.quit()
