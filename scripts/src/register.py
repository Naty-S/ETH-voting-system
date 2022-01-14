#!/usr/bin/python3
import socket

import scripts.config.vars as vars

""" Register voting scenario

  localities: [(# voters, # voting centers), ...].

  candidates: ([Voter, ...], [Voter, ...]).
    Assembly candidates, Congress candidates.

  voters: All voters
"""
def register(localities, cadidates, voters):
  
  s   = socket.socket()
  ls  = localities
  vs  = voters
  cs  = cadidates
  msg = str((ls, vs, cs)).encode()

  s.connect((b'localhost', 5001))
  s.send(msg)
  s.recv(512)
  s.close()

  vars.scenaryInit = True
