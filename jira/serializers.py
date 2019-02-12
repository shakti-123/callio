from rest_framework import serializers
from rest_framework_mongoengine import serializers as mongoserializers
from jira.models import Tickets, Users


class TicketsSerializer(mongoserializers.DocumentSerializer):

    class Meta:
        model = Tickets
        fields = '__all__'

    def validate(self, data):
        if 'summary' not in data:
            raise serializers.ValidationError("Summary can not be empty")

        if 'reporter' not in data:
            raise serializers.ValidationError("reporter can not be empty")

        if 'status' not in data or 'status' == '':
            raise serializers.ValidationError("Status must be defined")

        if 'priority' not in data or 'priority' == '':
            raise serializers.ValidationError("Priority must be defined")

        return data

    def fill(self):
        return self.validated_data


class UsersSerializer(mongoserializers.DocumentSerializer):

    class Meta:
        model = Users
        fields = '__all__'

    def validate(self, data):
        if 'first_name' not in data or 'first_name' == '':
            raise serializers.ValidationError("First name not be empty")

        if 'last_name' not in data or 'last_name' == '':
            raise serializers.ValidationError("Last name not be empty")

        if 'team' not in data or 'team' == '':
            raise serializers.ValidationError("Team can not be empty")

        return data

    def fill(self):
        return self.validated_data
