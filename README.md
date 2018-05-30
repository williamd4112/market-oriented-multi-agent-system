Multi-agent system for Taxi coordinator
=

TODO
--
- [] Lookahead bidding
- [] Check the formula of payoff computation
- [] Enable the driver to give up the call

Requirements
--
- numpy>=1.14
- sortedcontainers

Installation
--
1. ```pip install -r requirement.txt```

Note for developers
--
- Driver payment computation [[code](https://github.com/williamd4112/market-oriented-multi-agent-system/blob/e9f82c533e5f7cd655d08fa9d1a48712d9cbc733/auction/taxi_coordinator.py#L71)]
- Driver payoff computation [[code](https://github.com/williamd4112/market-oriented-multi-agent-system/blob/e9f82c533e5f7cd655d08fa9d1a48712d9cbc733/auction/taxi_driver.py#L204)]
- Bidding price computation [[code](https://github.com/williamd4112/market-oriented-multi-agent-system/blob/e9f82c533e5f7cd655d08fa9d1a48712d9cbc733/auction/taxi_driver.py#L204)]
- Data for visualization
  - Load from JSON (see ```test_load_json.py```)

