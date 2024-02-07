from assignments.models import Client, Proxy, ProxyReport, Assignment
from .Censor import *
from .config_basic import *


############ CENSOR ############
censor = OptimalCensor()

def run_simulation(birth_period:bool):
    duration = BIRTH_PERIOD if birth_period else SIMULATION_DURATION
    global censor


    for step in range(duration):
        # Censor chooses what proxies of the ones they have to block
        list_of_proxies_to_be_blocked = censor.run()
        # TODO: mark these proxies as blocked
        
        # NOTE: maybe not neccesary. Clients get affected
        #   enumerate clients that are connected to the blocked proxies and update things?

        # Affected clients (agent or not) request for new proxies and see if they're blocked or not.
        #   The get proxy algo gets run for every single client that was previously connected to those blocked proxies

        #TODO: at some point I should decide when the agents request for new proxies

        # Number of disconnected users are determined and recorded
        #   this is just data collection

        # IF the rejuvination interval > 1 then count blocked proxies on intervals where there are no rejuvs
        #   TODO: decide whether this is done before or after clients request for new thngs
        if REJUVINATION_INTERVAL > 1:
            # record_blocked stuff
            pass
        

        # New proxies (if any) get created
        if step % NEW_PROXY_INTERVAL == 0:
            # create new proxy
            pass

        # New clients get added (censor agent with chance of censoring agent)
        if step % NEW_USER_RATE_INTERVAL == 0:
            # create a new client (censor agent with the specific chance)
            pass

        pass

def run(*args):
    print("we're live baby!")