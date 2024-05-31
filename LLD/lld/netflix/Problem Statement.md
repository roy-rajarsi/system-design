# Problem Statement

* We are designing the core Netflix service - basically how do we serve various videos to user
* The auxiliary functionalities - AuthN and AuthZ, Payments, Subscriptions, etc is not something that we are looking forward to design
* However, we need to store some form of user activity data, that helps Netflix recommend videos to its user. We need not design a Recommendation Engine, but we need to store and manage the data which will be consumed by the Recommendation Engine, in the background asynchronously.

## To Ask, while solving

* Count of Videos Netflix Stores -> 10k videos
* Videos are on an average 1hr long
* Videos are stored in Standard Definition and High Definition.

* DAU -> 200 M
* User-base is Global
