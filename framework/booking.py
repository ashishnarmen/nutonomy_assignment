'''Module to call Taxi booking REST API endpoints'''

import requests

from framework.data_classes import Location
from framework.util import to_json


class TaxiBooking:
    '''Class to call Taxi booking REST API endpoints'''
    base_url = ''
    x_fas_signature = ''
    book_url = '/v1/book'
    reset_url = '/v1/reset'
    tick_url = '/v1/tick'
    header = {}
    header_with_content_type = {}

    def __init__(self, base_url: str, x_fas_signature: str):
        self.base_url = base_url
        self.x_fas_signature = x_fas_signature
        self.header = {
            'x-fas-signature': self.x_fas_signature
        }
        self.header_with_content_type = {
            'x-fas-signature': self.x_fas_signature,
            'content-type': 'application/json'
        }

    def book(self, source: Location, destination: Location):
        '''Book a taxi ride'''
        url = self.base_url + self.book_url
        data = {
            'source': source,
            'destination': destination
        }
        return requests.post(
            url=url, headers=self.header_with_content_type,
            data=to_json(data), allow_redirects=True)

    def reset(self):
        '''Reset the Taxi booking system to defaults'''
        url = self.base_url + self.reset_url
        return requests.put(url=url, headers=self.header)

    def tick(self):
        '''Simulate the passage of one time unit'''
        url = self.base_url + self.tick_url
        return requests.post(url=url, headers=self.header)
