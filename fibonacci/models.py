from __future__ import unicode_literals
from django.utils import timezone
from mongoengine import fields, Document


class History(Document):
    """
    Store History Data
    """
    position = fields.IntField(default=1)
    value = fields.IntField(default=1)
    time = fields.IntField(default=0)
    creation_date = fields.DateTimeField(default=timezone.now, null=True)
    active = fields.IntField(default=1)

    def __str__(self):
        return str(self.id)
