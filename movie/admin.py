# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from movie.models import Movie, Genere
# Register your models here.
admin.site.register(Movie)
admin.site.register(Genere)