from threading import Thread

from email_service.email_service_proxy import EmailServiceProxy


email_sent: bool = False


def callback() -> None:
    global email_sent
    email_sent = True


def client() -> None:
    global email_sent
    EmailServiceProxy.send_email(sender_email_address='sender@abc.com',
                                 receiver_email_address='receiver@abc.com',
                                 email_payload={'body': 'Hello'},
                                 callback=callback)
    while not email_sent:
        continue
    print('Terminating...')


if __name__ == '__main__':
    client()
