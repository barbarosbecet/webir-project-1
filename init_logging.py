"""
WiSe 15, WebIR, Project-1, Becet, Simmet
Initializer for logging (compatible for bibtexparser library)
"""

import logging
import logging.config


def init_logging():
    logging.config.dictConfig({
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s [%(levelname)s] %(name)s %(funcName)s:%(lineno)d: %(message)s'
            },
        },
        'handlers': {
            'default': {
                'level': 'WARNING',
                'formatter': 'standard',
                'class': 'logging.StreamHandler',
            },
        },
        'loggers': {
            '': {
                'handlers': ['default'],
                'level': 'WARNING',
                'formatter': 'standard',
                'propagate': True
            }
        }
    })

