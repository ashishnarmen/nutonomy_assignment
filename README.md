# Nutonomy QA Take Home Exercise - Taxi booking system

## How to execute tests 

### Using docker 

Run the following commands to execute the tests
```
docker build -t nutonomy_assignment .
docker run nutonomy_assignment
```
After test exectuion, if you want to remove the docker image that is created, run the commaond 
``` 
docker rmi nutonomy_assignment
```

### On local environment

#### MacOS
Install Python 3.8.3
``` 
python3 -m venv nutonomy_assignment
source nutonomy_assignment/bin/activate
pip3 install -r requirements.txt
python3 -m unittest -v
deactivate
```

#### Linux
Install Python 3.8.3
``` 
python -m venv nutonomy_assignment
source nutonomy_assignment/bin/activate
pip install -r requirements.txt
python -m unittest -v
deactivate
```

#### Windows
Install Python 3.8.3
``` 
python -m venv nutonomy_assignment 
nutonomy_assignment\Scripts\activate.bat
pip install -r requirements.txt
python -m unittest -v
deactivate
```



## Test structure 
The central idea behind using this structure is to separate the tests that will be executed and the framework that is used to interact with the REST API endpoints. The tests themselves are divided into different classes based on the aspects of the REST API that is getting verified. 

This approach minimizes the impact of minor changes to the REST API behavior on the tests themselves. Additionally, the test verfications are themselves modularized such that repeated verifications are not duplicated. 

### Framework

#### Booking 
Class to call Taxi booking REST API endpoints 

#### Constants
Store constants that are globally applicable across the tests. 

#### Data classes 
Data transfer objects to use in requests / responses.

#### Utils 
Utility methods to be used in tests and in the framework

### Tests 

## Tests 

### TestBookingWorkflow

#### test_taxis_are_set_to_default_zero_x_and_zero_y
Test that all taxis are defaulted to 0,0 in the grid. This is verified by verifying that the Manhattan distance to various destinations is the same as calculated from 0,0.

#### test_booking_flow_total_time_is_calculated_correctly
Test that the total time taken for a taxi is greater than the time that will be taken to traverse the Manhattan distance as the taxi will take additional time to reach the passenger.

#### test_taxi_is_available_after_the_time_to_drop_has_elapsed
Test that a taxi that is booked is able to complete its journey and is available for booking again. 

#### test_empty_response_as_null_is_returned_after_all_taxis_get_booked
Test that an empty response is returned after all the taxis are booked

#### test_tick_api_call
Test that the tick API call returns the correct HTTP status code


### TestAPICallsWithInvalidCustomHeader

#### test_booking_returns_error_with_invalid_header
Test to verify that the /v1/book returns an error when an invalid custom header is passed. 

#### test_reset_returns_error_with_invalid_header
Test to verify that the /v1/reset returns an error when an invalid custom header is passed. 

#### test_tick_returns_error_with_invalid_header
Test to verify that the /v1/tick returns an error when an invalid custom header is passed. 

### TestBookingAPICallsWithInvalidLocation

#### test_invalid_location_of_source_returns_internal_failure
Test that setting an invalid location for source returns an error

#### test_invalid_location_of_destination_returns_internal_failure
Test that setting an invalid location for destination returns an error


## Issues
* Specifying `content-type: application/json` causes an error for `PUT /v1/reset` and `POST /v1/tick`
* The following scenarios should have a JSON response 
  * `POST /v1/book`: When there are no taxis available for a booking, the text `null` is returned which is plain text and not JSON.  
  * `PUT /v1/reset`: The text `null` is returned
  * `POST /v1/tick`: The text `null` is returned
* Error responses should be more descriptive instead of `internal_failure` or `unauthorized` 
* There is no mechanism to check the current status of a specific car when it is en-route. 