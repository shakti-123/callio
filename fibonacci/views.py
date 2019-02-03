# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from django.http import HttpResponse
from datetime import datetime
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework import viewsets, status
from mongoengine import Q

from fibonacci.models import History
from fibonacci.serializers import HistorySerializer


class Fibonacci(viewsets.ViewSet):

    @list_route(methods=['get'], url_path='get_number')
    def get_number(self, request):
        '''
        Get value of fibonacci series at particular position.
        :param request:
        :return:
        '''

        start = datetime.now()
        position = int(request.query_params.get('position', 1))
        pie = (1 + 5 ** 0.5) / 2
        denom = 5 ** 0.5
        value = ((pie**position) - (1-pie)**position)/denom
        end = datetime.now()

        time = end - start
        data_to_send = {'value': int(value), 'time': time.microseconds}
        return HttpResponse(json.dumps(data_to_send), content_type='application/json')

    def create(self, request):
        '''
        Saving data of last search.
        :param request:
        :return:
        '''
        data = self.request.data

        try:
            serializer = HistorySerializer(data=data)
            if serializer.is_valid():
                data.update({'creation_date': datetime.now(), 'active': 1})
                History.objects.filter(Q(position=data['position']) & Q(value=data['value'])).update(upsert=True, multi=True, **data)

            return HttpResponse(json.dumps('OK'), content_type='application/json')
        except Exception as e:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @list_route(methods=['get'], url_path='get_history')
    def get_history(self, request):

        '''
        Get saved history data.
        :param request:
        :return:
        '''

        histories = History.objects.all()
        data = [{'position': history.position, 'value': history.value, 'time': history.time} for history in histories]

        return Response(data, status=status.HTTP_200_OK)
