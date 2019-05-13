from unittest.mock import Mock
import risk
import main


def test_compare_dice():
    assert risk.DieComparison.Higher == risk.compareDice((10,1))
    assert risk.DieComparison.Lower == risk.compareDice((1,10))
    assert risk.DieComparison.Equal == risk.compareDice((10,10))


def test_simulate_http():
    data = {
        'num_simulations': 1000,
        'attacker_armies': 30,
        'attack_until': 0,
        'defender_armies': 0,
        'defend_until': 0,
        'ruleset': {
            'attackerDice': 3,
            'attackerDieSize': [1,6],
            'minArmiesForAttack': 1,
            'defenderDice': 2,
            'defenderDieSize': [1,6],
            'minArmiesForDefend': 0,
            'tieBehavior': 0
        }
    }
    request = Mock(get_json=Mock(return_value=data), args=data)
    results = main.simulate_http(request)
    assert 'avgWinsPercent' in results
    assert 'avgAttackerArmiesRemaining' in results
    assert 'avgDefenderArmiesRemaining' in results

