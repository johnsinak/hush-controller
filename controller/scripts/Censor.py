from assignments.models import Assignment, Proxy, Client

class AggresiveCensor():
    def __init__(self) -> None:
        self.agents = []
    
    def run(self):
        # print(self.agents)
        known_proxies = Assignment.objects.filter(client__in=self.agents).values_list('proxy', flat=True).distinct()
        known_proxies_good_for_blocking = Proxy.objects.filter(id__in=known_proxies, is_blocked=False, is_active=True)
        # print(known_proxies_good_for_blocking)
        return known_proxies_good_for_blocking

class OptimalCensor():
    def __init__(self) -> None:
        self.agents = []
    
    def run(self):
        pass
    
