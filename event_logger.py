### EVENT LOGGER ###
""" Use this module to invoke lambda function for logging and notification system.
by: Steve Nalos

PARAMETERS: 
    url       - (str) - API Gateway URL. 
    log_level - (str) - Severity of logs. 
                      - 'info', 'warning'
                      - 'error', 'critical'
                      - 'debug'
    message   - (str) - Log message
    details   - (str) - Any other details e.g. errors, filename. 
    source_application - (str) - Name of the application being used. 
"""

import requests
import json

from time import sleep

ses = requests.Session()

def log_event(url, log_level, message, details=None, source_application=None):

    # Format parameters into json file. 
    data = {
        'json': {
            'log_level': log_level,
            'message': message,
            'details': details,
            'source_application': source_application,
            }
        }

    # Input data to lambda function and get the output    
    obj = getattr(ses, 'post')(url, **data)
    obj.raise_for_status()

    try:
        return obj.json()
    except json.decoder.JSONDecodeError:
        return res.text
    finally:
        print('='*60)
        print('{}'.format(message))
        print('='*60)
        print(obj.json())
        print('-'*60)
        sleep(1) 
