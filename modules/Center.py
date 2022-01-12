import ast, threading
import brownie as br

class Center:

  def __init__(self, center: int, locality: str, port:int) -> None:
    self.__name         = center
    self.__locality     = locality
    self.__port         = port
    self.__voters       = []
    self.__localities   = []
    self.__candidates   = []
    self.__netListenerT = threading.Thread(name=self.__name+"-netListener", target=self.__netListener)
  

  def registerVoters(self, voters):
    self.__voters = voters
  

  def registerLocalities(self, localities):
    self.__localities = localities
  

  def registerCandidates(self, candidates):
    self.__candidates = candidates


  def __netListener(self) -> None:

    self.__socket.listen(5)

    while True:
      connex  = self.__socket.accept()[0]
      msg     = ast.literal_eval(connex.recv(8192).decode())
      request = msg[0]

      # if centro1 => config escenario
