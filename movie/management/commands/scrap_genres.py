from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from tmdbv3api import TMDb, Genre

from movie.models import Genere

tmdb = TMDb()
tmdb.api_key = settings.API_KEY


class Command(BaseCommand):
    help = 'Scrap genres'

    def add_arguments(self, parser):
        parser.add_argument('page', type=int)

    def handle(self, *args, **options):
        genre = Genre()
        genres = genre.movie_list()
        for g in genres:
            Genere.objects.get_or_create(id=g.id, title=g.name)
