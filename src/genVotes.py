import argparse

def genVotos(*args):
  p = argparse.ArgumentParser()
  p.add_argument('-n', type=str, required=True)
  p.add_argument('-nc', type=int, required=True)
  
  centers, ports = p.parse_args(args)._get_args()
