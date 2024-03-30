from flask import Blueprint, jsonify, session, request
from app.models import db, Booking, Tour, City
from app.forms import BookingForm
from flask_login import current_user, login_required
from .auth_routes import validation_errors_to_error_messages
import datetime

booking_routes = Blueprint("bookings", __name__)


@booking_routes.route("/")
def get_all_bookings():
    bookings = Booking.query.all()
    bookings_data = []
    for booking in bookings:
        # tour_id = booking.tour_id
        # tour = Tour.query.get_or_404(tour_id)
        booking_dict = booking.to_dict()

        # print(tour_id)
        # print(tour.id)
        # booking_dict["tour_title"] = tour.title
        # # to convert to string use strftime
        # date_format = '%Y-%m-%d'
        # if not isinstance(booking.date, str):
        #     date = (booking.date).strftime(date_format)
        # else: date = booking.date
        # time_format = '%H:%M:%S'
        # start_time = (booking.start_time).strftime(time_format)
        # # to convert to datetime.date.fromisoformat(start_time)
        # booking_date = datetime.date.fromisoformat(booking.date)

        today = datetime.datetime.today()
        booking_date = datetime.datetime.strptime(booking.date, "%A, %B %d, %Y")
        # booking_date = datetime.datetime.combine(datbooking.date, datetime.time(0, 0, 0))
        diff = (booking_date - today).days
        occured = False
        if diff <= 0:
            occured = True
        booking_dict["completed"] = occured

        # booking_dict['start_time'] = start_time
        # booking_dict['date'] = date
        # tour_guide = booking.tour_guide
        # print(tour_guide)
        # tourguide_arr = []
        # tourguide_arr.append(tour_guide)

        # booking_dict['tour'] = tourguide_arr

        bookings_data.append(booking_dict)
    # return jsonify(bookings_data)
    return {"bookings": {booking["id"]: booking for booking in bookings_data}}
