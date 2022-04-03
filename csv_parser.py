### CSV PARSER ###
''' Parse csv file contents from the internet, and output to a csv file'''
### by: Steve Nalos ###
 
LAMBDA_ENDPOINT = (
    'https://ci4shtjnri.execute-api.ap-southeast-1.amazonaws.com'
    '/default/steve_email_notif_service'
    )

SRC = 'csv_parser.py'

try: 
    import csv
    import requests
    from event_logger import log_event

    log_event(
        url=LAMBDA_ENDPOINT, 
        log_level='info', 
        message='Importing packages and modules.....................[DONE]', 
        source_application=SRC, 
        )
except ImportError as e:
    log_event(
        url=LAMBDA_ENDPOINT, 
        log_level='critical', 
        message='Importing necessary packages and modules.....................[FAILED]', 
        source_application=SRC,
        details=f"{e}" 
        )        
try: 
    # Prompt user to enter url 
    url = input('Enter the url csv of the file: ')
    outfile = 'clean_products_2.csv'
    url_file = requests.get(url, allow_redirects=True)
    
    log_event(
        url=LAMBDA_ENDPOINT, 
        log_level='info', 
        message='Fetching contents from the url.....................[DONE]', 
        source_application=SRC, 
        details=f"{url}"
        )
except MemoryError as e:
    log_event(
        url=LAMBDA_ENDPOINT, 
        log_level='critical', 
        message='Fetching contents from the url.....................[FAILED]', 
        source_application=SRC, 
        details=f"Operation runs out of memory. {e}"
        )
except (RuntimeError, SystemError) as e:
    log_event(
        url=LAMBDA_ENDPOINT, 
        log_level='critical', 
        message='Fetching contents from the url.....................[FAILED]', 
        source_application=SRC, 
        details=f"An unknown error occured. {e}"
        )
except Exception as e:
    log_event(
        url=LAMBDA_ENDPOINT, 
        log_level='debug', 
        message='Fetching contents from the url.....................[FAILED]', 
        source_application=SRC, 
        details=f"{e}"
        )
    
try: 
    with open('sample_products.csv','w') as fh:
        fh.write(url_file.text)
    file = fh.name

    log_event(
        url=LAMBDA_ENDPOINT, 
        log_level='info',
        message='Writing contents to a csv file.....................[DONE]', 
        source_application=SRC, 
        details=f'url: {url}; file: {file}'
        )  
except Exception as e:
    log_event(
        url=LAMBDA_ENDPOINT, 
        log_level='error', 
        message='Writing contents to a csv file.....................[FAILED]', 
        source_application=SRC, 
        details=f'Error: {e};url: {url}'
        )    

try:    
    # Obtaining headers
    with open(f'{file}',newline='') as f0: 
       reader2 = csv.reader(f0)
       fieldnames = next(reader2)

    log_event(
        url=LAMBDA_ENDPOINT, 
        log_level='info',
        message='Obtaining file headers...............................[DONE]', 
        source_application=SRC, 
        details=f'file: {file}'
        )  
except Exception as e:
    log_event(
        url=LAMBDA_ENDPOINT, 
        log_level='debug',
        message='Obtaining file headers.....................[FAILED].', 
        source_application=SRC, 
        details=f'file: {file}'
        )
try:              
    # Reading contents of a csv as a dict. 
    with open(f'{file}',newline='') as f, open(outfile, 'w', newline='') as f2:
        reader = csv.DictReader(f)
        writer = csv.DictWriter(f2,fieldnames=fieldnames)
        writer.writeheader()
    
    # Writing clean contents in a new csv file.
        for row in reader:
            if row['Categories'] != '':
                writer.writerow(row)

    log_event(
        url=LAMBDA_ENDPOINT, 
        log_level='info',
        message=f"Output file written in {outfile}.............[DONE]", 
        source_application=SRC
        )
    print("End.")    
except MemoryError as e:
    log_event(
        url=LAMBDA_ENDPOINT, 
        log_level='critical', 
        message=f"Output file written in {outfile}..............[FAILED]", 
        source_application=SRC, 
        details=f"{e}"
        )
except (RuntimeError, SystemError) as e:
    log_event(
        url=LAMBDA_ENDPOINT, 
        log_level='critical', 
        message=f"Output file written in {outfile}...............[FAILED]", 
        source_application=SRC, 
        details=f"{e}"
        )
except ResourceWarning as e:
    log_event(
        url=LAMBDA_ENDPOINT, 
        log_level='warning', 
        message=f"Output file written in {outfile}................[FAILED]", 
        source_application=SRC
        )     
except Exception as e:
    log_event(
        url=LAMBDA_ENDPOINT, 
        log_level='debug',
        message= f"Output file written in {outfile}................[FAILED]", 
        source_application=SRC,
        details=f"{e}"
        )    
