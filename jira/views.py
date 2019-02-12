# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from django.http import HttpResponse
from datetime import datetime
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework import viewsets, status
from django.test import TestCase, Client

from jira.models import Tickets, Users
from jira.serializers import TicketsSerializer, UsersSerializer


class Jira(viewsets.ViewSet):
    """
    Handing Ticket functions such as:
    Create: { url => /jira/, request_type => POST , Data => Data required for ticket creation} For Creating Tickets
    Get_tickets: { url => /jira/get_tickets/, request_type => GET} For getting Tickets list
    """

    def create(self, request):
        """
        Saving ticket data.
        :param request:
        :return:
        """
        data = self.request.data
        try:
            data = data['data']
            data.update({'creation_date': datetime.now(), 'update_date': datetime.now(), 'active': 1, 'priority': 0})
            serializer = TicketsSerializer(data=data)
            if serializer.is_valid():
                serializer.fill()
                serializer.save()

            return HttpResponse(json.dumps('OK'), content_type='application/json')
        except Exception as e:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @list_route(methods=['get'], url_path='get_tickets')
    def get_tickets(self, request):

        """
        Get saved history data.
        :param request:
        :return:
        """

        tickets = Tickets.objects.filter(active=1)
        data = {}
        data['ticket'] = [{'summary': ticket.summary, 'description': ticket.description, 'assignee': ticket.assignee,
                 'reporter': ticket.reporter, 'status': ticket.status, 'creation_date': ticket.creation_date,
                 'updated_date': ticket.update_date, 'tag': ticket.tag} for ticket in tickets]

        users = Users.objects.filter(active=1)
        data['users'] = [user.first_name for user in users]

        return Response(data, status=status.HTTP_200_OK)


class UserData(viewsets.ViewSet):
    """
    Handling User functions such as:
    Create: { url => /user/, request_type => POST , Data => Data required for user create} For Creating Users(Assignee/Reporter)
    """

    def create(self, request):
        """
        Saving user data.
        :param request:
        :return:
        """
        data = self.request.data
        try:
            data = data['data']
            serializer = UsersSerializer(data=data)
            if serializer.is_valid():
                serializer.fill()
                serializer.save()

            return HttpResponse(json.dumps('OK'), content_type='application/json')
        except Exception as e:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @list_route(methods=['get'], url_path='get_users')
    def get_users(self, request):

        """
        Get saved history data.
        :param request:
        :return:
        """

        users = Users.objects.filter(active=1)
        data = [user.first_name for user in users]

        return Response(data, status=status.HTTP_200_OK)


class JiraPageViewTest(TestCase):

    def mock_ticket_data(self):
        data = {
            'summary': 'Summary',
            'description': 'Description',
            'assignee': 'Assignee',
            'reporter': 'Reporter',
            'status': 'Done',
            'tag': 'All Done'
        }

        return data

    def test_ticket_create(self):

        data = {'data': self.mock_ticket_data()}
        response = self.client.post('/jira/', data=json.dumps(data))

        self.assertEqual(response.status_code, 200, 'Ticket Creation Failed')

    def test_ticket_fetch(self):

        response = self.client.get('/jira/get_tickets/')

        self.assertEqual(response.status_code, 200, 'Ticket Creation Failed')
