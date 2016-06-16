# coding=utf-8
import json
import smtplib
from datetime import datetime
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from random import randint

from django.db.models import Min, Max, Count
from django.http import HttpResponse
from django.shortcuts import render, render_to_response, redirect
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from .serializers import BuildingSerializer, CrimesSerializer
from .models import Building, Crimes


class BuildingListView(ListAPIView):
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer


class CrimesListView(ListAPIView):
    queryset = Crimes.objects.all()
    serializer_class = CrimesSerializer


target_email = "vidkrytist@mvs.gov.ua"

base_email = "letter.author.name@gmail.com"
password = "azaza00754lol"

send_template = u"""
Запитувач name, email, phone,
Прошу інформацію відповідно до Закону України "Про доступ до публічної інформації" надати дані про правопорушення,
що сталися у місті Київ за проміжок часу start-end
Дані у вигляді: час скоєння правопорушення, день скоєння правопорушення, місце (точна адреса і також опис місцевості)
скоєння правопорушення, тип скоєння правопорушення (вид злочину).
Запитувану інформацію прошу надати у визначений законом строк на електронну адресу email
"""


@api_view(['POST'])
def send_letter(request):
    if request.user.is_anonymous():
        return Response({"data": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
    user = request.user

    data = request.data
    user.first_name = data['first_name']
    user.last_name = data['last_name']
    user.middle_name = data['middle_name']
    user.phone_number = data['phone_number']
    user.start_date = data['start_date']
    user.end_date = data['end_date']

    name = user.last_name + " " + user.first_name + " " +\
        user.middle_name
    email = base_email
    phone = user.phone_number
    start_date = user.start_date
    end_date = user.end_date
    send_date = datetime.now().strftime("%Y-%m-%d")

    letter = send_template.replace('name', name).replace('email', email)\
        .replace('phone', phone).replace('start', str(start_date)).replace('end', str(end_date))
    letter += send_date

    msg = MIMEMultipart('alternative')
    h = Header('Subject', 'utf-8')
    msg['Subject'] = h
    plain = MIMEText(letter.encode('utf-8'), 'plain', 'utf-8')
    msg['Subject'] = 'Send email'
    msg['From'] = email
    msg['To'] = target_email
    msg.attach(plain)
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.ehlo()
    s.starttls()
    s.login(email, password)
    s.sendmail(email, [target_email], msg.as_string())
    s.quit()
    return redirect('/admin')


@api_view(['GET'])
def get_send_letter_form(request):
    return render(request, 'send_letter.html')


@api_view(['GET'])
def get_crimes_grid(request):
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
        rows_count = randint(1, int(buildings_per_row))
    if buildings_per_column < 1:
        columns_count = 1
    else:
        columns_count = randint(1, int(buildings_per_column))
    cell_size = (length / rows_count, width / columns_count)
    table = []
    for i in range(rows_count):
        table.append([])
        for j in range(columns_count):
            top_left = (bound_buildings['latitude_min'] + i * cell_size[0],
                        bound_buildings['longitude_min'] + i * cell_size[1])
            right_bottom = (bound_buildings['latitude_min'] + (i + 1) * cell_size[0],
                            bound_buildings['longitude_min'] + (i + 1) * cell_size[1])
            matching_buildings = Building.objects.filter(longitude__range=(top_left[1], right_bottom[1]),
                                                         latitude__range=(top_left[0], right_bottom[0]))
            center_coords = (top_left[1] * 1.5, top_left[0] * 1.5)
            crimes_count = 0
            for building in matching_buildings:
                for crime in building.crimes:
                    crimes_count += crime.get_crimes_total_count()
            cell = {
                'longitude': center_coords[0],
                'latitude': center_coords[1],
                'crimes_count': crimes_count,
            }
            table[i].append(cell)
    return HttpResponse(json.dumps({'results': table}))