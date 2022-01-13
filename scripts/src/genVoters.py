#!/usr/bin/python3
import argparse, random
import brownie as br

import scripts.modules.Voter as voter
import scripts.config.vars   as vars


def genVotantes(*args): # -> tuple(list(voter.Voter), dict(int, list(voter.Voter))):

  voters = []
  localities = []

  # Candidates by locality, each position represents a locality
  assemblyCandidates = []
  congressCandidates = []
  
  p = argparse.ArgumentParser()
  p.add_argument('-f', type=str, required=True)
  
  # Localities file
  file = p.parse_args(args)[1:]
  
  with open(f"{file.f}", "r+") as locals:

    locality, nVoters, nCenters = locals.readline().split()
    localities.append((nVoters, int(nCenters)))

    # Select candidates for the locality, when read another
    votersLen = len(voters)
    if (votersLen > 0):
      
      nCandidates = int(nVoters) * 0.01 if int(nVoters) > 100 else 2
      lCandidates = [v.__dict__ for v in voters[votersLen - 1:]]
      candidates  = random.choices(lCandidates, k=nCandidates)
      mid         = len(candidates) // 2
      assemblyCandidates.append(candidates[:mid])
      congressCandidates.append(candidates[mid:])


    for v in range(int(nVoters)):
      newVoter = voter.Voter(v, int(locality[-1]), random.choice(int(nCenters)))
      
      # Creates new account for voter and fund it
      newAcc           = br.accounts.add(newVoter.privKey)
      newVoter.address = newAcc.address
      br.accounts[random.choice(9)].transfer(newAcc, 10000000, required_confs=0, gas_price="1 gwei")
      
      voters.append(newVoter)


  return (localities, voters, {1: assemblyCandidates, 2: congressCandidates})
