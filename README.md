Multi-agent system for Taxi coordinator
=

TODO
--
- [ ] Lookahead bidding
- [ ] Check the formula of payoff computation
- [ ] Enable the driver to give up the call

Requirements
--
- numpy>=1.14
- sortedcontainers

Installation
--
1. ```pip install -r requirement.txt```

Note for developers
--
- Company payment computation [[code](https://github.com/williamd4112/market-oriented-multi-agent-system/blob/2b859980d4d8ecf4336d02cca5fcd6ca0d53b37d/auction/taxi_coordinator.py#L109)]
- Driver payment computation [[code](https://github.com/williamd4112/market-oriented-multi-agent-system/blob/2b859980d4d8ecf4336d02cca5fcd6ca0d53b37d/auction/taxi_coordinator.py#L81)]
- Driver payoff computation [[code](https://github.com/williamd4112/market-oriented-multi-agent-system/blob/2b859980d4d8ecf4336d02cca5fcd6ca0d53b37d/auction/taxi_driver.py#L217)]
- Bidding price computation [[code](https://github.com/williamd4112/market-oriented-multi-agent-system/blob/2b859980d4d8ecf4336d02cca5fcd6ca0d53b37d/auction/taxi_driver.py#L195)]
- Data for visualization
  - Load from JSON (see ```test_load_json.py```)

