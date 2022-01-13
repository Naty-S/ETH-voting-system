#!/usr/bin/python3
import brownie as br

from scripts.src.genCenter import centroVotacion
from scripts.src.genVoters import genVotantes
from scripts.src.genVotes  import genVotos
from scripts.src.register  import register


def main():

  localities, voters, candidates = genVotantes("-f ../data/localities.txt")
  
  centroVotacion("-n 1 -p 5001")
  centroVotacion("-n 2 -p 5002")
  centroVotacion("-n 3 -p 5003")
  centroVotacion("-n 4 -p 5004")
  centroVotacion("-n 5 -p 5005")
  centroVotacion("-n 6 -p 5006")
  centroVotacion("-n 7 -p 5007")
  centroVotacion("-n 8 -p 5008")
  centroVotacion("-n 9 -p 5009")
  centroVotacion("-n 10 -p 5010")
  centroVotacion("-n 11 -p 5011")
  centroVotacion("-n 12 -p 5012")
  centroVotacion("-n 13 -p 5013")
  centroVotacion("-n 14 -p 5014")
  centroVotacion("-n 15 -p 5015")
  centroVotacion("-n 16 -p 5016")
  centroVotacion("-n 17 -p 5017")
  centroVotacion("-n 18 -p 5018")
  centroVotacion("-n 19 -p 5019")

  register(localities, candidates, [v.__dict__ for v in voters])

  genVotos(voters, "-n ../data/centros.txt -nc 3")
  