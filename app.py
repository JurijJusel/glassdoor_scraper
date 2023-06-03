from bs4 import BeautifulSoup
import requests
import time
from urls import urls
from utils.file import create_json
from constants import headers, fuel_types
from get_company_url import get_url_by_name

class FuelCrawler:
    def __init__(self, url, headers):
        self.url = url
        self.headers = headers
        

    def download_response(self):
        req = requests.get(self.url, self.headers).text
        soup = BeautifulSoup(req, features="lxml")
        return soup


    def circlek_prices(self, soup):
        title = soup.title.string[-8::]
        cards = soup.find_all('div', {'class': 'atom-card'})
        updated_fuel_info = cards[0].text[139:160]
        price_miles_95 = cards[0].text[43:48]
        price_miles_plus_95 = cards[1].text[43:48]
        price_miles_plus_98 = cards[2].text[43:48]
        price_miles_D = cards[3].text[43:48]
        price_miles_D_plus = cards[4].text[43:48]
        price_dz = cards[5].text[43:48]
        price_lpg = cards[6].text[43:48]
        price_ad_blue = cards[7].text[43:48]

        time_now = time.strftime("%Y-%m-%d %H:%M:%S")
        
        self.circlek_data = {
            'company': title,
            'scrap_time': time_now,
            'updated_fuel_info': updated_fuel_info, 
            'miles_95': price_miles_95, 
            'miles_plus_95': price_miles_plus_95,
            'miles_plus_98': price_miles_plus_98,
            'miles_D': price_miles_D,
            'miles_D_plus': price_miles_D_plus,
            'DZ': price_dz,
            'lpg': price_lpg,
            'ad_blue': price_ad_blue
            }
        
        return self.circlek_data


    def get_prices(self):
        soup_response = self.download_response()
        return self.circlek_prices(soup_response)
        
       
    def print_data(self):
        self.get_prices()
        updated_fuel_info = self.circlek_data['updated_fuel_info']
        company = self.circlek_data['company']
        for fuel_type in fuel_types:
            fuel_value = self.circlek_data[fuel_type]
            print(f"{updated_fuel_info}:  {company}  {fuel_type} - {fuel_value}")
      

if __name__ == '__main__':
    station = FuelCrawler(get_url_by_name('Circle'), headers)
    station.print_data()

