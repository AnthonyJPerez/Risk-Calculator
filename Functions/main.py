
def simulate_http(request):
    import risk
    from flask import json
    from functools import reduce

    params = request.get_json(silent=True)
    
    # Run the simulation
    initializer = {
        'avgWinsPercent': 0.0,
        'avgAttackerArmiesRemaining': 0.0,
        'avgDefenderArmiesRemaining': 0.0
    }
    num_simulations = params['num_simulations']
    attacker_armies = params['attacker_armies']
    attack_until = params['attack_until']
    defender_armies = params['defender_armies']
    defend_until = params['defend_until']
    ruleset = params['ruleset']

    reduceResults = lambda results, result: risk.sumResults(results, result, num_simulations)
    results = reduce(    \
        reduceResults,    \
        risk.repeatfunc( \
            risk.run_simulation, \
            num_simulations, \
            attacker_armies, attack_until, defender_armies, defend_until, ruleset), \
        initializer)
    return json.dumps(results)