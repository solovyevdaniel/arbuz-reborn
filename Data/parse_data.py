# -*- coding: utf-8 -*-
__author__ = 'dan'

import xlrd
from collections import OrderedDict
import json
import requests


def parse_data_from_file(f):
    print('aaaaaaaaaa')
    pass

# excel_file = xlrd.open_workbook('Crime/2014/09m_2014/09m_2014.xls')
# # excel_file = xlrd.open_workbook('1.xls')
# sheet = excel_file.sheet_by_index(2)
#
# crime_list = []
# counter = 0
#
# for i in range(12502, 14627):
#     list = OrderedDict()
#     locations = OrderedDict()
#     counter += 1
#     print (counter)
#     row_values = sheet.row_values(i)
#
#     address = row_values[1].split('.')
#     address = [x.encode('utf8') for x in address]
#
#     sum_points = (int(row_values[3]) * 5) + (int(row_values[4]) * 5) + (int(row_values[5]) * 4) + \
#                          (int(row_values[6]) * 5) + (int(row_values[7]) * 4) + (int(row_values[8]) * 1) + \
#                          (int(row_values[9]) * 2) + (int(row_values[10]) * 2) + (int(row_values[11]) * 3) + \
#                          (int(row_values[12]) * 2) + (int(row_values[13]) * 3) + (int(row_values[14]) * 1) + \
#                          (int(row_values[15]) * 3)
#
#     if address[-1] == '' or address[-1] == None or sum_points == 0 or int(row_values[2]) == 0:
#          continue
#     else:
#         key = 'AIzaSyBQ5Bu8s_ZjxD3kfKsJCMr3vVU8tNFIi3k'
#         lal = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + ' '.join(address) + \
#               ' Киев,Украина&key=' + key
#         r = requests.get(lal)
#         if r.json()['status'] != 'OK' or \
#                 ((r.json()['results'][0]['geometry']['location']['lat'] == 50.4501) and
#                      (r.json()['results'][0]['geometry']['location']['lng'] == 30.5234)):
#             continue
#         else:
#             list['street'] = ('. ').join(address[:-1])
#             list['building'] = address[-1]
#
#             locations['latitude'] = r.json()['results'][0]['geometry']['location']['lat']
#             locations['longitude'] = r.json()['results'][0]['geometry']['location']['lng']
#             locations['__type'] = 'GeoPoint'
#             list['location'] = locations
#
#             list['total'] = int(row_values[2])
#             list['heavy'] = int(row_values[3])
#             list['murder'] = int(row_values[4])
#             list['intentional_injury'] = int(row_values[5])
#             list['bodily_harm_with_fatal_cons'] = int(row_values[6])
#             list['rape'] = int(row_values[7])
#             list['theft'] = int(row_values[8])
#             list['looting'] = int(row_values[9])
#             list['brigandage'] = int(row_values[10])
#             list['extortion'] = int(row_values[11])
#             list['fraud'] = int(row_values[12])
#             list['car_theft'] = int(row_values[13])
#             list['hooliganism'] = int(row_values[14])
#             list['drugs'] = int(row_values[15])
#
#
#             list['total_points'] = sum_points
#             list['month'] = int(9)
#             list['year'] = int(2014)
#             crime_list.append(list)
#
# # d['results'] = crime_list
# # add_to_json = json.dumps(d, ensure_ascii=False)
#
# add_to_json = json.dumps(crime_list, ensure_ascii=False)
#
#
# with open('Crime/2014/09m_2014/address_6.json', 'w') as f:
# # with open('data.json', 'w') as f:
#     f.write(add_to_json)
#
#
