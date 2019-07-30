__author__ = "Sanjeev Kumar"
__email__ = "sanjeev.k@srijan.net"
__copyright__ = "Copyright 2019, Srijan Technologies Pvt. Ltd."

import pandas as pd
from booking_scraper import BookingScraper
from expedia_scraper import ExpediaScraper
from hotel_scraper import HotalScraper
from settings import ROI_BOOKING, ROI_HOTEL, ROI_EXPEDIA

MODEL_MAPPING = {
    ExpediaScraper: ROI_EXPEDIA,
    HotalScraper: ROI_HOTEL,
    BookingScraper: ROI_BOOKING
}

if __name__ == '__main__':

    data_list = []
    for k, v in MODEL_MAPPING.items():
        print("Start scraping from " + str(k.__resource_name__))
        for url in v:
            exp_obj = k(url)
            data_list.append(exp_obj.get_hotel_data())
        print("Complete scraping from " + str(k.__resource_name__))

    df = pd.DataFrame(data_list)
    df.rename(index=str, columns={
        'hotel_name': 'HOTEL NAME',
        'hotel_amenities': 'HOTEL AMENITIES',
        'hotel_description': 'HOTEL DESCRIPTION',
        'room_amenities': 'ROOM AMENITIES'}, inplace=True)
    df.to_csv('hotel.csv')



