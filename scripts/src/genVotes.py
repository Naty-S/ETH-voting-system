import argparse

import modules.Voter    as voter


def genVotos(voters: list(voter.Voter), *args):

  p = argparse.ArgumentParser()
  p.add_argument('-n', type=str, required=True)
  p.add_argument('-nc', type=int, required=True)
  
  myArgs = p.parse_args(args)
  centersFile, concurrency = myArgs.n, myArgs.nc

  centers = open(f"{centersFile}", "r+")
  totalCenters = centers.readline()

  for c in centers[1:]:
    centerName, centerPort = c.split()
  
  centers.close()

  # Wait for center1 to initialize scenario

  for v in voters:
    v.center
