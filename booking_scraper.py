__author__ = "Sanjeev Kumar"
__email__ = "sanjeev.k@srijan.net"
__copyright__ = "Copyright 2019, Srijan Technologies Pvt. Ltd."

from base_scraper import BaseScraper


class BookingScraper(BaseScraper):

    __resource_name__ = 'BOOKING'

    def __init__(self, url=None):
        super(BookingScraper, self).__init__(url)
        self.soup_obj = self.get_parse_data()

    def get_hotel_name(self) -> str:
        """
        Function get_hotel_name
        This function is used to find hotel name from soup object.

        :return:
          Return a hotel name string.
        """

        return ' '.join(
            [h2.text.strip().replace('Hotel\n', '').lower()
             for div in
             self.soup_obj.find_all("div", {"class": "hp__hotel-title"})
             for h2 in div.find_all('h2', id="hp_hotel_name")]
        )

    def get_hotel_amenities(self) -> list:
        """
        Function get_hotel_amenities
        This function is used to get hotel amenities from soup object.

        :return:
          Returns list of hotel amenities.
        """

        return ','.join([
            li.text.strip().replace('\n', '').replace('Additional charge', '').lower()
            for div in
            self.soup_obj.find_all("div", {"class": "facilitiesChecklist"})
            for ul in div.find_all("ul") for li in ul.find_all("li")
        ])

    def get_hotel_description(self) -> str:
        """
        Function get_hotel_description
        This function is used to find hotel description from soup object.

        :return:
          Return a hotel description string.
        """

        return ' '.join(
            [p.text.strip().lower()
             for div in
             self.soup_obj.find_all("div", id="property_description_content")
             for p in div.find_all("p")
             ]
        )

    def get_room_amenities(self) -> list:
        """
        Function get_room_amenities
        This function is used to get hotel room amenities from soup object.

        :return:
          Returns list of hotel room amenities.
        """

        return ','.join([
                   li.text.strip().replace('\n', '').replace(
                       'Additional charge', '').lower()
                   for div in
                   self.soup_obj.find_all("div", {"data-section-id": 6})
                   for ul in div.find_all("ul") for li in ul.find_all("li")
               ] + [
                   li.text.strip().replace('\n', '').replace(
                       'Additional charge', '').lower()
                   for div in
                   self.soup_obj.find_all("div", {"data-section-id": 26})
                   for ul in div.find_all("ul") for li in ul.find_all("li")
               ])

    def get_hotel_data(self) -> dict:
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
