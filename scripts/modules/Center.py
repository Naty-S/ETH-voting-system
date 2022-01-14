#!/usr/bin/python3
import ast, socket, threading
import brownie as br

import scripts.config.vars   as vars


class Center:

  def __init__(self, center: int, port:int) -> None:
    self.__name       = center
    self.__port       = port
    self.__socket     = socket.socket()
    self.netListenerT = threading.Thread(name=str(self.__name)+"-netListener", target=self.__netListener)
  
    # Start server
    self.__socket.bind((b'localhost', self.__port))
    self.netListenerT.start()
  

  def __registerLocalities(self, localities):

    print("\n\tRegister localities...\n")
    loc = 1
    for l in localities:
      vars.Voting.registerLocality(loc, l[0], {'from': br.accounts[0]})
      loc += 1


  def __registerVoters(self, voters):

    print("\n\tRegister voters...\n")
    for v in voters:
      vars.Voting.registerVoter(v["address"], v["name"], v["locality"], {'from': br.accounts[0]})
  

  def __registerCandidates(self, candidates):

    print("\n\tRegister candidates...\n")
    for ac in candidates[0]:
      for c in ac:
        vars.Voting.registerCandidate(c["address"], c["name"], 1, c["locality"], {'from': br.accounts[0]})

    for cc in candidates[1]:
      for c in cc:
        vars.Voting.registerCandidate(c["address"], c["name"], 2, c["locality"], {'from': br.accounts[0]})


  def __netListener(self) -> None:

    self.__socket.listen(5)

    votingOpen = True

    while votingOpen:

      print(f"\n\tCenter {self.__name} listening...\n")
      connex  = self.__socket.accept()[0]
      msg     = ast.literal_eval(connex.recv(16384*2).decode())

      if (self.__name == 1) and not(vars.scenaryInit):

        self.__registerLocalities(msg[0])
        self.__registerVoters(msg[1])
        self.__registerCandidates(msg[2])

        connex.send(b'Initialized')

      else:
        voter = msg[0]
        assemblyChoice = msg[1]
        congressChoice = msg[2]

        # Listen 'VotingClosed' event
        # if voting closed:
        #   votingOpen = False
        #   vars.Voting.closeVoting()
        #   connex.close()
        # else:
        
        print(f"\n\t{voter} voting...\n")
        vars.Voting.vote(voter, assemblyChoice, congressChoice, {'from': voter})
        connex.send(b'Voted')


  def __listenCloseVotingEvent():
    pass
