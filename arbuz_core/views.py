# coding=utf-8
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.shortcuts import render
from django.utils import timezone
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
target_email = "psyhoge@gmail.com"

send_template = """
Запитувач name, email, phone,
Прошу інформацію відповідно до Закону України "Про доступ до публічної інформації" надати дані про правопорушення,
що сталися у місті Київ за проміжок часу start-end
Дані у вигляді: час скоєння правопорушення, день скоєння правопорушення, місце (точна адреса і також опис місцевості)
скоєння правопорушення, тип скоєння правопорушення (вид злочину).
Запитувану інформацію прошу надати у визначений законом строк на електронну адресу email
send_date
"""


@api_view(['GET'])
def send_letter(request):
    if request.user.is_anonymous():
        return Response({"data": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
    user = request.user

    data = request.data
    name = user.first_name + " " + user.last_name + " " +\
        user.middle_name
    email = user.email
    phone = user.phone_number
    start_date = user.start_date
    end_date = user.end_date
    send_date = timezone.now()

    letter = send_template.replace('name', name).replace('email', email)\
        .replace('phone', phone).replace('start', start_date).replace('end', end_date).replace('send_date', send_date)

    password = data['password']
    msg = MIMEText(letter)
    msg['Subject'] = 'Send email'
    msg['From'] = email
    msg['To'] = target_email
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.ehlo()
    s.starttls()
    s.login(email, password)
    s.sendmail(email, [target_email], msg.as_string())
    s.quit()