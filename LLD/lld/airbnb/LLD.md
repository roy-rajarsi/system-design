# LLD of Airbnb

## Actors

* Hosts
* Renters
* Listings

## Api Design

### Listings

#### Listings CRUD Apis

1. Create Api - `POST /listing/` `Request Body: {state_id: int, city_id: int, date_available_from: datetime, price: float}`
2. Get Api - `GET /listing/<listing_id: int>`
3. Update Api - `PATCH /listing/<listing_id: int>` `Request Body : {date_available_from: datetime, price: float}`
4. Delete Api - `DELETE /listing/<listing_id: int>`

#### Search Listing Apis

1. Search Listing Api - `GET /listing?state='West Bengal'&city='Kolkata'&region='salt_lake'&tentative_booking_date=12/04/2024&price_start_range=3000&price_end_range=5000`

#### Book Listing Apis

1. Book Listing Api (HTTP but not REST Api) - `POST book_listing/` `Request Body: {listing_id: int, user_id: int, booking_from_date: datetime, booking_to_date: datetime}`


### QuadTree (Leader-Follower) Search Cluster (Separate gRpc Service)

1. Search Listing Api - `GET /listing?latitude=<region_latitude>&longitude=<region_longitude>&tentative_booking_date=12/04/2024&price_start_range=3000&price_end_range=5000`

## Object Oriented Design

### Functionality Flows

#### SearchListings Flow

    Request Object: SearchListingsRequest(city: str, region: str, tentative_booking_date: datetime, price_start_range: float, price_end_end_range: float)
    Response Object: SearchListingsResponse(listings: List[Listing])

* SearchListingsRequest -> CoordinatesEnrichmentHandler -> CoordinatesEnrichedSearchListingResponse / raises CityNotInDBException, RegionNotInDBException 
* CoordinatesEnrichedSearchListingResponse -> CoordinatesEnrichedSearchListingRequest -> RegionInCityValidationHandler -> RegionInCityValidatedResponse / raises RegionNotInCityException
* RegionInCityValidatedResponse -> RegionInCityValidatedRequest -> SearchObjectEnrichmentHandler -> SearchObjectEnrichedSearchListingResponse
* SearchObjectEnrichedSearchListingResponse -> SearchObjectEnrichedSearchListingRequest -> SearchListingsHandler -> SearchListingsResponse

##### Handlers

* **SearchObjectEnrichmentHandler**
  * SearchObjectEnrichmentHandler basically checks if the QuadTree Search Cluster hosts are active to search.
  * If yes, then, it adds in a `search_strategy` attribute in the request instance with a QuadTree gRpc stub instance, otherwise a simple object that performs a DB call.
      
* **SearchListingsHandler**:
  * The handler just calls the `search_strategy.search_listings()` and returns the response

#### BookListingFlow

    Request Object: BookListingRequest(listing_id: int, user_id: int, booking_from_date: datetime, booking_end_date: datetime, order_id, payment_id, payment_signature: str)
    Response Object: BookListingResponse(booked: bool, booking_id: int)

* BookListingRequest -> BookListingHandler -> BookListingResponse

##### Handlers

BookListingPaymentInfoEnrichedRequest -> PaymentValidationHandler -> BookListingPaymentValidatedResponse 
BookListingPaymentValidatedRequest -> BookListingHandler (Transaction) -> BookListingResponse

BookListingHandler
* Create a Transaction and lock the Listing instance
* Create an instance in the Booking Table













