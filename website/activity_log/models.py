from django.db import models
from django.contrib.contenttypes import generic


class Action (models.Model):
    actor = models.ForeignKey('auth.User', related_name='actions')
    """The user that took the action"""

    description = models.CharField(max_length=128)
    """The action they took"""

    datetime = models.DateTimeField(auto_now=True)
    """The time that they took the action"""

    # affected_content (backref)
    """The set of content that they affected"""


class AffectedContent (models.Model):
    action = models.ForeignKey('Action', related_name='affected_content')
    """The action taken"""

    item_type = models.ForeignKey('contenttypes.ContentType')
    item_id = models.PositiveIntegerField()
    item = generic.GenericForeignKey('item_type', 'item_id')
    """The content item affected (potentially one of many)"""
