# Cache

## Functional Requirements

* ***C***reate {key: value} pairs in Cache
* ***R***ead value for a particular key from Cache
* ***U***pdate value for a particular key in Cache
* ***D***elete a key from Cache
* Write to a Database Service - (Write Through Cache and Write Back Cache Writing Patterns) - Data Models in Cache and DB will be same(Guaranteed)
* Cache Reconstruction in case of Cache Server going down
* Hot-loading the Cache: The Cache, can store certain keys during startup, which it can load from the  DB, which will be accessed very frequently
* Request Coalescing: If the Cache receives a bunch of read request for the same key(lets say 3 requests in 1s), instead of querying the DB, multiple times(thrice, in this case), we should request once, and return the same response for all 3 requests.

## Non Functional Requirements

* **Availability** : We want high Availability of the Cache system. Hence, we must have replicas of our Cache servers.

* **Consistency and Latency** :
  * ***Strong Consistency and High Latency*** : Guaranteeing Strong Consistency, will mandate synchronous writes to all replicas of the Cache System. We can apply Strong Consistency if we use a ***Write Through Cache Writing Strategy***. Write Through Cache is used along with Read Through Cache strategy, and is used in Read Heavy Systems. We can afford the additional latency, of writing to replica Cache and DB, for the minimal amount of writes.

  * ***Eventual Consistency and Low Latency***: Guaranteeing Eventual Consistency, does allow asynchronous writes, to the replicas and to the DB, and is used primarily in Write Heavy Systems, that need low latency. We can use this, when we choose a ***Write Back Cache Writing Strategy***.

* **Scalability** : Our Cache system must be scalable for increasing and decreasing traffic.

* Update on Cache, can be accomplished by just invalidating the Cache entry, and just sending a write request to Db(If Cache interacts with the Db). For the next read, there will be a Cache insertion for the key, and hence is getting updated. However, this is a naive approach, if we want to avoid the heavy lifting during the update operation in LFU and LRU caches.

* Deletion of key from Cache is be done during 2 instances:
  * Cache Invalidation:
    * Cache entry timeout {key: value} pair timed-out
    * Update on a key in Cache
  * Cache Eviction:
    * Cache is full; hence one {key-value} pair must be evicted from the Cache

## Solution

Functional Requirements basically say, that we need to perform CRUD on a Dictionary. However, seeing the Non-Functional Requirements, we see a few aspects:

### Scalability

How can we ensure Scalability in true sense ? **Horizontal Scaling - Scaling Out: Sharding the Cache Server**

We must distribute the big Dictionary into multiple small Dictionary instances, thereby using Distributed Hashing. Now, as we know we must use Consistent Hashing, to know which Dictionary (or rather Cache Server instances in real life) holds what data, how to drop Cache instances and spawn up new instances.

### Availability and Fault Tolerance

We must create multiple replica instances for each Cache Server, in order to ensure Fault Tolerance.

### Consistency

We multiple replicas of each Cache Server. We need to propagate updates to all these replicas and also to the DB.

#### ***Writing to Cache Replicas***

How can we ensure a Strong Consistency Guarantee, with Low Latency?

If we think carefully, any `read(B)` is not reliant on any `write(A)`. So, why not order requests for the same key and ensure ***Causal Consistency*** ? This ensures **ordered** writing to a Cache Server.

Now each Cache Server is comprised of multiple replicas. If a `write(A) = 10` does not propagate to Cache Replica 4, and a read request of `read(A)` comes to Cache Replica 4, Cache Replica 4 will return a stale value of A, and hence we are again moving to the realm of Eventual Consistency. How can we ensure a Strong Consistency in here ? We can use the Quorum Consistency Model to do that (R + W > N). We should choose a good value for R and W depending on whether our system is Read-Heavy or Write-Heavy.

#### Writing to DB

Should we follow a Synchronous or an Asynchronous approach for writing to DB, relies on the type of the application, we are caching for. We can take an estimate from the user, when he/she creates a Cache Cluster instance, and then we can choose our ways.

Writing Asynchronously to Cache, can include patterns like:

* Write to DB, during Cache Invalidation, due to TTL or during Cache Eviction
* An Event based writing strategy can be used to send a write request to the DB, for a key that is updated more than a given constant number of times.
* Batch jobs writing in bulks to DB -> Low Data Persistance, but easier to implement.

### Cache Reconstruction

If the Cache Server, goes down to due to some reason, the data stored in Cache is lost forever.
We must come up with an idea to re-construct the Cache. Two very popular approaches are:

* Storing Snapshot of Cache at regular intervals - We store Cache Snapshot at regular intervals.
* Re-constructing Cache using Logs - We look at the operation logs on Cache, and use that to re-construct the Cache.

Re-constructing the Cache, using Operation Logs, is a better way of Cache Reconstruction. We may be taking snapshots of the Cache at an interval of 5 mins. Now lets say, the last snapshot was taken at 9:55pm, and before taking snapshot at 10pm, many requests came, but the Cache server crashed at 9:58. So, all these new cache data, was not stored in any snapshot, but was stored in logs. Hence, this is a better way of Cache Reconstruction

## References

* Gaurav Sen Cache Machine Coding
* Redis System Design -> https://www.youtube.com/watch?v=DUbEgNw-F9c&t=1431s
