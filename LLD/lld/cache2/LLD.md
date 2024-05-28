# LLD Of Cache

## Actors

* Cache Cluster - Container for a group of Cache Servers - Distributed Cache Servers

* Cache Server (Individual Cache Server in the cache Cluster) - Contains In-memory KV "store***S***" for storing data - Contains a group of KV stores, representing the replicas as well.

* KV Store - KV Store should be 2 in-memory Data structures:
  * Hash Table -> For Reads, we would need `O(1) TC`.
  * TreeMap (BST) -> In Consistent Hashing, we require shifting of keys from one Cache Server to the other. Hence, it is very important, to get a list of keys in a specific numeric range, in the quickest time. Using a BST we can do this in `log_2(n) TC`.

* ThreadPool (Custom Thread Pool - As we want one particular thread to handle all requests for a key. In this way we can ensure Linearizability and hence Causal Consistency)

* Worker Threads (Threads in ThreadPool) - Worker Threads are basically responsible for CRUDs

* Daemon Threads - Daemon Threads are responsible for 2 aspects:
  * Regularly checking the TTL of Cache entries and invalidating the entries
  * Bulk Writes to the DB

## Request Flow

### Single Threaded Application

If we have a single-threaded application, that takes in input, processes the request and then returns the output, we cannot handle multiple requests at the same time, parallelly or concurrently. The single thread (main  thread), may rely on the external DB calls, and hence can be blocked. As long as the thread, does not complete the operation, it cannot handle other requests, despite sitting idle.

### Multi-Threaded Application - Input Thread and Worker Threads

We can have 2 threads:

* One input thread -> This thread will be responsible to take in input, and assign a request to the correct worker thread
* Worker Thread Pool -> These threads will be responsible for executing the requests

### Multi-Threaded Application - Input Thread, Worker Thread Assigner Thread and Worker Threads

There is no point of introducing asynchrony in the Input Thread. We will use the input thread to just take in console input and push it in a Request Queue. Input Thread is never blocked, hence we do not need asynchrony in here.

The Worker Thread Assigner Thread, will read from the Request Queue, and just map a request to the correct worker thread. Here, as well there is no blocking call (as the Request Queue is in-memory; if it were some external process, we could have thought about asynchrony).

Every Worker Thread will have its own Request Queue. Requests will be added to the Request Queue of a particular Worker Thread, by the Worker Thread Assigner Thread. The Worker Thread will take one request at a time from its Request Queue, and process it. This processing may require a DB call, which is a blocking call. Hence, we can introduce asynchrony.

When a Worker Thread is communicating with the DB, the thread is basically waiting; so can we introduce asynchrony in here ? Lets say, we introduce asynchrony in here. Lets say we get 2 requests - Write A(=10) to 100 and then Read A, after 1 minute. Now while writing 100 to A in the DB, the async task is waiting, so we can execute the async task for Read A. Now, due to some reason, the async thread for Read A gets processed by the DB first and responded to. So, we get Read A as 10, which violates our Read Your Write Guarantee.

### Async Approach [VERY COMPLICATED IMPLEMENTATION]

We can use Async approach, only if we run the entire application as async - async input and async request handling in one task. We can do that - but one thing we must keep in mind - context switch will occur only when there is an await in a task.

The implementation is a bit complicated, as input() is a synchronized blocking call. If we have an input() in a async task, the entire event loop is blocked, as this input() is not awaited, since this is not a co-routine. The way we can implement this, is we have to create a new thread in this async block and run the input() [blocking function] in that thread, so that we do not block the current thread.

More about this here -> https://superfastpython.com/asyncio-to_thread/#Run_Function_in_New_Thread_with_to_thread

## Response Flow

The individual worker threads can populate a Response Queue and we can have an Output Thread that can dequeue the Response Queue and print the Response, corresponding to a particular Request Id.

