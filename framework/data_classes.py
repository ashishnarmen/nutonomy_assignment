'''Data Transfer Objects'''

from dataclasses import dataclass


@dataclass
class Location:
    '''Class for keeping track of the location of a car.'''
    x: int
    y: int


@dataclass
class BookingResponse:
    '''Class for tracking the booking details'''
    car_id: int
    state: str
    total_time: int

    def __init__(self, json_object):
        self.car_id = json_object['car_id']
        self.state = json_object['state']
        self.total_time = json_object['total_time']


@dataclass
class ErrorResponse:
    '''Class for recording errors'''
    code: str
    message: str

    def __init__(self, json_object):
        self.code = json_object['code']
        self.message = json_object['message']
