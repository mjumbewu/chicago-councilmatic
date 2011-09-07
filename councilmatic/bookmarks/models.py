from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

class Bookmark (models.Model):
    user = models.ForeignKey('auth.User', related_name='bookmarks')
    content_id = models.PositiveIntegerField()
    content_type = models.ForeignKey(ContentType)
    content = generic.GenericForeignKey('content_id', 'content_type')
