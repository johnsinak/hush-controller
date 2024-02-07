############ BASICS ############
SIMULATION_DURATION = 3 * 365 * 24 # 3 years
BIRTH_PERIOD = 1 * 365 * 24 # 1 year?
FLEET_SIZE = 10
CLIENT_UTILITY_THRESHOLD = 0.4

############ RATES ############
# for our reference: TIME_UNIT = 1 hour
NEW_USER_RATE = 1 # 1 user every hours, which is like 20 per day?
NEW_PROXY_INTERVAL = 30 # 1 every 30 hours
REJUVINATION_RATE = 1 # rejuvinations are made every this many time units 
CENSORING_AGENTS_TO_ALL_CLIENTS = 0.05 # can be 0.05, 0.1, and 0.5
CENSORING_AGENTS_TO_ALL_CLIENTS_BIRTH_PERIOD = 0.02

def run_simulation():
    for step in range(BIRTH_PERIOD):
        pass

    for step in range(SIMULATION_DURATION):
        # Censor chooses what proxies of the ones they have to block
        # Clients get affected
        # New clients get added (censor agent with chance of censoring agent)
        # Affected clients (agent or not) request for new proxies and see if they're blocked or not.
        # Number of disconnected users are determined
        # IF the rejuvination rate > 1 then count blocked proxies on intervals where there are no rejuvs 

        pass

def run(*args):
    print("we're live baby!")