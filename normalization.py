import csv
import re
import time
from collections import defaultdict
from enum import Enum

import pandas as pd
import spacy
from fuzzywuzzy import fuzz

from settings import UK_US_COMPREHENSIVE_LIST, HOTEL_NAMES

start_time = time.time()
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
    # 'number of ',
    # 'number of bars/lounges - 2',
    'russian',
    'french',
    'chinese',
    'italian',
    'english',
    'japanese',
    'spanish',
    ' allowed.',
    'use of nearby ',
    # '/towers -  1',
    # '/towers -  0',
    # '/towers - 0',
    # '/towers - 1',
    'filipino',
    'greek',
    'free ',
    '24-hour ',
    ' in lobby',
    'safe'
    'in room accessibility'
]
category = ['shop', 'center', 'service', 'spa', 'parking', 'pet', 'bar',
            'storage', 'pool', 'atm', 'desk', 'smoking', 'wifi', 'elevator',
            'breakfast', 'tv', 'salon', 'rental'
            ]


class YesNo(Enum):
    YES = 'yes'
    NO = 'no'

    def __invert__(self):
        return YesNo.YES if self == YesNo.NO else YesNo.NO


def update_comprehensive_word__(token, language) -> str:
    """

    :param token:
    :param language:
    :return:
    """
    if language == 'UK':
        R_UK_US_COMPREHENSIVE_LIST = {
            v: k for k, v in UK_US_COMPREHENSIVE_LIST.items()
        }
        return R_UK_US_COMPREHENSIVE_LIST[
            token].strip() if token in R_UK_US_COMPREHENSIVE_LIST else \
            token.strip()
    else:
        return UK_US_COMPREHENSIVE_LIST[
            token].strip() if token in UK_US_COMPREHENSIVE_LIST else \
            token.strip()


def filter(data_entity=[]):
    filtered_phrase_set = set()
    for enity in data_entity:
        for phrase in enity:
            for c in filter_phrase_list:
                phrase = phrase.replace(c, '').strip()
            phrase = re.sub(r'^[a-z ]+ \- [0-9 ]+', '', phrase, flags=re.M)
            phrase = re.sub(r'^[a-z ]+ \([a-z0-9 ]+\)\-[0-9 ]+', '', phrase,
                            flags=re.M)
            phrase = re.sub(r'\ssize[ a-z()\-0-9]+', ' ', phrase, flags=re.M)
            phrase = re.sub(r'\([a-z ]+\)+', ' ', phrase, flags=re.M)
            phrase = re.sub(r'^built[a-z 0-9]+', ' ', phrase, flags=re.M)
            if phrase.strip():
                filtered_phrase_set.add(phrase.strip())
    return list(filtered_phrase_set)


def final_filter(data_set=set()):
    filtered_phrase_set = set()
    for dc in data_set:
        doc = nlp(dc)
        filtered_phrase_set.add(" ".join([update_comprehensive_word__(
            token.lemma_, 'US') for token in doc if not
                                                    token.is_punct and not token.is_digit]))
    return list(filtered_phrase_set)


if __name__ == '__main__':
    hotel_amenities = set()
    hotel_name = []
    hotel_description = set()
    room_amenities = set()
    reader = pd.read_csv('hotel.csv', delimiter=',')
    for index, rows in reader.iterrows():
        for row in rows[1].split(','):
            hotel_amenities.add(row.replace('/', ' or '))
        hotel_description.add(rows[2])
        hotel_name.append(rows[3])
        for row in rows[4].split(','):
            room_amenities.add(row)
    nlp = spacy.load("en_core_web_sm")
    print("*" * 95)
    filtered_phrase_set = filter([hotel_amenities])
    filtered_phrase_set2 = final_filter(filtered_phrase_set)

    catogory_dict = defaultdict(list)
    for c in category:
        for ph in filtered_phrase_set2:
            sp = ph.split(' ')
            if c in sp:
                catogory_dict[c].append(ph)
                if ph in filtered_phrase_set2:
                    filtered_phrase_set2.remove(ph)
                if len(sp) == 1 and c in filtered_phrase_set2:
                    filtered_phrase_set2.remove(c)

    for li in filtered_phrase_set2:
        catogory_dict['others'].append(li)
    hotel_taxonomy = defaultdict()
    for k, v in catogory_dict.items():
        if v is None:
            hotel_taxonomy[k] = {
                name: YesNo.NO.name for name in HOTEL_NAMES
            }
        else:
            for vn in v:
                if k not in hotel_taxonomy:
                    hotel_taxonomy[k] = {
                        vn: {
                            name: YesNo.NO.name for name in HOTEL_NAMES
                        }
                    }
                else:
                    hotel_taxonomy[k].update({
                        vn: {
                            name: YesNo.NO.name for name in HOTEL_NAMES
                        }
                    })
    # with open('category.csv', 'w', newline='') as f:
    #     w = csv.writer(f)
    #     h = 0
    #     for k, v in catogory_dict.items():
    #         if isinstance(v, list):
    #             i = 0
    #             for l in v:
    #                 if i == 0:
    #                     k = k
    #                     i = 1
    #                 else:
    #                     k = ''
    #                 w.writerow([k, l])
    given_list = ['wifi', 'parking']
    for index, rows in reader.iterrows():
        row = set(rows[1].split(','))
        filter1 = filter([row])
        filter2 = final_filter(filter1)
        for f in filter2:
            e = f
            token_text, token_number = 'FREE', 0
            for r in row:
                if f in r or fuzz.ratio(f, r) > 80:
                    doc = nlp(r)
                    for token in doc:
                        if token.like_num:
                            token_text = token.text
                            break

            for k, v in hotel_taxonomy.items():
                for h in v:
                    if fuzz.ratio(h, f) > 80:
                        for name in HOTEL_NAMES:
                            if (name in rows[3] or fuzz.ratio(name, \
                                    rows[3]) > 80) and any(w in h.split(' ') for w in given_list):
                                hotel_taxonomy[k][h].update({
                                    name: token_text
                                })
                            elif name in rows[3] or fuzz.ratio(name, rows[3])\
                                > 80:
                                hotel_taxonomy[k][h].update({
                                    name: YesNo.YES.name
                                })
                                continue

    print(''.join(["||{:>10}||{:>35}" .format(
        "Category",
        "Sub Category"
    )] + ['||{:>20}'.format(name.title()) for name in HOTEL_NAMES]) + '||')
    df = pd.DataFrame(hotel_taxonomy)

    for k, v in hotel_taxonomy.items():
        i = 0
        if isinstance(v, dict):
            for l, j in v.items():
                if i == 0:
                    k = k
                    i = 1
                else:
                    k = ''
                st = ''.join(['||{:>10}||{:>35}'.format(k, l)] + ['||{'
                                                             ':>20}'.format(
                    e) for d, e in j.items()])
                print(st + '||')


    # with open('hotel_taxonomy2.csv', 'w', newline='') as f:
    #     w = csv.writer(f)
    #     h = 0
    #     for k, v in hotel_taxonomy.items():
    #         i = 0
    #         for l in v:
    #             if i == 0:
    #                 k = k
    #                 i = 1
    #             else:
    #                 k = ''
    #             w.writerow([k, l])
    # df = pd.DataFrame(hotel_taxonomy).transpose()
    # df.rename(index=str, columns={name: name.title() for name in HOTEL_NAMES},
    #           inplace=True)
    # df.to_csv('hotel_taxonomy.csv')
    end_time = time.time()
    print("Total script execution time: {}".format(end_time - start_time))
    print("*" * 95)

