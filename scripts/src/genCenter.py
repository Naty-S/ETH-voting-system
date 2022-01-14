#!/usr/bin/python3
import argparse

import scripts.modules.Center as center


def centroVotacion(*args) -> center.Center:

  p = argparse.ArgumentParser()
  p.add_argument('-n', type=int, required=True)
  p.add_argument('-p', type=int, required=True)
  # p.add_argument('-f', type=str, required=True)
  
  myArgs = p.parse_args(args)
  centerName, port = myArgs.n, myArgs.p

  print(f"\n\tStarting center {centerName}\n")
  
  return center.Center(centerName, port)
