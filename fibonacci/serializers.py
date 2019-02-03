from rest_framework import serializers
from rest_framework_mongoengine import serializers as mongoserializers
from fibonacci.models import History


class HistorySerializer(mongoserializers.DocumentSerializer):

    class Meta:
        model = History
        fields = '__all__'

    def validate(self, data):
        if 'position' not in data:
            raise serializers.ValidationError("Position not present")

        if 'value' not in data or data['value'] < 0:
            raise serializers.ValidationError("Invalid Value")

        if 'time' not in data or data['time'] < 1:
            raise serializers.ValidationError("Invalid time")

        return data

    def fill(self):
        return self.validated_data
