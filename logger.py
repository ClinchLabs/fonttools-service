from logentries import LogentriesHandler
import logging
from ConfigParser import SafeConfigParser

config = SafeConfigParser()
config.read('settings.ini')
API_KEY = config.get('logentries', 'key')

log = logging.getLogger('logentries')
log.setLevel(logging.INFO)

log.addHandler(LogentriesHandler(API_KEY))
