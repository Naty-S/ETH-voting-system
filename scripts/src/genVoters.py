#!/usr/bin/python3
import argparse, random
import brownie as br

import scripts.modules.Voter as voter


def genVotantes(*args):

  voters = []
  localities = []

  # Candidates by locality, each position represents a locality
  assemblyCandidates = []
  congressCandidates = []
  
  p = argparse.ArgumentParser()
  p.add_argument('-f', type=str, required=True)
  
  # Localities file
  file = p.parse_args(args)
  
  locals = open(f"{file.f[1:]}", "r+")

  for l in locals:

    line     = l.split()
    locality = line[0]
    nVoters  = int(line[1])
    nCenters = int(line[2])
    loc      = int(locality.partition('l')[2])

    localities.append((nVoters, nCenters))
    
    print(f"\n\tReading {locality}...\n")

    for v in range(nVoters):
      
      center   = random.randrange(1, nCenters)
      newVoter = voter.Voter(v + len(voters), loc, center)
      
      # Creates new account for voter and fund it from miner account
      newAcc           = br.accounts.add(newVoter.privKey)
      newVoter.address = newAcc.address

      print("\n\tFunding new voter account...\n")
      br.accounts[0].transfer(newAcc, 10000000, required_confs=0, gas_price="1 gwei")
      
      voters.append(newVoter)

    # Select candidates for the locality
    nCandidates = nVoters * 0.01 if nVoters > 100 else 2
    locVoters   = voters if loc == 1 else voters[len(voters) - nVoters:]
    lCandidates = [v.__dict__ for v in locVoters]
    candidates  = random.sample(lCandidates, nCandidates)
    mid         = len(candidates) // 2

    assemblyCandidates.append(candidates[:mid])
    congressCandidates.append(candidates[mid:])


  print("\n\tVoters created...\n")

  return (localities, voters, (assemblyCandidates, congressCandidates))
