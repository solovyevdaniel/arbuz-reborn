import json
from arbuz_core.models import Building, Crimes
from datetime import datetime


file_path = './Data/01m_2013/data_01_2013_part4.json'
# file_path = ''

def read_from_file():
    with open(file_path) as f:
        data = json.load(f)
        print(len(data))
        for d in range(len(data)):
            building = Building(street=data[d]['street'],
                                number=data[d]['building'],
                                latitude=data[d]['location'][0]['latitude'],
                                longitude=data[d]['location'][0]['longitude'])
            building.save()

            get_building = Building.objects.filter(street=data[d]['street']).get(number=data[d]['building'])
            crimes = Crimes(building_id=get_building,
                            year_month=datetime.strptime('01-{}-{}'.format(data[d]['month'], data[d]['year']), "%d-%m-%Y"),
                            total=data[d]['total'],
                            total_points=data[d]['total_points'],
                            bodily_harm_with_fatal_cons=data[d]['bodily_harm_with_fatal_cons'],
                            brigandage=data[d]['brigandage'],
                            drugs=data[d]['drugs'],
                            extortion=data[d]['extortion'],
                            fraud=data[d]['fraud'],
                            grave_and_very_grave=data[d]['heav_osobo_heav'],
                            hooliganism=data[d]['hooliganism'],
                            intentional_injury=data[d]['intentional_injury'],
                            looting=data[d]['looting'],
                            murder=data[d]['murder'],
                            rape=data[d]['rape'],
                            theft=data[d]['theft'])
            crimes.save(force_insert=True)
    return data