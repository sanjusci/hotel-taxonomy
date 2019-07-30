__author__ = "Sanjeev Kumar"
__email__ = "sanjeev.k@srijan.net"
__copyright__ = "Copyright 2019, Srijan Technologies Pvt. Ltd."

from base_scraper import BaseScraper


class HotalScraper(BaseScraper):

    __resource_name__ = 'HOTEL'

    def __init__(self, url=None):
        super(HotalScraper, self).__init__(url)
        self.soup_obj = self.get_parse_data()

    def get_hotel_name(self)-> str:
        """
        Function get_hotel_name
        This function is used to find hotel name from soup object.

        :return:
          Return a hotel name string.
        """
        return ' '.join(
            [h1.text.strip().lower()
             for div in self.soup_obj.find_all("div", {"class": "vcard"})
             for h1 in div.find_all('h1')]
        )

    def get_hotel_amenities(self)-> list:
        """
        Function get_hotel_amenities
        This function is used to get hotel amenities from soup object.

        :return:
          Returns list of hotel amenities.
        """
        return ','.join([
            li.text.strip().lower()
            for div in self.soup_obj.find("div", {
                'class': "in-the-property-module"}).find_all("div", {
                'class': "fact-sheet-table-cell"})
            for ul in div.find_all("ul") for li in ul.find_all("li")
        ])

    def get_hotel_description(self)-> str:
        """
        Function get_hotel_description
        This function is used to find hotel description from soup object.

        :return:
          Return a hotel description string.
        """

        return ' '.join(
            [p.text.strip().lower()
             for div in
             self.soup_obj.find("div", id="special-features").find_all("div", {
                 "class": "info-box"})
             for p in div.find_all("p")
             ]
        )

    def get_room_amenities(self)-> list:
        """
        Function get_room_amenities
        This function is used to get hotel room amenities from soup object.

        :return:
          Returns list of hotel room amenities.
        """

        return ','.join([
            li.text.strip().lower()
            for div in
            self.soup_obj.find("div", {'class': "in-the-room-module"}).find_all(
                "div", {'class': "fact-sheet-table-cell"})
            for ul in div.find_all("ul") for li in ul.find_all('li')
        ])

    def get_hotel_data(self)-> dict:
        """
        Function get_hotel_data
        This function is used to get hotel data.

        :return:
          Returns hotel data dictionary.
        """
        return dict(
            hotel_name=self.get_hotel_name(),
            hotel_amenities=self.get_hotel_amenities(),
            hotel_description=self.get_hotel_description(),
            room_amenities=self.get_room_amenities()
        )
