
def simulate_http(request):
    import risk
    from flask import json
    from functools import reduce

    params = request.get_json(silent=True)
    #params = json.loads('''{"num_simulations":1000,"attacker_armies":30,"attack_until":0, "defender_armies":30, "defend_until":0,"ruleset":{"attackerDice":3,"attackerDieSize":[1,6],"minArmiesForAttack":1,"defenderDice":2,"defenderDieSize":[1,6],"minArmiesForDefend":0,"tieBehavior":0}}''')
    
    # Run the simulation
    initializer = {
        'avgWinsPercent': 0.0,
        'avgAttackerArmiesRemaining': 0.0,
        'avgDefenderArmiesRemaining': 0.0
    }

    reduceResults = lambda results, result: risk.sumResults(results, result, params['num_simulations'])
    results = reduce(    \
        reduceResults,    \
        risk.repeatfunc( \
            risk.run_simulation, \
            params['num_simulations'], \
            params['attacker_armies'], params['attack_until'], params['defender_armies'], params['defend_until'], params['ruleset']), \
        initializer)
    return json.dumps(results)