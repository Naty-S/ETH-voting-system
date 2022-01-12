import argparse

import modules.Center as center

def centroVotacion(*args):

  p = argparse.ArgumentParser()
  p.add_argument('-n', type=int, required=True)
  p.add_argument('-p', type=int, required=True)
  # p.add_argument('-f', type=str, required=True)
  
  myArgs = p.parse_args(args)
  centerName, port = myArgs.n, myArgs.p

  center.Center(centerName, "", port)
