### EMAIL & LOG NOTIFICATION SERVICE ###
""" Fetch logs from a service application and alert developers through SNS. 
by: Steve Nalos

PARAMETERS:
    event     - (json) - composed of various data used as inputs to various parameters.
    log_level - (str) - Severity of logs. 
                      - 'info', 'warning'
                      - 'error', 'critical'
                      - 'debug'
    message   - (str) - Log message
    details   - (str) - Any other details e.g. errors, filename. 
    source_application - (str) - Name of the application being used.      
"""

import boto3
import json
import logging
import requests
from datetime import datetime

log = logging.getLogger('steve_email_notif_service')
log.setLevel(logging.INFO)

BASE_RES_URL = (
    'https://8hj75wczi6'
    '.execute-api.ap-southeast-1.amazonaws.com'
    '/default{}'
)

DB_NAME = 'steve_application_logs'
REGION = 'ap-southeast-1'
__sns_client__ = boto3.client('sns', region_name=REGION)
__dynamodb_client__ = boto3.resource('dynamodb', region_name=REGION)
SEND_TO = 'steveanthony.nalos@gcash.com'

FORMAT = 'steve_email_notif_log_'

NOW = datetime.utcnow().strftime('%Y%m%d%H%M%S')

SNS_TOPIC_MAP = {
    'steve_email_notif_log_info': 'info',
    'steve_email_notif_log_warning': 'warning',
    'steve_email_notif_log_error': 'error',
    'steve_email_notif_log_critical': 'critical',
    'steve_email_notif_log_debug': 'debug',
    }
    
API_PARAMS = {
        'log_level', 
        'message', 
        'details', 
        'source_application'
        }

def obtain_sns_topic_arns():
    """Returns a dictionary of log level and it's corresponding SNS Topic ARN."""
    
    topics = (__sns_client__.list_topics()).get('Topics', [])

    arns = {}

    for topic in topics:
        arn = topic.get('TopicArn', '')
        name = arn.split(':')[-1]
        if name in SNS_TOPIC_MAP.keys() and name not in arns.keys():
           arns[name] = arn
    return arns

def log_sns_event(sns_arn, message):
    """Log Message to an SNS topic."""
    
    params = {
        'TopicArn': sns_arn, 
        'Message': message,
    }
    __sns_client__.publish(**params)
    return True

def send_email_alert(message):
    """Send an email alert when log is critical."""
    
    subject = '[URGENT EMAIL] CRITICAL ERROR ALERT!!!'
    url = BASE_RES_URL.format('/ac2e_email_sender_service')
    message = str(message)
    res = requests.post(url, json={
        'to': SEND_TO,
        'subject': subject,
        'body': message,
    })
    res.raise_for_status()
    return res.json()
    
def store_log(data):
    """Store application log to Dynamodb table."""
    
	# Connect to Dynamodb table
    log_table = __dynamodb_client__.Table(DB_NAME)
    period = int(NOW)
	
	# Parse data into db json formatted file 

    item = {
	    "source_application": {"S": data['source_application'] },
	    "period": {"S": period },
	    "log_level": {"S": data['log_level'] },
	    "message": {"S": data['message'] },
	    "details": {"S": data['details'] }
	}
	    
    try:
        log_table.put_item(Item=item)
        log.info('Application log saved to log database...[DONE]')
    except Exception as e:
        log.error(e)
        log.error('Application log saved to log database...[FAILED]')
        
def lambda_handler(event, context):
    # try: 
    #     # Store log to dynamodb table
    #     data = json.dumps(event.copy())
    #     store_log(data)        
    # except Exception as e:
    #     log.error(f'Event: {event}')    
    
    try:
        #Ensure proper formatting of SNS Data.
        VALID_PARAMS = set(API_PARAMS)
        if not VALID_PARAMS.issuperset(set(event.keys())):
            log.error('Invalid event parameter/s.')
            return {
                'status': 400,
                'message': 'Invalid request.'
                }
                

        
        # Map log-level and extract message from app
        log_level = event['log_level']
        sns_message = json.dumps(event)
        
        # Publish to SNS
        target_sns_topic_arns = obtain_sns_topic_arns()
        sns_arn = target_sns_topic_arns[f"{FORMAT}{log_level}"]
        log_sns_event(sns_arn, sns_message)
        
        # Email alert for critical logs
        if log_level == 'critical':
            send_email_alert(sns_message)

        return {
            'status': 202,
            'message': 'Request has been recorded.'
            }
        

    except Exception as e:
        log.error(e)
        log.error(f'Event: {event}')

        return {
            'status': 400,
            'message': 'Invalid request.',
            'error': e
            }
