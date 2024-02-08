from assignments.models import Client, Proxy, ProxyReport, Assignment
from .Censor import *
from .config_basic import *
from .simulation_utils import request_new_proxy, request_new_proxy_new_client


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
    pr1 = Proxy.objects.create(ip=f'1.0.0.1', is_test=True, is_active=False)
    pr2 = Proxy.objects.create(ip=f'1.0.0.2', is_test=True, is_blocked=True)
    pr3 = Proxy.objects.create(ip=f'1.0.0.3', is_test=True)
    pr4 = Proxy.objects.create(ip=f'1.0.0.4', is_test=True)
    pr5 = Proxy.objects.create(ip=f'1.0.0.5', is_test=True)
    pr6 = Proxy.objects.create(ip=f'1.0.0.6', is_test=True)
    pr7 = Proxy.objects.create(ip=f'1.0.0.7', is_test=True)

    cl1 = Client.objects.create(ip='2.2.2.2')
    cl2 = Client.objects.create(ip='3.3.3.3', is_censor_agent=True)
    request_new_proxy_new_client(cl1)
    request_new_proxy_new_client(cl2)

    # Assignment.objects.create(proxy=pr1, client=cl, assignment_time=4)
    # Assignment.objects.create(proxy=pr2, client=cl, assignment_time=2)
    # Assignment.objects.create(proxy=pr3, client=cl, assignment_time=5)
    # Assignment.objects.create(proxy=pr5, client=cl, assignment_time=1)


    print(request_new_proxy([cl1,cl2], 10))
    print(request_new_proxy([cl1,cl2], 15))
    print(request_new_proxy([cl1,cl2], 20))

    # print(request_new_proxy('5.5.5.5'))
    # print(request_new_proxy('5.5.5.5'))
