class Hostname(object):
    platform = 'Generic'
    distribution = None
    strategy_class = UnimplementedStrategy
    # Possible annotation strategy
    # distribution: Union[None, str] = None
    # strategy_class: Type[Strategy] = UnimplementedStrategy

class RHELHostname(Hostname):
    platform = 'Linux'
    distribution = 'Redhat'
    strategy_class = RedHatStrategy