from rest_framework import serializers
from decimal import Decimal


from .models import (
    Tickets,
    Orders,
    Booking,
    Feedback,
    Seats,
    ClubCard,
    TicketType,
)


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tickets
        fields = [
            'id',
            'ticket_type',
            'seats',
            'user',
            'orders',
            'show_time',
            'price',
            'payment_methods',
            'club_card',
        ]
        read_only_fields = ["price"]

    def validate(self, data):
        seats = data.get('seats')
        show_time = data.get('show_time')
        if Booking.objects.filter(seats=seats, show_time=show_time).exists():

            raise serializers.ValidationError('This seat is already reserved.')

        return data


class OrdersSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField('get_total_price')

    class Meta:
        model = Orders
        fields = [
            'id',
            'user',
            'total_price',
        ]

    @staticmethod
    def get_total_price(obj):
        tickets = Tickets.objects.filter(orders=obj.id)
        card = ClubCard.objects.filter(user=obj.user)
        print(card)
        total_price = 0
        for ticket in tickets:
            for cards in card:
                if cards.discount == 7:
                    total_price += (ticket.price - ((ticket.price*cards.discount)//100))
                total_price += ticket.price
        return total_price


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = [
            'id',
            'title',
            'content',
            'rate',
            'user',
        ]


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            'id',
            'show_time',
            'seats',
            'user',
        ]

    def validate(self, data):
        seats = data.get('seats')
        show_time = data.get('show_time')
        if Booking.objects.filter(seats=seats, show_time=show_time).exists():

            raise serializers.ValidationError('This is already reserved.')

        return data


class SeatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seats
        fields = [
            'id',
            'number_of_seat',
            'number_of_row',
            'rooms',
        ]


class ClubCardSerializer(serializers.ModelSerializer):
    balance = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ClubCard
        fields = [
            'id',
            'balance',
            'discount',
            'user',
        ]

    def get_balance(self, obj):
        orders = Tickets.objects.filter(users=obj.user)
        balance = 0
        for i in orders:
            balance += i.price
            if balance > 10000:
                obj.discount = 3
            if balance > 15000:
                obj.discount = 5
            if balance > 20000:
                obj.discount = 7
        return balance


class TicketTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketType
        fields = [
            'id',
            'name',
            'price',
        ]
