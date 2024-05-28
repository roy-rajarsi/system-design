# Design a Cab Booking Service

# Requirements
* Users - Riders and Drivers should be able to request a ride
* The System must handle Driver Selection for a particular ride request and calculate corresponding pricing associated with the trip

## Details

### Ride
Rides or Trips are bound within a specific city and no ride-sharing aspect is involved

### Ride Request
Ride Request can be initiated by either a Rider or Driver
* Ride Request by Rider is a ride request for a trip from Point A to Point B
* Ride Request by Driver is a ride request starting from a specific region

### Driver Selection Strategy
Based on the city in which rides are requested, we may have the following Driver Selection Strategies:
* Town : Nearest few drivers to be matched
* City : Nearest few drivers to be matched -> Preferred in the order of the drivers having less trips on top
* Metro City : Nearest few drivers to be matched -> Preferred in the order of the drivers having less trips on top -> Sorted based on Driver rating

### Pricing Strategy:
* Basic Pricing Strategy : Price per kilometer fixed for Town, City and Metro City
* Price Increment : For highly-rated drivers (4 -> 5) : may be 10% increment
* Price Discount : For highly-rated riders (4 -> 5) : may be 5% discount

