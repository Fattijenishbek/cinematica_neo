from django.db import models
from django.utils import timezone


class Cinemas(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    working_schedule = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    contacts = models.CharField(max_length=255, blank=True, null=True)


class Movie(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    age_limit = models.IntegerField(blank=True, null=True)
    beginning_of_movie = models.DateTimeField(default=timezone.now)
    ending_of_movie = models.DateField(auto_now=False, blank=True, null=True)


class RoomsFormat(models.Model):
    name = models.CharField(max_length=255)
    price = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name


class Rooms(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    format = models.ForeignKey(RoomsFormat, on_delete=models.CASCADE)
    cinemas = models.ForeignKey(Cinemas, on_delete=models.CASCADE)


class MovieFormat(models.Model):
    name = models.CharField(max_length=255)
    price = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name


class ShowTime(models.Model):
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(auto_now=False, blank=True, null=True)
    movie_format = models.ForeignKey(MovieFormat, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rooms = models.ForeignKey(Rooms, on_delete=models.CASCADE)
