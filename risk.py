from random import *

def attack(aArmies, dArmies):
  a = []
  d = []
  
  # Give the players their dice
  [a.append(randint(1,6)) for _ in range(min(aArmies-1, 3))]
  [d.append(randint(1,6)) for _ in range(min(dArmies, 2))]
	
  # Sort each player's dice
  a.sort()
  d.sort()
  
  #print "Dice: "
  #print a
  #print d
  
  try:
    # Attack with dice until one array is empty, Max of two dice to check
    for _ in range(2):
      attacker, defender = (a.pop(), d.pop())
      #print "Attacker: ", attacker, ", Defender: ", defender
      aArmies -= 0 if attacker > defender else 1
      dArmies -= 1 if attacker > defender else 0
  except IndexError:
    pass

  return (aArmies, dArmies)	

  
def run_round(a, d):
  aArmies = a
  dArmies = d
  while aArmies > 1 and dArmies > 0:
    aArmies, dArmies = attack(aArmies, dArmies)
  return (True if dArmies == 0 else False, aArmies, dArmies)
  
	
def run_risk(a, d, numRounds):
  count = 0;
  armiesLost = 0
  totalRounds = numRounds
  attackerArmies = a
  defenderArmies = d
  for round in xrange(1, totalRounds):
    win, aArmies, dArmies = run_round(attackerArmies,defenderArmies)
    #print "Round: ", round
    if win:
      count += 1
      armiesLost += attackerArmies - aArmies
	  
  print "Wins: ", (count*100)/totalRounds, "%, Armies lost: ", ((armiesLost*100)/max(attackerArmies*count,1)), "%"
	
	
