import argparse

def centroVotacion(*args):
  p = argparse.ArgumentParser()
  p.add_argument('-n', type=str, required=True)
  p.add_argument('-p', type=int, required=True)
  p.add_argument('-f', type=str, required=True)
  
  center, port, ethNode = p.parse_args(args)._get_args()
