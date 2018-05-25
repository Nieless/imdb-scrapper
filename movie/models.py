# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.

class Movie(models.Model):
    title = models.CharField(max_length=1000)
    discription = models.TextField()
    released_year = models.DateTimeField()
    rating = models.FloatField(default=10.0)
    genre = models.ManyToManyField('Genere')

    class Meta:
        verbose_name = 'Movie'

    def __unicode__(self):
        return '{0}'.format(self.title)


class Genere(models.Model):
    title = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Genre'

    def __unicode__(self):
        return '{0}'.format(self.title)
