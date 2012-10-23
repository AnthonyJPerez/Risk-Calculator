from random import *




def compare(attackArmies, defendArmies, attackDice, defendDice):
  attackArmies -= 0 if attackDice > defendDice else 1
  defendArmies -= 1 if attackDice > defendDice else 0
  return (attackArmies, defendArmies)




def attack_custom(attackArmies, defendArmies, maxNumAttackDice=3, maxNumDefendDice=2, attackDiceMin=1, attackDiceMax=6, defendDiceMin=1, defendDiceMax=6):
  aArr = []
  dArr = []

  # Give the players their dice:
  # Each player gets either the max dice they can use, or dice 
  # equal to the amount of armies they have to attack with, 
  # whichever is smallest.
  [aArr.append(randint(attackDiceMin, attackDiceMax)) for _ in range(min(attackArmies-1, maxNumAttackDice))]
  [dArr.append(randint(defendDiceMin, defendDiceMax)) for _ in range(min(defendArmies, maxNumDefendDice))]

  # Sort each player's dice
  aArr.sort()
  dArr.sort()

  # Compare dice until one array is out of dice
  try:
    while True:
      attackArmies, defendArmies = compare(attackArmies, defendArmies, aArr.pop(), dArr.pop())
  except IndexError:
    pass

  # Return the updated armies
  return (attackArmies, defendArmies)




def attack(aArmies, dArmies):
  a = []
  d = []
  
  # Give the players their dice
  [a.append(randint(1,6)) for _ in range(min(aArmies-1, 3))]
  [d.append(randint(1,6)) for _ in range(min(dArmies, 2))]
	
  # Sort each player's dice
  a.sort()
  d.sort()
  
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
    aArmies, dArmies = attack_custom(aArmies, dArmies)
  return (True if dArmies == 0 else False, aArmies, dArmies)
  


	
def run_risk(a, d, numRounds):
  count = 0;
  armiesLost = 0
  defenderLoss = 0
  totalRounds = numRounds
  attackerArmies = a
  defenderArmies = d
  for round in xrange(1, totalRounds):
    win, aArmies, dArmies = run_round(attackerArmies,defenderArmies)
    #print "Round: ", round
    if win:
      count += 1
      armiesLost += attackerArmies - aArmies
    else:
      defenderLoss += defenderArmies - dArmies

  print ""
  print "******** Attacker: ", a, " vs. Defender: ", d, " ********"  
  print "Attacker Win Chance: %3.f%%" % ((count*100)/totalRounds)
  print "Average Attacker loss: %3.f%%" % ((armiesLost*100)/max(attackerArmies*count,1))
  print ""
  print "Defender Win Chance: %3.f%%" % (100 - ((count*100)/totalRounds))
  print "Average Defender loss: %3.f%%" % ((defenderLoss*100)/max(defenderArmies*count,1))
  print ""	
	
