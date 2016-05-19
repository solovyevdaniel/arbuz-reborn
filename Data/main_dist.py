# -*- coding: utf-8 -*-
__author__ = 'dan'

import xlrd
from collections import OrderedDict
import json

excel_file = xlrd.open_workbook('Crime/2013/01m_2013/01m_2013.xls')
sheet = excel_file.sheet_by_index(1)

d = {}
crime_list = []
counter = 0

for i in range(2, sheet.nrows):
    list = OrderedDict()
    counter += 1
    print counter

    row_values = sheet.row_values(i)

    district = row_values[1]
    district = [x.encode('utf8') for x in district]
    list['dist_name'] = ('').join(district)
    list['total'] = int(row_values[2])
    list['heav_osobo_heav'] = int(row_values[3])
    list['murder'] = int(row_values[4])
    list['intentional_injury'] = int(row_values[5])
    list['bodily_harm_with_fatal_cons'] = int(row_values[6])
    list['rape'] = int(row_values[7])
    list['theft'] = int(row_values[8])
    # list['ST185_TR'] = int(row_values[9])
    list['looting'] = int(row_values[10])
    list['brigandage'] = int(row_values[11])
    list['extortion'] = int(row_values[12])
    list['fraud'] = int(row_values[13])
    # list['occupation'] = int(row_values[14]) * 2
    list['hooliganism'] = int(row_values[15])
    list['drugs'] = int(row_values[16])
    # list['done_nesov'] = int(row_values[17])
    sum_points = (int(row_values[3]) * 5) + (int(row_values[4]) * 5) + (int(row_values[5]) * 4) + \
                 (int(row_values[6]) * 5) + (int(row_values[7]) * 4) + (int(row_values[8]) * 1) + \
                 (int(row_values[10]) * 2) + (int(row_values[11]) * 3) + (int(row_values[12]) * 2) + \
                 (int(row_values[13]) * 1) + (int(row_values[15]) * 1) + (int(row_values[16]) * 3)
    list['total_points'] = sum_points
    list['month'] = int(1)
    list['year'] = int(2013)
    crime_list.append(list)

d['results'] = crime_list
add_to_json = json.dumps(d, ensure_ascii=False)

# add_to_json = json.dumps(crime_list, ensure_ascii=False)
#add_to_json = add_to_json.encode('utf8')

with open('Crime/2013/01m_2013/data_dist_01_2013.json', 'w') as f:
# with open('data.json', 'w') as f:
    f.write(add_to_json)