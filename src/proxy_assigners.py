from random import randint


def random_proxy_assigner(dao, client, proxies):
    proxy = proxies[randint(0, len(proxies) - 1)]
    return proxy