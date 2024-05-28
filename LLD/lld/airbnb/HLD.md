# HLD of Airbnb

We have 3 major actors according to the problem - Hosts, Renters and Listings. It is better to have 3 separate services for each of these actors, the reason being separation of concerns.

Let's say, we want to run some DL algorithms on what is the typical time for renting in  a particular region. If we have one server, to get the Listings data, we have to hit the same server handling Hosts and Renters data as well, thereby increasing load on the server - why would requests for Hosts and Renters suffer due to some DL algorithm running for Listings ? The same argument can be applied to all other actors. Hence, its best to have separation of services handling the various actor details.

## Hosts Service

The Host Service handles CRUD Apis for Hosts. It contains a cluster of App servers, behind a Load Balancer. The Load Balancing Algorithm can be very simple Round Robin Load Balancing, as we do not have any inclination towards a specific App Server, as all these perform homogeneous task.

## Renters Service

The Renters Service handles CRUD Apis for Renters. Similar to the Hosts Service, it contains a cluster of App servers, behind a Load Balancer. The Load Balancing Algorithm, again, can be very simple Round Robin Load Balancing, as we do not have any inclination towards a specific App Server, as all these perform homogeneous task.

## Listing Service

The Listings Service handles requests from Hosts and Renters.

### Hosts Request

CRUD Request for Listings from Hosts

### Renters Request

* Renters would request for available properties in a region (or country as mentioned in the Question). Filters: Date Range and Price Range.

    Per country, we can have a DB cluster maintaining the information of the Listings. We can then index by Next Date Available and the by Price, in order to perform the search queries effectively.

    Number of listings is 1M per region. So, indexing by date is basically performing Binary Search on 1M entries - maximum queries we touch per query for finding the correct date available - log_2(10**6) = almost 20.
    For price, again for worst case (if all listings all valid for the date, so we have to filter from all 1M records) = almost 20.
    So, to give out result of one search we need to perform 40 touches on the records, which is pretty fast operation for any modern DBs.

    But, we can make this faster.
    
    ***QuadTree Search for faster query results***
    
    The actual requests will be something like this - Give me the nearby listings in Mahadevpura, from a specific date and within a specific price range.

    So, if we know we need to search for listings in Bangalore(Karnataka), why should be look into listings of Kolkata(WB) ?

    So, given a country, we'll have some cities where Airbnb will be active, and in some cities where Airbnb wont be active. For ex. Uber is active in Kolkata, but not in Berhampore.

    So, we can partition our data based on cities or index based on Cities - Bangalore, but then we can use a Quadtree to see the listings near a specific area ie. Mahadevpura - which will be blazing fast (although over-engineered). But, this QuadTree Search must return the list of listings based on the filters, as well, otherwise it does not make sense of the QuadTree Search returning a list of listings, where one or two listings are not valid, and we again have to filter them. Hence, we must mandatorily maintain these 2 attributes - `Date Available` and `Price` in the QuadTreeNodes, as well for effective filtering.
    
    We can have a cluster of Leader-Follower Servers, that stores an In-memory QuadTree of listings in a specific city. We must synchronously update the Leader Server, while we update the Listings DB, and then we can schedule jobs that synchronize the data between the leader and the followers. Synchronous Data Replication of the ListingsDB and the Leader Server is necessary, because we do not want our QuadTreeSearch return a Listing that is stale, for ex. a listing was updated to be not-available, but it did not get updated to the In-Memory QuadTree, due to Asynchronous Replication.

    If the Leader fails, a Follower will be appointed as a Leader. But what if the Leader had some data, and before the "Leader-Follower Synchronization Job" running, the Leader fails due to some reason, the Follower getting appointed as Leader, would not have these updates. Hence, how do we ensure consistency in Query Results ?

        -> For some interval, the ListingDB can be used as the data source to query, and hence the ListingDB should have proper indexing.

        -> The ideal way to solve this, could be to use the logs to sort of add in these missed updates to the new Leader.

    So, wrapping up, we can store all the Listings of a Country in a simple SQL DB cluster (we have just 1M listings in an area). We can index the listing based on City, then on Date Available and the on Price. If we see, we'll have Foreign Key relations, for instance, between the Listing Table and the City Table.

    Here's how our query will look like.
    Query the City Table for getting the Latitude and Longitude of the City, and then perform a QuadTree Search to get the nearest valid listings.
    In case of the Leader Server failing, till the new Leader is updated with the missed events, the ListingsDB can be used  as the data source to answer queries, and then once the new Leader is updated with the missing events, things can continue as normal.

* Renters' Booking Request

    Handling Booking Requests is a bit cryptic.
    Lets say, 2 renters - Renter1 and Renter2 clicked on "Book Now" of a particular listing, at 10:00 pm and 10:02 pm respectively. But due to faster internet, Renter2 could complete the payment and hence the booking by 10:04 pm. When Renter1 clicks on "Pay Now" at 10:05 pm, he/she, sees "This Listing is not Available". This is a very bad user experience.

    We can fix this, by locking. Whenever a Renter clicks on "Book Now" of the UI, a request must be send to the Listing App Server to lock the particular listing for lets say 10 mins. Within these 10 mins,
    
        -> Any other Renter, will see this listing to be `Unavailable` during these 10 mins.

        -> If the Renter comes out of the "Book UI", a request must be sent to release this lock. Otherwise, till the payment is done and the listing is booked in the name of the Renter, all these should be done in a transaction, and then the lock must be released.

### Apis

***Primary Exposed Apis***

* GET /listings/country_name/state="West Bengal"?city='Kolkata'&region="salt_lake"&tentative_booking_date=12/04/2024&price_start_range=3000&price_end_range=5000 (Currency should be present in Config files of the Applications)

* POST /book/ -> payload: {listing_id, user_id, booking_from_date, booking_to_date} - This will be a long running request, as we are dependent on an external payment service call. So, we can use an Async thread to handle it (ASGI in Django)

***Primary Consuming Apis***

* External Payment Api

* GET /listings/country_name/state="WestBengal"?region="salt_lake"&tentative_booking_date=12/04/2024&price_start_range=3000&price_end_range=5000 : from the Leader Server containing the in-memory QuadTree

## Leader-Follower Search Cluster

We'll usually use something like Zookeeper or EtcD to start off a Leader-Follower Server Cluster.

### Apis

***Exposed Apis***

* GET /listings/country_name/state="WestBengal"?region="salt_lake"&tentative_booking_date=12/04/2024&price_start_range=3000&price_end_range=5000 

Returns: JSON -> {available_listings: [{listing_id: 1, booked: false, .....}, {listing_id: 2, booked: false, .....}]}

## Capacity Estimations

    <TODO>

## Few observations

* Caching is usually done in almost any system. However, here as per the scope of the problem, we are only working on Searching and Booking. Now, Booking is something, which is purely action based, and hence no scope of caching. However, for Searching, usually we cache. But here Searching is something that cannot be done on stale data, which may arise in a Cache. Hence, given the scope of the problem, we do not require Caching.

* Why is Booking and Listing Service not decomposed into separate micro-services ?

We can, for sure - the reason being these fall in the same domain - Listing. But of-course, if the Booking System goes complex and we need to decompose these using the Strangler Design Pattern.

If we consider, the number of requests that come for Searching the Listings, is considerably higher than the number of actual bookings. Hence, of-course we can decompose these.

But currently our system has not gone that complex, and the Booking System, will make use of the Listing DB.

* The response for Search Listings must be paginated. We do not want to overwhelm a user with 50 listings in one page.

## Reference

* SystemsExpert : Design Airbnb -> https://www.algoexpert.io/systems/workspace/design-airbnb
