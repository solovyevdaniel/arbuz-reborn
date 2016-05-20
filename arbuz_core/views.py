from django.shortcuts import render_to_response
from rest_framework.generics import ListAPIView
from .data import read_from_file
from .serializers import BuildingSerializer, CrimesSerializer
from .models import Building, Crimes


class BuildingListView(ListAPIView):
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer


class CrimesListView(ListAPIView):
    queryset = Crimes.objects.all()
    serializer_class = CrimesSerializer


def dump(request):
    # read_from_file()
    response = Building.objects.all()

    return render_to_response('main.html', {'response': response})
