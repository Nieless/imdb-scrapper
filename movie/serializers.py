from rest_framework import serializers

from movie.models import Movie


class MovieSerializer(serializers.ModelSerializer):
    genre = serializers.SerializerMethodField()

    def get_genre(self, instance):
        genre = []
        a = instance.genre.get_queryset()
        for i in a:
            genre.append(i.title)
        return genre

    class Meta:
        model = Movie
        exclude = []
