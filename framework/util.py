'''Utility methods'''
import json

from framework.data_classes import Location

def to_json(data_object):
    '''Serialize object to JSON'''
    return json.dumps(data_object, default=lambda o: o.__dict__)


def calculate_manhattan_distance(source: Location, destination: Location):
    '''Calculate manhattan distance between two locations'''
    return abs(destination.x - source.x) + abs(destination.y - source.y)
