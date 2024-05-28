from dotenv import dotenv_values


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'formatter': {
            'format': '{asctime} : {levelname} ({levelno}) : {pathname} : Line {lineno} -> {message}',
            'style': '{'
        }
    },
    'handlers': {
        'application_logger': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': ''.join([dotenv_values(dotenv_path=dotenv_values(dotenv_path='airbnb/.env').get('HOST_ENV_ENV_PATH')).get('LOGS_DIR'), 'application_log.log']),
            'interval': 1,
            'when': 'h',
            'backupCount': 24,
            'formatter': 'formatter'
        }
    },
    'loggers': {
        '': {
            'level': 'DEBUG',
            'handlers': ['application_logger']
        }
    }
}


