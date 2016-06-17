from random import randint, random

from decimal import Decimal
from django.core.management import BaseCommand

from arbuz_core.models import Building, CrimeStat
from django.db.models import Min, Max, Count


class Command(BaseCommand):
    def handle(self, *args, **options):
        print 'Update crime stats job has been started'
        CrimeStat.objects.all().delete()
        print 'Removed old data'
        bound_buildings = Building.objects.aggregate(Count('id'), Min('longitude'), Min('latitude'),
                                                     Max('longitude'), Max('latitude'))
        buildings_count = bound_buildings['id__count']
        length = bound_buildings['latitude__max'] - bound_buildings['latitude__min']
        width = bound_buildings['longitude__max'] - bound_buildings['longitude__min']
        proportion = buildings_count / (width * length)
        buildings_per_row = length * proportion
        buildings_per_column = width * proportion
        if buildings_per_row < 1:
            rows_count = 1
        else:
            rows_count = randint(1, int(buildings_per_row)) % 25
        if buildings_per_column < 1:
            columns_count = 1
        else:
            columns_count = randint(1, int(buildings_per_column)) % 25
        cell_size = (length / rows_count, width / columns_count)
        for i in range(rows_count):
            for j in range(columns_count):
                top_left = (bound_buildings['latitude__min'] + j * cell_size[0],
                            bound_buildings['longitude__min'] + i * cell_size[1])
                right_bottom = (bound_buildings['latitude__min'] + (j + 1) * cell_size[0],
                                bound_buildings['longitude__min'] + (i + 1) * cell_size[1])
                matching_buildings = Building.objects.filter(longitude__gt=top_left[1], longitude__lt=right_bottom[1],
                                                         latitude__gt=top_left[0], latitude__lt=right_bottom[0])
                center_coords = (top_left[1] * Decimal(1.5), top_left[0] * Decimal(1.5))
                crimes_count = 0
                for building in matching_buildings:
                    for crime in building.crimes.all():
                        crimes_count += crime.get_crimes_total_count()
                crimes_count += ((2 * random() - 1) * crimes_count)
                CrimeStat.objects.create(
                    longitude=center_coords[0],
                    latitude=center_coords[1],
                    crimes_coefficient=crimes_count
                )
    print 'Update crime stats is done'
