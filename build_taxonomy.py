
__author__ = "Sanjeev Kumar"
__email__ = "sanjeev.k@srijan.net"
__copyright__ = "Copyright 2019, Srijan Technologies Pvt. Ltd."

import re
import pandas as pd
import spacy
from enum import Enum
from settings import UK_US_COMPREHENSIVE_LIST, HOTEL_NAMES
from fuzzywuzzy import fuzz
from time import time


class YesNo(Enum):
    YES = 'yes'
    NO = 'no'

    def __invert__(self):
        return YesNo.YES if self == YesNo.NO else YesNo.NO


class BuildTaxonomy(object):

    hotel_amenities = set()
    hotel_name = list()
    hotel_description = set()
    room_amenities = set()
    filtered_phrase_set = set()
    filter_phrase_list = [
        ' is available in the hotel rooms and costs  usd  14.99 per  24 '
        'hours.',
        'free!wifi is available in all areas and is free of charge.',
        'are not ',
        'pets are allowed. charges may apply.',
        ' is available on site (reservation is not needed) and costs  usd 68 per  day.',
        'paid ',
        'facilities for disabled guests',
        ' is available in the hotel rooms and costs  usd  16.95 per  24 '
        'hours.',
        ' is available on site (reservation is not needed) and costs  usd 47 per  day.',
        ' is available at a location nearby (reservation is not possible) '
        'and costs  usd 90 per  day.',
        ' is available at a location nearby (reservation is not needed) and '
        'costs  usd 78 per  day.',
        'free!wired internet is available in the hotel rooms and is free of '
        'charge.',
        ' is available on site (reservation is not needed) and costs  usd 80 per  day.',
        # 'number of buildings',
        # 'number of bars/lounges - 2',
        'french',
        'russian',
        'chinese',
        'italian',
        'english',
        'japanese',
        'spanish',
        ' allowed.',
        'use of nearby ',
        '/towers -  1',
        '/towers -  0',
        '/towers - 0',
        '/towers - 1',
        'filipino',
        'free ',
        '24-hour ',
        ' in lobby'
    ]

    def __init__(self, file_name, *args, **kwargs):
        """
        :param file_name:
        :param args:
        :param kwargs:
        """
        self.filename = file_name
        self.nlp = spacy.load("en_core_web_sm")
        self.hotel_taxonomies = dict()

    def read_file(self, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        :return:
        """
        reader = pd.read_csv(self.filename, delimiter=',')
        for index, rows in reader.iterrows():
            for row in rows[1].split(','):
                self.hotel_amenities.add(row)
            self.hotel_description.add(rows[2])
            self.hotel_name.append(rows[3])
            for row in rows[4].split(','):
                self.room_amenities.add(row)

    def filter(self, list_data=[]):
        """

        :param list_data:
        :return:
        """
        self.filtered_phrase_set.clear()
        for enity in list_data:
            for phrase in enity:
                for filtered_phrase in norm_obj.filter_phrase_list:
                    phrase = phrase.replace(filtered_phrase, '').strip()
                phrase = re.sub(r'^[a-z ]+ \- [0-9 ]+', '', phrase, flags=re.M)
                phrase = re.sub(r'^[a-z ]+ \([a-z0-9 ]+\)\-[0-9 ]+', '',
                                phrase,
                                flags=re.M)
                phrase = re.sub(r'\ssize[ a-z()\-0-9]+', ' ', phrase,
                                flags=re.M)
                phrase = re.sub(r'\([a-z ]+\)+', ' ', phrase, flags=re.M)
                phrase = re.sub(r'^built[a-z 0-9]+', ' ', phrase, flags=re.M)
                if phrase.strip():
                    self.filtered_phrase_set.add(phrase.strip())

    def __update_comprehensive_word__(self, token, language) -> str:
        """

        :param token:
        :param language:
        :return:
        """
        if language == 'UK':
            R_UK_US_COMPREHENSIVE_LIST = {
                v: k for k, v in UK_US_COMPREHENSIVE_LIST.items()
            }
            return R_UK_US_COMPREHENSIVE_LIST[token] if token in R_UK_US_COMPREHENSIVE_LIST else token
        else:
            return UK_US_COMPREHENSIVE_LIST[token] if token in UK_US_COMPREHENSIVE_LIST else token

    def __tokenize_and_lemmatize__(self, doc, language='US') -> list:
        """

        :param doc:
        :param language:
        :return:
        """
        return [
            self.__update_comprehensive_word__(token.lemma_, language) for token in doc if not token.is_punct and not token.is_digit
        ]

    def phrase_tokenization(self):
        """

        :return:
        """
        filtered_phrase = set()
        for phrase in self.filtered_phrase_set:
            doc = self.nlp(phrase)
            filtered_phrase.add(" ".join(
                self.__tokenize_and_lemmatize__(doc))
            )
        return list(filtered_phrase)

    def hotel_taxonomy(self, filtered_phrase):
        """

        :param filtered_phrase:
        :return:
        """
        self.hotel_taxonomies.clear()
        for phrase in filtered_phrase:
            self.hotel_taxonomies[phrase] = {
                name: YesNo.NO.name for name in HOTEL_NAMES
            }
        pass

    def read_file_by_rows(self):
        """

        :return:
        """
        reader = pd.read_csv(self.filename, delimiter=',')
        for index, rows in reader.iterrows():
            row = set(rows[1].split(','))
            self.filter([row])
            filter2 = self.phrase_tokenization()
            for f in filter2:
                if f in self.hotel_taxonomies:
                    for name in HOTEL_NAMES:
                        if name in rows[3] or fuzz.ratio(name, rows[3]) > 80:
                            self.hotel_taxonomies[f].update({
                                name: YesNo.YES.name
                            })
                            continue

    def write_hotel_taxonomy_csv(self, filename='hotel_taxonomy.csv'):
        """

        :param filename:
        :return:
        """
        df = pd.DataFrame(self.hotel_taxonomies).transpose()
        df.rename(
            index=str,
            columns={
                name: name.title() for name in HOTEL_NAMES
            },
            inplace=True
        )
        df.to_csv(filename)


if __name__ == '__main__':
    start_time = time()
    norm_obj = BuildTaxonomy('hotel.csv')
    print("*" * 50)
    norm_obj.read_file()
    norm_obj.filter([norm_obj.hotel_amenities])
    filtered_phrase_set = norm_obj.phrase_tokenization()
    norm_obj.hotel_taxonomy(filtered_phrase_set)
    norm_obj.read_file_by_rows()
    norm_obj.write_hotel_taxonomy_csv('hotel_taxonomy.csv')
    end_time = time()
    print("Total script execution time: {}".format(end_time - start_time))
    print("*" * 50)
