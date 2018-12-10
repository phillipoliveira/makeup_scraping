import requests
from bs4 import BeautifulSoup
from random_useragent.random_useragent import Randomize


class WebFunctions(object):

    @staticmethod
    def get_session():
        session = requests.session()
        headers = {
            "Connection": "close",
            "Accept-Language": "en,fr;q=0.9,en-US;q=0.8,fr-CA;q=0.7",
            "Cookie": "check=true; site_language=en; current_country=US;",
            "User-Agent": Randomize().random_agent('desktop', 'mac')}
        session.headers = headers
        # session.proxies = {'http': 'http://198.15.118.141:22222'}
        return session

    @staticmethod
    def make_soup(url, session):
        request = session.get(url)
        page_content = request.content
        soup = BeautifulSoup(page_content, "html.parser")
        return soup