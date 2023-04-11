import requests
from selectorlib import Extractor


class Temperature:
    yml_path = 'temperature.yaml'

    def __init__(self, city, country):
        self.country = country.replace(' ', '-').lower()
        self.city = city.replace(' ', '-').lower()

    def _build_url(self):
        url = f'https://www.timeanddate.com/weather/{self.country}/{self.city}'
        return url

    def _scrape(self):
        url = self._build_url()

        full_req = requests.get(url).text
        extractor = Extractor.from_yaml_file('temperature.yaml')

        raw_content = extractor.extract(full_req)

        return raw_content

    def get(self):
        scraped_content = self._scrape()
        return float(scraped_content['temp'].replace('°C', '').strip())
