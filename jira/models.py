from __future__ import unicode_literals
from django.utils import timezone
from mongoengine import fields, Document


class Users(Document):
    """
    Stores User data
    """
    first_name = fields.StringField(default='')
    middle_name = fields.StringField(default='')
    last_name = fields.StringField(default='')
    email = fields.StringField(default='')
    mobile = fields.IntField(default=0)
    team = fields.StringField(default='')
    active = fields.IntField(default=1)

    def __str__(self):
        return str(self.id)


class Tickets(Document):
    """
    Stores Tickets Data
    """
    summary = fields.StringField(default='')
    description = fields.StringField(default='')
    # assignee = fields.ReferenceField(Users, default=None)
    # reporter = fields.ReferenceField(Users, default=None)
    assignee = fields.StringField(default='')
    reporter = fields.StringField(default='')
    status = fields.StringField(default='')
    tag = fields.StringField(default='')
    creation_date = fields.DateTimeField(default=timezone.now, null=True)
    update_date = fields.DateTimeField(default=timezone.now, null=True)
    priority = fields.IntField(default=0)  # 0: low, 1: Medium, 2: High
    active = fields.IntField(default=1)

    def __str__(self):
        return str(self.id)


class Status(Document):
    """
    Stores Status data
    """
    name = fields.StringField(default='')
    active = fields.IntField(default=1)

    def __str__(self):
        return str(self.id)

