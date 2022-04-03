import requests

from pprint import pprint


BASE_RES_URL = (
    'https://8hj75wczi6'
    '.execute-api.ap-southeast-1.amazonaws.com'
    '/default{}'
)


def send_email_alert(to_email, message):
    subject = '[AC2E EMAIL NOTIF] CRITICAL ERROR ALERT'
    url = BASE_RES_URL.format('/ac2e_email_sender_service')
    res = requests.post(url, json={
        'to': to_email,
        'subject': subject,
        'body': message,
    })
    try:
        res.raise_for_status()
    except Exception as err:
        breakpoint()
    return res.json()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        'to_email',
        help='Valid to email.',
    )
    parser.add_argument(
        'message',
        help='Email message',
    )
    args = parser.parse_args()

    res = send_email_alert(args.to_email, args.message)
    pprint(res)
