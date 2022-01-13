import argparse, random
import brownie as br
from typing import Tuple

import modules.Voter    as voter


def genVotantes(*args) -> Tuple(list(voter.Voter), dict(int, list(voter.Voter))):

  voters = []

  # Candidates by locality, each position represents a locality
  assemblyCandidates = []
  congressCandidates = []
  
  p = argparse.ArgumentParser()
  p.add_argument('-f', type=str, required=True)
  
  # Localities file
  file = p.parse_args(args)[1:]
  
  with open(f"{file.f}", "r+") as locals:

    locality, nVoters, nCenters = locals.readline().split()

    # Select candidates for the locality, when read another
    if (len(voters) > 0):
      
      nCandidates = nVoters * 0.01 if nVoters > 100 else 2
      candidates  = random.choices(voters, k=nCandidates)
      mid         = len(candidates) // 2
      assemblyCandidates.append(candidates[:mid])
      congressCandidates.append(candidates[mid:])


    for v in nVoters:
      newVoter = voter.Voter(v, locality, random.choice(nCenters))
      
      # Creates new account for voter and fund it
      newAcc           = br.accounts.add(newVoter.privKey)
      newVoter.address = newAcc.address
      br.accounts[random.choice(9)].transfer(newAcc, 10000000, required_confs=0, gas_price="1 gwei")
      
      voters.append(newVoter)


  return (voters, {0: assemblyCandidates, 1: congressCandidates})
