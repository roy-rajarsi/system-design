# Netflix

## Video Storage

***(Storing Videos is the most important aspect; User Details, Subscription, Payment etc are also significant, but not in current scope)***

Storage of videos, will be a very crucial part of designing Netflix. At this point we would need information about an average number of videos, that Netflix stores in its DB. Also, to estimate the storage, we would need how long are the videos, what is the resolution (length * breadth) of the videos.

We obtain from the question, that on an average Netflix stores 10k videos, 1 hour long each and each video is stored in 2 resolutions - SD and HD.

So, 1 SD video, that is 1 hour long is of approximately 10 GB, and 1 HD video, that is 1 hour long is of approximately 20GB.

So, raw storage needed to store all 10K videos = (10K * 10 + 10K * 20) GB = 30 * 10K GB = **300 TB** (1 TB = almost 1k GB).

Now, this size of videos is not very large, compared to Youtube, where anyone can upload videos at any time. Here, only a few production houses are allowed to publish videos. So, we need not go for video compression or anything fancy. We can simply use a Blob Data Storage like Amazon S3, to store the videos. Of-course, we will partition the videos, into multiple S3 Buckets. It is okay to replicate the videos, but replicas aren't too significant here, since S3 guarantees durability, so two to three replicas, per bucket will suffice.

Now lets consider, a video got published now, and become very popular. But this video, wont be very relevant, in lets say 20 years. So, we can store videos, that are (lets say), 20-25 years old, into Amazon S3 Glacier. If that video is requested by some client, we can ask the client to wait for sometime, and come back in an hour or so, within which we retrieve the video from the Glacier format back to its original format, and then serve it.

Now, a video, will be associated with some meta-data, as well - `title`, `description`, `production_house_id`, `cast_details`, `date_and_time_posted`, `video_thumbnail_url`, `video_url`. (Video Thumbnail image can be stored in S3 as well, and will lead to insignificant amount of storage increment, when compared to the actual video storage, so this can be neglected for storage estimation)

So, we have to associate  these meta-data as well. These meta-data can be well easily added into a SQL Database, as we have relations to store - `production_house_id`, and also storing this data do not need anything fancy.

* Title -> 100 words. Each word has an average of 10 characters. Each character takes 1 byte. Storage = 100 * 10 * 1 byte = 1000 bytes = 1 kB

* Production House Id -> 16 characters UUID. So storage needed = 16 * 1 byte = 16 bytes = 20 bytes (almost)

* Cast Details -> 1000 words. So storage needed = 1000 * 10 * 1 byte = 10 kB

* Date and Time Details -> 20 characters(almost) = 20 * 1 byte = 20 bytes

* Urls -> 200 characters = 200 * 1 bytes = 200 bytes

Storage needed to store the video metadata = 100 kB (max 100 kilo-bytes) * 10K = 1000K kB = 1K MB = 1 GB

So, summing up, we'll store the videos and the video thumbnails in Blob Storage like S3, with a 2 replicas, and we can store the video meta-data in a SQL DB. We'll need an approx of 300 TB of storage to store videos, and with replication and storing these minute extras, we can estimate our video storage to take around 600 TB.

## Video Streaming - HLS with Adaptive Bitrate

Of-course, video streaming is going to be primary task of Netflix. We have to always keep in mind of the peak traffic to serve, and the bandwidth we consume. Whenever a new movie comes out and it is rightly promoted, we have a huge load come in.

So, lets try to perform the Peak Traffic Estimation and Bandwidth Estimation, while streaming videos.

Here's where we'll need the DAU. So, DAU is 200 M, and at peek we except all 200 M users, requesting to get the video.
Lets consider, 10 % of 200M users request for a certain video in a time duration of 1s. So Read RPS = 20M Rps. (Write Request is very insignificant, as in Netflix almost 99 % requests will be for watching a video)

Now what geographical location is this 20M requests coming from. Is it local to a country or continent or global ? We have a Global Audience.

***How do we distribute an HD video to a Global Audience ?***

Distribution of video should be very efficient. It should not be like, users are waiting for a 20 GB HD video to be downloaded, and then users getting to watch the video. Rather, we should stream the videos. We should stream the video to the user's device, so that user's device can download and at the same play small bits of videos at a time. For streaming, the protocol we can use is ***HLS - Http Live Streaming***. HLS has a very unique feature, called ***Adaptive Bitrate***, that basically allows to reduce or increase the quality of the video, depending on the strength of the network. *(Details of HLS are in Notes) !*

