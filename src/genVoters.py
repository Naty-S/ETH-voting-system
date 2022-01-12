import argparse, random

import modules.Voter    as voter


def genVotantes(*args) -> list(voter.Voter):

  voters = []
  
  p = argparse.ArgumentParser()
  p.add_argument('-f', type=str, required=True)
  
  # Localities file
  file = p.parse_args(args)[1:]
  
  with open(f"{file.f}", "r+") as locals:
    locality, nVoters, nCenters = locals.readline().split()

    if (len(voters) > 0) and (locality != voters[-1].locality):
      nCandidates = nVoters * 0.01 if nVoters > 100 else 2
      candidates  = random.choices(voters, k=nCandidates)
      mid         = len(candidates) // 2
      assembly    = candidates[:mid]
      congress    = candidates[mid:]

      # Se actualiza el cargo al que se postula el candidato
      for a in assembly:
        a.cargo = 0

      for c in congress:
        c.cargo = 1


    for v in nVoters:
      newVoter = voter.Voter(v, locality, random.choice(nCenters))
      voters.append(newVoter)

  return voters
