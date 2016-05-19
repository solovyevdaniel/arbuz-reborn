from django.shortcuts import render
from rest_framework.generics import ListAPIView

from .serializers import BuildingSerializer, CrimesSerializer
from .models import Building, Crimes


class BuildingListView(ListAPIView):
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer


class CrimesListView(ListAPIView):
    queryset = Crimes.objects.all()
    serializer_class = CrimesSerializer
