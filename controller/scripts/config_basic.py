############ BASICS ############
SIMULATION_DURATION = 3 * 365 * 24 # 3 years
BIRTH_PERIOD = 1 * 365 * 24 # 1 year?
FLEET_SIZE = 10
CLIENT_UTILITY_THRESHOLD = 0.4
WORLD_SIZE = 20000
CENSORED_REGION_SIZE = 1000

############ RATES ############
# for our reference: TIME_UNIT = 1 hour
NEW_USER_RATE_INTERVAL = 1 # 1 user every 1 hour
NEW_USER_COUNT = 1

NEW_PROXY_INTERVAL = 30 # 1 every 30 hours
NEW_PROXY_COUNT = 1

REJUVINATION_INTERVAL = 1 # rejuvinations are made every this many time units 
CENSORING_AGENTS_TO_ALL_CLIENTS = 0.05 # can be 0.05, 0.1, and 0.5
CENSORING_AGENTS_TO_ALL_CLIENTS_BIRTH_PERIOD = 0.02