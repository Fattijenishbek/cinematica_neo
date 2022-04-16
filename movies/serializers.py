from django.utils import timezone

from django.core.exceptions import ValidationError

from rest_framework import serializers

from .models import (
    Cinemas,
    Movie,
    ShowTime,
    Rooms,
    RoomsFormat,
    MovieFormat,
)


class CinemasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cinemas
        fields = [
            'id',
            'name',
            'working_schedule',
            'location',
            'contacts',
        ]

    def validate(self, data):
        if data['contacts'][:3] != '996':
            raise ValidationError('Value should be 996 ')

        return data


class MovieFormatSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieFormat
        fields = "__all__"


class MovieSerializer(serializers.ModelSerializer):

    movie_status = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Movie
        fields = [
            'id',
            'name',
            'age_limit',
            'beginning_of_movie',
            'ending_of_movie',
            'movie_status',
        ]

    @staticmethod
    def get_movie_status(obj):

        now = timezone.now()

        if obj.beginning_of_movie <= now <= obj.ending_of_movie:
            obj.movie_status = 'current'
            return obj.movie_status

        if obj.beginning_of_movie > now:
            obj.movie_status = 'upcoming'
            return obj.movie_status


class ShowTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShowTime
        fields = [
            'id',
            'start_time',
            'end_time',
            'movie_format',
            'movie',
            'rooms',
        ]


class RoomsFormatSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomsFormat
        fields = [
            'id',
            'name',
            'price',
        ]


class RoomsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rooms
        fields = [
            'id',
            'name',
            'format',
            'cinemas',
        ]
