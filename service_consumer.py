"""Service Consumer

Sample:

https://vedj2c3e62.execute-api.ap-southeast-1.amazonaws.com/default/ac2e_email_notif_service

"""
import requests
import json

from pprint import pprint as print
from time import sleep

_http = requests.Session()
APP_NAME = 'service_consumer'

DEFAULT_REQUEST = 'post'

KEY_LOG_LVL = 'log_level'
KEY_MSG = 'message'
KEY_DTLS = 'details'
KEY_SRC_APP = 'source_application'


def log_api(svc_url, level, msg):
    requests.post(svc_url, json={
        'application_name': APP_NAME,
        'level': level,
        'log_message': msg,
    })


def log_event(
    url, level, message, details=None,
    request_type=DEFAULT_REQUEST,
    extra_data=None,
    use_post_data=False,
    key_log_lvl=KEY_LOG_LVL,
    key_msg=KEY_MSG,
    key_dtls=KEY_DTLS,
    key_src_app=KEY_SRC_APP,
    source=APP_NAME,
):
    data = {
        key_log_lvl: level,
        key_msg: message,
        key_dtls: details or '',
        key_src_app: source,
    }
    if isinstance(extra_data, dict):
        data.update(extra_data)

    # print('Data -> {}'.format(data))

    r_key = 'json' if request_type.lower() == 'post' else 'params'

    if use_post_data:
        r_args = (url, json.dumps(data),)
        r_kwargs = {
            'headers': {'Content-type': 'application/json'},
        }
    else:
        r_args = (url,)
        r_kwargs = {
            r_key: data,
        }

    # print('Request args -> {}'.format(r_args))
    # print('Request kwargs -> {}'.format(r_kwargs))

    res = getattr(_http, request_type)(*r_args, **r_kwargs)
    # from IPython import embed; embed()
    res.raise_for_status()

    try:
        return res.json()
    except json.decoder.JSONDecodeError:
        return res.text


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        'service_url',
        help='Logging service API Gateway URL',
    )
    parser.add_argument(
        'log_level',
        nargs='*',
        choices='info warning error critical debug'.split(),
        help='Log level (i.e. info, warning, error, critical, debug)',
    )
    parser.add_argument(
        'message',
        help='Log message',
    )
    parser.add_argument(
        '-D', '--details',
        help='Optional log details',
    )
    parser.add_argument(
        '-r', '--request-type',
        help='Set request type (i.e. post, get)',
        default=DEFAULT_REQUEST,
    )
    parser.add_argument(
        '--as-post-data',
        help='Use `data` param instead of JSON.',
        action='store_true',
        default=False,
    )
    parser.add_argument(
        '-e', '--extra-data',
        help='Additional JSON data.',
    )
    parser.add_argument(
        '-k1', '--key1',
        help='Log level key (i.e. log_level)',
        default=KEY_LOG_LVL,
    )
    parser.add_argument(
        '-k2', '--key2',
        help='Message key (i.e. message)',
        default=KEY_MSG,
    )
    parser.add_argument(
        '-k3', '--key3',
        help='Details key (i.e. details)',
        default=KEY_DTLS,
    )
    parser.add_argument(
        '-k4', '--key4',
        help='Source application key (i.e. source_application)',
        default=KEY_SRC_APP,
    )
    args = parser.parse_args()

    print('Calling service -> {}'.format(args.service_url))
    print('Args -> {}'.format(args))
    print('-'*40)

    extra_data = json.loads(args.extra_data) if args.extra_data else None

    for llevel in args.log_level:
        print('='*40)
        print('{}'.format(llevel))
        print('='*40)
        res = log_event(
            args.service_url,
            llevel,
            args.message,
            details=args.details,
            request_type=args.request_type,
            use_post_data=args.as_post_data,
            extra_data=extra_data,
            key_log_lvl=args.key1,
            key_msg=args.key2,
            key_dtls=args.key3,
            key_src_app=args.key4,
        )
        print(res)
        print('-'*40)
        sleep(3)

    # log_api(args.service_url, 'critical', 'Something got broken')
