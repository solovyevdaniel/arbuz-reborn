import json
file_path = '../Data/01m_2013/data_01_2013_part1.json'
string ='''
[{
    "street": "ПРОСП.   ПОБЕДЫ  буд",
    "building": "94/1",
    "location": [{"latitude": 50.459043, "longitude": 30.39884, "__type": "GeoPoint"}],
    "total": 2,
    "heav_osobo_heav": 0,
    "murder": 0,
    "intentional_injury": 0,
    "bodily_harm_with_fatal_cons": 0,
    "rape": 0,
    "theft": 1,
    "looting": 0,
    "brigandage": 0,
    "extortion": 0,
    "fraud": 0,
    "hooliganism": 0,
    "drugs": 0,
    "total_points": 1,
    "month": 1,
    "year": 2013
},
{
    "street": "ПРОСП.   ПОБЕДЫ  буд",
    "building": "94/1",
    "location": [{"latitude": 50.459043, "longitude": 30.39884, "__type": "GeoPoint"}],
    "total": 2,
    "heav_osobo_heav": 0,
    "murder": 0,
    "intentional_injury": 0,
    "bodily_harm_with_fatal_cons": 0,
    "rape": 0,
    "theft": 1,
    "looting": 0,
    "brigandage": 0,
    "extortion": 0,
    "fraud": 0,
    "hooliganism": 0,
    "drugs": 0,
    "total_points": 1,
    "month": 1,
    "year": 2014
}]
'''

def read_from_file():
    with open(file_path) as f:
        data = json.load(f)
        print(data)


read_from_file()