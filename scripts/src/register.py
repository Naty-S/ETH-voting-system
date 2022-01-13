#!/usr/bin/python3
import socket

import scripts.modules.Voter    as voter


""" Register voting scenario

  localities: {1: (# voters, # voting centers), ...}.

  candidates: {1: [Voter, ...], 2: [Voter, ...]}.
    1: Assembly candidate, 2: Congress candidate.

  voters: All voters
"""
def register(
  localities: list(tuple(int, int)),
  cadidates: dict(int, list(dict)),
  voters: list(dict)
):
  s   = socket.socket()
  ls  = str(localities).encode()
  vs  = str(voters).encode()
  cs  = cadidates.__dict__
  msg = str((ls, vs, cs)).encode()

  s.connect((b'localhost', 5001))
  s.send(msg)
  s.close()