Now, that we have decided on the protocol, to use, lets estimate the bandwidth needed to stream a 20 GB HD video, to 20M users. HLS, sends 6s video chunks at a time.

1 hr video -> 20GB (1 hr = 86400s = 10**5 s)
6s video -> (20 * 6) / (10**5) GB = 1200 kB
Per second, per request we have to transmit = 1200 kB
Per second for 20M requests we have to transmit = 20 * (10**6) * 1200 kB = 24 TB

Bandwidth to transmit per second is 24 TB/s

But per request we have to transmit 1.2 MB/s, which is pretty decent and can be handled, especially considering this is a video transfer. Usually the personal internet connections that we use provide somewhere between 40 Mb/s - 50 Mb/s download bandwidth. Note the "b" is small, and hence it is 40 MegaBits/s. And we need 1.2 MegaBytes/s = 12 Megabits/s (1 byte = 8 bits = almost 10 bits). So, this is very feasible.

Now, of-course if bandwidth of the network is a bit less, then yeah we have adaptive bitrate, which can query for a lower resolution of video, thereby having a theoretically buffer free experience.

### CDNs - AWS Cloudfront

How we will have multiple app-servers to handle these requests. But considering this is video streaming, and videos are static content, to share static content, even faster we can use CDNs.

If an Indian user wants to see a movie, it has to send request and wait for response from an app server in US. Of-course the distance is huge, and hence despite having good network, the request-response cycle will have good latency. To reduce the latency, we can use CDN services like AWS Cloudfront, and keep the relevant videos in the CDN Edge Locations (Edge Servers).

So, once a production house uploads a video to our app server, we can take an hour or two to upload the video, into the Edge Location of AWS Cloudfront, across the world. Hence, users are waiting for these 2 hours, unknowingly, but when they start watching the video, they get the video from a Edge Location with minimum latency, and hence gets a very fast download and watching experience.

## Recommendation Engine

We need not build the recommendation engine. However, we need to provide it the data it needs. So, of-course, lets try to estimate what data a recommendation engine might need.

The recommendation engine, will be responsible for recommending new videos to users. And for doing that a recommendation engine needs to know, what videos a user has watched, how much of a video a user has watched, at which part of the video the user clicked, may be see the portion again, which videos a user has liked, what rating a user has given to a video, and things like this.

So, all these boils down to the fact that we have to record some generic aspects about the user behaviour, on each video. So, if we formalize this, per user and per video, what we need to capture is:

* video_watched_by_this_user: bool
* last_watch_timestamp_of_the_video: timestamp
* liked: bool
* rating: int
* comment: str
* clicks: List[timestamp] or rather granular logs

Now, per user per video this data can take a maximum of 500 kB.

Now, on an average a person watches 2 videos or movies per week on Netflix. So, that is watching 2 * 50 = 100 videos in a year (1 year = 52 weeks = almost 50 weeks)

We have 200 M users, and we have to store and process 200M * 100 videos = 20000M sets of KV Pairs

So we have to store 2M * (10 ** 4) * 500 kB = 10 * PB data and process it. This is huge data, and must be stored into horizontally scalable machines. What do we use, when we have huge data and we need to process it frequently ? First we distribute this data across multiple machines and then we use MapReduce.

So, we can distribute this data into lets say 10 machines, each storing 1PB each. Now in order to determine, what `map()`, `shuffle()` and `reduce()` function, lets think what does the Recommendation Engine need ? The Recommendation Engine may need inputs in this format `<user_id, video_id, event_type>`, example `<user_id_1,video_id_2, 0>`, `<user_id_2, video_id_1, 1>` (Lets say 0 and 1 refers to Pause and Play, something like this).

So, here's how we can design our MapReduce functions. Now, one thing to keep in mind, is each of these 10 machines, holding 1 PB data each, can contain logs from various users.

Logs are basically like : `10:30 User1 Paused Video1 at 5:32`

* `map()` can be to parse this data and generate some Json like 
`{'user_id': '1', 'video_id': '1', event_type: 'PAUSED', 'event_timestamp': '5:32'}`
`{'user_id': '2', 'video_id': '1', event_type: 'PLAYED', 'event_timestamp': '15:32'}`

* `shuffle()` can be to segregate these data based on user_id

* `reduce()` can be to transform this data to make it Machine Learning Input compliant, like assigning label to the `PAUSED` and `PLAY` event types to `0` and `1`

Of-course, we wont implement MapReduce, but we'll use a Distributed File System Solution like Apache Hadoop Distributed File System (HDFS) or Google File System (GFS)
