'''Tests to verify invalid custom header'''
import unittest

from framework.booking import TaxiBooking
from framework.constants import BASE_URL
from framework.data_classes import ErrorResponse, Location


class TestAPICallsWithInvalidCustomHeader(unittest.TestCase):
    '''Tests to verify invalid custom header'''
    taxi: TaxiBooking

    def setUp(self):
        self.taxi = TaxiBooking(
            base_url=BASE_URL, x_fas_signature="invalid_signature")

    def test_booking_returns_error_with_invalid_header(self):
        '''Test to verify that the /v1/book returns an error'''
        source = Location(x=1, y=2)
        destination = Location(x=3, y=4)
        booking_response = self.taxi.book(
            source=source, destination=destination)
        self.response_is_unauthorized(booking_response)

    def test_reset_returns_error_with_invalid_header(self):
        '''Test to verify that the /v1/reset returns an error'''
        reset_response = self.taxi.reset()
        self.response_is_unauthorized(reset_response)

    def test_tick_returns_error_with_invalid_header(self):
        '''Test to verify that the /v1/tick returns an error'''
        tick_response = self.taxi.tick()
        self.response_is_unauthorized(tick_response)

    def response_is_unauthorized(self, response):
        '''Verify the response status code and the response content'''
        self.assertEqual(response.status_code, 401,
                         "Response status code is not 401 Unauthorized")
        error_response = ErrorResponse(response.json())
        self.assertEqual(error_response.code.lower(), "unauthorized",
                         "Response -> code is not returned correctly")
        self.assertEqual(error_response.message.lower(
        ), "unauthorized", "Response -> message is not returned correctly")
