from datetime import datetime
import django_filters
from django.db.models import Q
from django.conf import settings
from tmdbv3api import TMDb, Discover, Movie as MV
from tmdbv3api.exceptions import TMDbException

from movie.models import Movie

tmdb = TMDb()
tmdb.api_key = settings.API_KEY


class MovieFilter(django_filters.FilterSet):
    id = django_filters.NumberFilter(method='filter_id')
    title = django_filters.CharFilter(method='filter_title')
    released_year = django_filters.NumericRangeFilter(method='filter_year')
    rating = django_filters.RangeFilter(method='filter_rating')

    class Meta:
        model = Movie
        fields = ['id', 'rating', 'released_year', 'title', 'genre']

    def filter_id(self, queryset, name, value):
        if not value:
            return queryset
        if not queryset.filter(id=value).exists():
            self.scrap_movie_by_id(value)
        return queryset.filter(id=value)

    def filter_title(self, queryset, name, value):
        if not value:
            return queryset
        if not queryset.filter(title=value).exists():
            self.scrap_movie_by_title(value)
        return queryset.filter(title=value)

    def filter_rating(self, queryset, name, value):
        query_condition = Q()
        start = 0
        stop = 10

        if not value:
            return queryset

        if value.start:
            start = value.start
            query_condition.add(Q(rating__gte=start), Q.AND)

        if value.stop:
            stop = value.stop
            query_condition.add(Q(rating__lte=stop), Q.AND)

        if not queryset.filter(query_condition).exists():
            self.scrap_movie_by_rating(start, stop)

        return queryset.filter(query_condition)

    def filter_year(self, queryset, name, value):
        query_condition = Q()
        start = value.start
        stop = value.stop

        if not value:
            return queryset

        if start and not stop:
            query_condition.add(Q(released_year__year=start), Q.AND)

        if stop and not start:
            query_condition.add(Q(released_year__year=stop), Q.AND)

        if start and stop:
            query_condition.add(Q(released_year__year__range=[start, stop]), Q.AND)

        if not queryset.filter(query_condition).exists():
            self.scrap_movie_by_year(start, stop)
        return queryset.filter(query_condition)

    def scrap_movie_by_id(self, id):
        movie = MV()
        m = movie.details(id)
        self.set_data(m)

    # def scrap_movie_by_title(self, title):
    # import urllib2
    # from bs4 import BeautifulSoup
    #     page = urllib2.urlopen(url + '?title=' + title)
    #     print page, 'page'
    #     soup = BeautifulSoup(page, 'html.parser')
    #     print soup
    #     all = soup.find_all('div', attrs={'class': 'item poster card'})
    #     for i in all:
    #         disc = i.find('p', attrs={'class': 'overview'}).text
    #         rating = i.find('div', attrs={'class': 'user_score_chart'})['data-percent']
    #         rating = float(rating) / 10
    #         movie = i.find('a', attrs={'class': 'title result'})
    #         date = datetime.strptime(movie.findNext('span').text.split(',')[1], " %Y")
    #         title = movie['title']
    #         pk = movie['id'].split('_')[1]
    #         Movie.objects.create(id=pk, title=title, discription=disc, released_year=date,
    #                              rating=rating)

    def scrap_movie_by_title(self, title):
        movie = MV()
        res = movie.search(title)
        for m in res:
            self.set_data(m)

    def scrap_movie_by_year(self, start, stop):
        discover = Discover()
        discover_params = dict()
        if start:
            gte_year = datetime.strptime(str(start), "%Y")
            discover_params['primary_release_date.gte'] = gte_year
        if stop:
            lte_year = datetime.strptime(str(stop), "%Y")
            discover_params['primary_release_date.lte'] = lte_year
        try:
            movie = discover.discover_movies(discover_params)
            for m in movie:
                self.set_data(m)
        except Exception as e:
            raise TMDbException("Connection error to imdb api server")

    def scrap_movie_by_rating(self, start, stop):
        discover = Discover()
        movie = discover.discover_movies({
            'vote_average.gte': start,
            'vote_average.lte': stop
        })
        for m in movie:
            self.set_data(m)

    def set_data(self, m):
        data = dict()
        data['id'] = m.id
        data['released_year'] = datetime.strptime(m.release_date.split('-')[0], "%Y") \
            if m.release_date else datetime.now()
        data['rating'] = m.vote_average if m.vote_average is not 0 else 10.0
        data['title'] = m.title
        data['discription'] = m.overview
        Movie.objects.get_or_create(**data)
