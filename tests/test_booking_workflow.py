'''Tests to verify booking workflow'''
import unittest

from framework.booking import TaxiBooking
from framework.constants import (BASE_URL, SPEED,
                                 NO_OF_TAXIS, X_FAS_HEADER)
from framework.data_classes import BookingResponse, Location
from framework.util import calculate_manhattan_distance


def book_all_taxis_in_system(taxi):
    '''Book all the taxis in the system '''
    booking_ctr = 0
    booked_car_ids = []
    source = Location(x=1, y=2)
    destination = Location(x=3, y=4)
    while booking_ctr < NO_OF_TAXIS:
        booking_response_obj = taxi.book(source, destination)
        booking_response = BookingResponse(booking_response_obj.json())
        booked_car_ids.append(booking_response.car_id)
        booking_ctr += 1
    return booked_car_ids

class TestBookingWorkflow(unittest.TestCase):
    '''Tests to verify booking workflow'''

    def initialize_and_reset(self):
        '''Initialize a taxi booking object and reset the state of all taxis'''
        taxi = TaxiBooking(base_url=BASE_URL, x_fas_signature=X_FAS_HEADER)
        self.validate_reset_api_call(taxi)
        return taxi

    def test_taxis_are_set_to_default_zero_x_and_zero_y(self):
        '''
        Test that all taxis are defaulted to 0,0 in the grid
        This is verified by verifying that the Manhattan distance to various
        destinations is calculated from 0,0
        '''
        taxi = self.initialize_and_reset()
        source = Location(x=0, y=0)
        destinations = [Location(x=0, y=2), Location(
            x=-2, y=0), Location(x=0, y=-2)]
        for destination in destinations:
            booking_response_obj = taxi.book(
                source=source, destination=destination)
            booking_response = BookingResponse(booking_response_obj.json())
            expected_distance = calculate_manhattan_distance(
                source=source, destination=destination)
            expected_time = int(expected_distance / SPEED)
            self.assertEqual(booking_response.total_time,
                             expected_time, "Time taken is calculated correctly")

    def test_booking_flow_total_time_is_calculated_correctly(self):
        '''
        Test that the total time taken for a taxi is greater than the
        time that will be taken to traverse the Manhattan distance as
        the taxi will take additional time to reach the passenger
        '''
        taxi = self.initialize_and_reset()

        source = Location(x=1, y=2)
        destination = Location(x=3, y=4)
        expected_distance_minimum = calculate_manhattan_distance(
            source, destination)
        expected_time_minimum = int(expected_distance_minimum / SPEED)
        booking_response_obj = taxi.book(source, destination)
        self.response_is_successful(booking_response_obj)
        booking_response = BookingResponse(booking_response_obj.json())

        self.assertGreater(
            booking_response.total_time, expected_time_minimum)

    def test_taxi_is_available_after_the_time_to_drop_has_elapsed(self):
        '''
        Test that a taxi that is booked is able to complete its journey
        and is available for booking again
        '''
        taxi = self.initialize_and_reset()

        # Book a taxi for a passenger
        source = Location(x=1, y=2)
        destination = Location(x=3, y=4)
        booking_response_obj = taxi.book(source, destination)
        booking_response = BookingResponse(booking_response_obj.json())

        # Simulate the completion of the taxi ride by simulating ticks in the system
        ticks = 0
        while ticks < booking_response.total_time:
            taxi.tick()
            ticks += 1

        # Verify that all taxis are available and can be booked
        booked_car_ids = book_all_taxis_in_system(taxi)
        self.assertEqual(len(booked_car_ids), NO_OF_TAXIS,
                         "All the cabs were not available for booking")

    def test_empty_response_as_null_is_returned_after_all_taxis_get_booked(self):
        '''Test that an empty response is returned after all the taxis are booked'''
        taxi = self.initialize_and_reset()
        booked_car_ids = book_all_taxis_in_system(taxi)
        self.assertTrue(sorted(booked_car_ids),
                        "Service does not return taxi with lowest id")
        source = Location(x=1, y=2)
        destination = Location(x=3, y=4)
        booking_response_obj = taxi.book(source, destination)
        self.response_is_successful(booking_response_obj)
        self.response_is_empty_with_text_as_null(booking_response_obj)

    def validate_reset_api_call(self, taxi):
        '''Verify that the reset API call returns the correct HTTP status code'''
        reset_response_obj = taxi.reset()
        self.response_is_successful(reset_response_obj)
        self.response_is_empty_with_text_as_null(reset_response_obj)

    def test_tick_api_call(self):
        '''Test that the tick API call returns the correct HTTP status code'''
        taxi = TaxiBooking(base_url=BASE_URL, x_fas_signature=X_FAS_HEADER)
        tick_response_obj = taxi.tick()
        self.response_is_successful(tick_response_obj)
        self.response_is_empty_with_text_as_null(tick_response_obj)

    def response_is_successful(self, response):
        '''Verify that response is HTTP 200'''
        self.assertIsNotNone(response, "Response is null")
        self.assertEqual(response.status_code, 200,
                         "Response is not successful")

    def response_is_empty_with_text_as_null(self, response):
        '''Verify that response is empty and contains text stating null'''
        self.assertEqual(response.text, 'null',
                         "Response text is not set as null")
