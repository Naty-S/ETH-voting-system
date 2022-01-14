#!/usr/bin/python3
import scripts.config.vars    as vars

from scripts.src.genCenter  import centroVotacion
from scripts.src.genVoters  import genVotantes
from scripts.src.genVotes   import genVotos
from scripts.src.register   import register
from scripts.src.visualizer import visualizer


def main():

  localities, voters, candidates = genVotantes("-f scripts/data/localidades.txt")
  
  centers = []
  centers.append(centroVotacion("-n 1", "-p 5001"))
  centers.append(centroVotacion("-n 2", "-p 5002"))
  centers.append(centroVotacion("-n 3", "-p 5003"))
  centers.append(centroVotacion("-n 4", "-p 5004"))
  centers.append(centroVotacion("-n 5", "-p 5005"))
  centers.append(centroVotacion("-n 6", "-p 5006"))
  centers.append(centroVotacion("-n 7", "-p 5007"))
  centers.append(centroVotacion("-n 8", "-p 5008"))
  centers.append(centroVotacion("-n 9", "-p 5009"))
  centers.append(centroVotacion("-n 10", "-p 5010"))

  register(localities, candidates, [v.__dict__ for v in voters])

  vars.Voting.startVoting()

  genVotos(localities, voters, candidates, "scripts/data/centros.txt", 1)

  vars.Voting.closeVoting()
        
  visualizer()

  vars.Voting.reset()

  exit()
