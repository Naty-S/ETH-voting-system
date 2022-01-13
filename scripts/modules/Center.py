import ast, socket, threading
import brownie as br


class Center:

  def __init__(self, center: int, locality: int, port:int) -> None:
    self.__name         = center
    self.__locality     = locality
    self.__port         = port
    self.__socket       = socket.socket()
    self.__netListenerT = threading.Thread(name=self.__name+"-netListener", target=self.__netListener)
  
    # Start server
    self.__socket.bind((b'localhost', self.__port))
    self.__netListenerT.start()
  

  def __registerLocalities(self, localities):

    for l in localities:
      voters = l[0]
      br.Voting.registerLocality(l, voters)


  def __registerVoters(self, voters):

    for v in voters:
      br.Voting.registerVoters(v.address, v.name, v.locality[-1])
  

  def __registerCandidates(self, candidates):

    for c in candidates[0]:
      br.Voting.registerCandidate(c.address, c.name, 0, c.locality)

    for c in candidates[1]:
      br.Voting.registerCandidate(c.address, c.name, 1, c.locality)


  def __netListener(self) -> None:

    self.__socket.listen(5)

    while True:
      connex  = self.__socket.accept()[0]
      msg     = ast.literal_eval(connex.recv(8192).decode())

      if msg[0] == "Init":

        self.__registerLocalities(msg[1])
        self.__registerVoters(msg[2])
        self.__registerCandidates(msg[1], msg[3])
