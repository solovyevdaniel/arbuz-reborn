from rest_framework import serializers
from .models import Building, Crimes


class CrimesSerializer(serializers.ModelSerializer):
    # building_id = serializers.
    # def to_representation(self, instance):
    #     data = Crimes.objects.filter(year_month=self.request.GET.get('crimes__year_month'), '%Y-%m-%d')
    #     return data
    # building_id = BuildingSerializer(read_only=True)
    class Meta:
        model = Crimes
        fields = ('id',
                  # 'building',
                  'year_month',
                  'total',
                  'total_points',
                  'bodily_harm_with_fatal_cons',
                  'brigandage',
                  'drugs',
                  'extortion',
                  'fraud',
                  'grave_and_very_grave',
                  'hooliganism',
                  'intentional_injury',
                  'looting',
                  'murder',
                  'rape',
                  'theft')


class BuildingSerializer(serializers.ModelSerializer):
    crimes = CrimesSerializer(many=True, read_only=True)

    class Meta:
        model = Building
        fields = ('id',
                  'longitude',
                  'latitude',
                  'number',
                  'street',
                  'crimes')
