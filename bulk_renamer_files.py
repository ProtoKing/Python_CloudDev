__all__ = ['bulk_rename_files', 'rename_file',]

LAMBDA_ENDPOINT = (
    'https://ci4shtjnri.execute-api.ap-southeast-1.amazonaws.com'
    '/default/steve_email_notif_service'
    )

SRC = 'bulk_rename_files.py'

try:
    import glob, re, os, sys, logging, shutil, datetime, requests
    from pathlib import Path
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

####################################################################

# Creating a logger
FORMAT = ('[%(asctime)s] %(levelname)s %(module)s %(lineno)d - %(message)s')

logging.basicConfig(level=logging.INFO, format=FORMAT)
log = logging.getLogger(__name__)   

####################################################################

def get_files(target_dir, filter_pat=None):
    """Returns a list of files in the target_dir,
    filtered by filter_pat
    
    """
    target_dir = Path(target_dir)
    match = []
    try:
        if filter_pat:
            filter_pat = re.compile(filter_pat)

        log_event(
            url=LAMBDA_ENDPOINT, 
            log_level='info', 
            message='Transforming filter pattern.................[DONE]', 
            source_application=SRC, 
            )            
    except Exception as err:
        msg = f'Invalid filter: {err}'
        log_event(
            url=LAMBDA_ENDPOINT, 
            log_level='error', 
            message='Transforming filter pattern..................[FAILED]', 
            source_application=SRC, 
            details=f"{err}"
            )
        
    for file in target_dir.iterdir():
        if filter_pat:
            if filter_pat.match(file.name):
                match.append(file)
        else:
            match.append(file)
    log_event(
        url=LAMBDA_ENDPOINT, 
        log_level='info', 
        message='Retrieving matching files.....................[DONE]', 
        source_application=SRC, 
        )            
    return match
    
def rename_file(target_dir, name_pat, counter=None):
    """Rename file_path given name_pat, optionally include
    a counter number
    
    """

    counter = counter or ''
    new_name = f"{name_pat}{counter}{target_dir.suffix}"
    new_path = target_dir.parent.joinpath(new_name)
    shutil.move(target_dir, new_path)
        
    log.info(f'Renamed {target_dir.name} -> {new_path.name}')

    return new_path

def bulk_rename_files(name_pat, target_dir, filter_pat=None):
    target_dir = Path(target_dir)
    try: 
        counter = 0
        for fpath in get_files(target_dir, filter_pat=filter_pat):
            rename_file(fpath, name_pat, counter=counter)
            counter += 1
        log_event(
            url=LAMBDA_ENDPOINT, 
            log_level='info', 
            message='Renaming all files.....................[DONE]', 
            source_application=SRC, 
            )            
        return True    
    except Exception as e:
        log_event(
            url=LAMBDA_ENDPOINT, 
            log_level='error', 
            message='Renaming all files.....................[FAILED]', 
            source_application=SRC,
            details=f"{e}" 
            )        
####################################################################################

def main(args):
    try:
        success = bulk_rename_files(args.new_name, args.target_dir, args.filter_pat)
        if success:
            log.info('Complete!')
            log_event(
                url=LAMBDA_ENDPOINT, 
                log_level='info', 
                message='ALl done.....................[DONE]', 
                source_application=SRC, 
                )
            sys.exit(0)
        else:
            e = Exception
            log_event(
                url=LAMBDA_ENDPOINT, 
                log_level='critical', 
                message='Operation.....................[FAILED]', 
                source_application=SRC,
                details=f"{e}"                  
                )             
            sys.exit(1)
    except Exception as e:
        log_event(
            url=LAMBDA_ENDPOINT, 
            log_level='critical', 
            message='Operation.....................[FAILED]', 
            source_application=SRC,
            details=f"{e}"              
            )        
        sys.exit(1)
        
######################################################################################

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    
    # Adding Global Arguments
  
    parser.add_argument(
        'new_name',
        help='Files matching "file_pattern" will be renamed with this value. An incrementing count will also be added.'
    )
    
    parser.add_argument(
        'target_dir',
        help='Directory where the files to rename reside.'
    )
    
    parser.add_argument(
        'filter_pat',
        help='Files to rename (Regex compatible).'
    )
            
    parser.add_argument('-L', '--log-level',
        help='Set log level',
        default='info'
    )
        
    args = parser.parse_args()
    
    # Logger Configuration
    logging.basicConfig(level=getattr(logging, args.log_level.upper()), format=FORMAT,)
    
    
    main(args)