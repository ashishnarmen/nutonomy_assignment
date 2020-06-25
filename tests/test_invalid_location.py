'''Tests to verify invalid location'''
import unittest

from framework.booking import TaxiBooking
from framework.constants import BASE_URL, X_FAS_HEADER
from framework.data_classes import ErrorResponse, Location


def get_invalid_locations():
    '''Method to generate a set of invalid locations'''
    invalid_values = [-2147483649, 2147483648]
    valid_value = 0
    invalid_locations = [
        Location(valid_value, invalid_values[0]),
        Location(valid_value, invalid_values[1]),
        Location(invalid_values[0], valid_value),
        Location(invalid_values[1], valid_value)
    ]
    return invalid_locations

class TestBookingAPICallsWithInvalidLocation(unittest.TestCase):
    '''Tests to verify invalid location'''
    taxi: TaxiBooking

    def setUp(self):
        self.taxi = TaxiBooking(
            base_url=BASE_URL, x_fas_signature=X_FAS_HEADER)
        self.taxi.reset()

    def test_invalid_location_of_source_returns_internal_failure(self):
        '''Test that setting an invalid location for source returns an error'''
        valid_value = 0
        sources = get_invalid_locations()
        destination = Location(valid_value, valid_value)
        for source in sources:
            booking_response_object = self.taxi.book(
                source=source, destination=destination)
            self.response_is_an_error(booking_response_object)

    def test_invalid_location_of_destination_returns_internal_failure(self):
        '''Test that setting an invalid location for destination returns an error'''
        valid_value = 0
        destinations = get_invalid_locations()
        source = Location(valid_value, valid_value)
        for destination in destinations:
            booking_response_object = self.taxi.book(
                source=source, destination=destination)
            self.response_is_an_error(booking_response_object)

    def response_is_an_error(self, response):
        '''Verify response status code and response content'''
        self.assertEqual(response.status_code, 500,
                         "Response status code is not 500 Internal Server Error")
        error_response = ErrorResponse(response.json())
        self.assertEqual(error_response.code.lower(
        ), "internal_failure", "Response -> code is not returned correctly")
        self.assertEqual(error_response.message.lower(
        ), "internal failure", "Response -> message is not returned correctly")
