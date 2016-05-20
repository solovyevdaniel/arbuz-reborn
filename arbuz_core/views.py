# coding=utf-8

import smtplib
from datetime import datetime
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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


# target_email = "vidkrytist@mvs.gov.ua"
target_email = "dd.aa.nn.1.kk@gmail.com"

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
    email = data['email']
    phone = user.phone_number
    start_date = user.start_date
    end_date = user.end_date
    send_date = datetime.now().strftime("%Y-%m-%d")

    letter = send_template.replace('name', name).replace('email', email)\
        .replace('phone', phone).replace('start', str(start_date)).replace('end', str(end_date))
    letter += send_date

    password = data['password']
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