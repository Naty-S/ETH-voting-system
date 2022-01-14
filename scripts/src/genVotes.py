#!/usr/bin/python3
import random, socket, threading
from os import abort

import scripts.config.vars   as vars


# Voters with abstention
trueVoters = []

def genVotos(localities, voters, candidates, centersFile, concurrency) -> None:

  centersPorts  = []
  votingThreads = []
  global trueVoters
  # Total centers by locality
  locsNcenters  = [ l[1] for l in localities ]
  centersFile   = open(f"{centersFile}", "r+")
  totalCenters  = centersFile.readline()

  for c in centersFile.readlines():
    _, centerPort = c.split()
    centersPorts.append(int(centerPort))
  
  centersFile.close()

  locI = 0
  for loc in localities:
    locAbstention = loc[0] * random.randrange(1, 4) // 10
    locVoters     = [ v for v in voters if v.locality == locI ]
    trueLocVoter  = random.sample(locVoters, k= len(locVoters) - locAbstention)
    trueVoters.append(trueLocVoter)
  
    locI += 1

  # Join in one list
  trueVoters = sum(trueVoters, [])

  for c in range(concurrency):
    voteArgs = (locsNcenters, centersPorts, candidates)
    thread   = threading.Thread(name="voterT-" + str(c), target=_votingThread, args=voteArgs)
    votingThreads.append(thread)
  
  for vt in votingThreads:
    vt.start()

  for vt in votingThreads:
    vt.join()


def _votingThread(locsNcenters, centers, candidates):
  
  global trueVoters
  
  for v in trueVoters:
    _vote(locsNcenters, centers, v, candidates)


def _vote(locsNcenters, centers, voter, candidates):

  assert(vars.scenaryInit)

  print("\n\tStarting voting...\n")

  s              = socket.socket()
  loc            = voter.locality
  prevNcenters   = locsNcenters[loc - 2 if loc > 1 else 0]
  center         = voter.center
  port           = centers[prevNcenters + center - 1 if loc > 1 else center - 1]
  assemblyChoice = random.randrange(len(candidates[0][loc]))
  congressChoice = random.randrange(len(candidates[1][loc]))
  vote           = str((voter.address, assemblyChoice, congressChoice)).encode()

  print(f"\n\tConecting to {port}...\n")
  s.connect((b'localhost', port))

  print(f"\n\tEnviando voto: {vote}...\n")
  s.send(vote)

  # Wait to finish
  s.recv(512)
  
  s.close()
