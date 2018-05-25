# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets

from movie.models import Movie
from movie.serializers import MovieSerializer
from movie.movie_filter import MovieFilter


class MovieViewset(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_class = MovieFilter
    http_method_names = ['get']
