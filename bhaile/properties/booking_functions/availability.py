import datetime
from properties.models import Post, Booking


def check_availability(accommodation, move_in, move_out):
    avail_list = []
    booking_list = Booking.objects.filter(accommodation=accommodation)
    for booking in booking_list:
        if booking.move_in > move_out or booking.move_out < move_in:
            avail_list.append(True)
        else:
            avail_list.append(False)
    return all(avail_list)