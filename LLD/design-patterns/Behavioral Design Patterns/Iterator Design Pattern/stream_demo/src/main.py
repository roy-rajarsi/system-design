from threading import Thread
from time import sleep
from stream import Stream, StreamIterator


def push_numbers_to_stream(stream: Stream) -> None:
    element: int = 0
    while element <= 25:
        stream.push_to_stream(element=element)
        element += 1
        sleep(1)


def display_numbers_in_stream(stream: Stream) -> None:
    stream_iterator: StreamIterator = iter(stream)
    while True:
        try:
            print(next(stream_iterator))
            sleep(3)
        except StopIteration:
            print(f'StopIteration Raised on -> {stream.get_queue()} Sleeping for 10s')
            sleep(10)
            continue


def main() -> None:
    stream: Stream = Stream()
    stream_push_thread: Thread = Thread(name='StreamFastPushThread',
                                        kwargs={'stream': stream},
                                        target=push_numbers_to_stream)
    stream_display_thread: Thread = Thread(name='StreamSlowDisplayThread',
                                           kwargs={'stream': stream},
                                           target=display_numbers_in_stream)
    stream_push_thread.start()
    stream_display_thread.start()
    stream_push_thread.join()
    stream_display_thread.join()


if __name__ == '__main__':
    main()
