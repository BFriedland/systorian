from __future__ import unicode_literals

from django.db import models
from django.contrib.postgres.fields import JSONField


class Entry(models.Model):
    created = models.DateTimeField(auto_now_add=True, editable=False)
    command = models.CharField(max_length=255)
    data = JSONField()

    class Meta:
        ordering = ('-created',)

    def __unicode__(self):
        return u'{}: {}'.format(self.id, self.created)
