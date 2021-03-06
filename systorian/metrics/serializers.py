from metrics.models import Entry

from rest_framework import serializers


class EntrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Entry
        fields = (
            'id',
            'created',
            'command',
            'data',
        )
