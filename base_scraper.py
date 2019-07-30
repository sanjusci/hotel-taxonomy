__author__ = "Sanjeev Kumar"
__email__ = "sanjeev.k@srijan.net"
__copyright__ = "Copyright 2019, Srijan Technologies Pvt. Ltd."

import requests
from bs4 import BeautifulSoup


class BaseScraper(object):

    __resource_name__ = 'BASE_SCRAPER'

    def __init__(self, url=None):
        self.url = url
        self.page_content = None
        self._session = self.__session__()

    def __session__(self)-> object:
        """
        Function __session__
        This function is used to start request session.

        :return:
          Returns session object.
        """

        with requests.Session() as session:
            session.headers = {
                'accept': 'text/html,application/xhtml+xml,'
                          'application/xml;q=0.9,'
                          'image/webp,'
                          'image/apng,'
                          '*/*;q=0.8,'
                          'application/signed-exchange;'
                          'v=b3',
                'accept-language': 'en-US,en;q=0.9,hi;q=0.8',
                'cache-control': 'no-cache, private',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X '
                              '10_13_4) AppleWebKit/537.36 (KHTML, '
                              'like Gecko) Chrome/74.0.3729.169 '
                              'Safari/537.36',
            }
            return session

    def __parse__(self, features)-> object:
        """
        Function __parse__
        This function is used to get content from given url and generate
        soup object.

        :param features: Desirable features of the parser to be used. This
            may be the name of a specific parser ("lxml", "lxml-xml",
            "html.parser", or "html5lib") or it may be the type of markup
            to be used ("html", "html5", "xml").

        :return:
          Returns beautiful soup object.
        """
        try:
            self.page_content = self._session.get(self.url)
        except Exception as e:
            print(str(e))
        else:
            soup_obj = BeautifulSoup(self.page_content.content, features)
        return soup_obj

    def get_parse_data(self, features='lxml')-> object:
        """
        Function get_parse_data
        This function is used to get parse data object.

        :param features:
          This may be the name of a specific parser ("lxml", "lxml-xml",
            "html.parser", or "html5lib")

        :return:
          Returns parse data object.
        """
        return self.__parse__(features)
