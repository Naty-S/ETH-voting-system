import socket

import modules.Voter    as voter


# Register voting scenario
def register(localities: list(int), cadidates: dict(int, list(voter.Voter)), voters: list(voter.Voter)):
  
  s = socket.socket()
  msg = str((localities.__dict__, cadidates.__dict__, voters.__dict__)).encode()

  s.connect((b'localhost', 5001))
  s.send(msg)
  s.close()
