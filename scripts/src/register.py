import socket
from typing import Tuple

import modules.Voter    as voter


""" Register voting scenario

  localities: {1: (# voters, # voting centers), ...}. Each key represents the locality

  candidates: {0: [Voter], 1: [Voter]}.
    0: Assembly candidate, 1: Congress candidate.
    Each position in the lists represents the locality

  voters: All voters
"""
def register(localities: dict(int, Tuple(int, int)), cadidates: dict(int, list(voter.Voter)), voters: list(voter.Voter)):
  
  s   = socket.socket()
  ls  = localities.__dict__
  vs  = voters.__dict__
  cs  = cadidates.__dict__
  msg = str(("Init", ls, vs, cs)).encode()

  s.connect((b'localhost', 5001))
  s.send(msg)
  s.close()
