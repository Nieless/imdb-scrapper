from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from tmdbv3api import TMDb, Movie as MV

from movie.models import Movie

tmdb = TMDb()
tmdb.api_key = settings.API_KEY


class Command(BaseCommand):
    help = 'Scrap movies'

    def add_arguments(self, parser):
        parser.add_argument('page', type=int)

    def handle(self, *args, **options):
        page = options['page']
        mv = MV()
        popular = mv.popular(page=page)

        for m in popular:
            data = dict()
            data['id'] = m.id
            data['released_year'] = datetime.strptime(m.release_date.split('-')[0], "%Y") \
                if m.release_date else datetime.now()
            data['rating'] = m.vote_average if m.vote_average is not 0 else 10.0
            data['title'] = m.title
            data['discription'] = m.overview
            mv_obj, created = Movie.objects.get_or_create(**data)
            mv_obj.genre.add(*m.genre_ids)
