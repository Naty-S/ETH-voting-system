

class Center:

  def __init__(self, center: int, locality: str, port:int) -> None:
    self.name       = "Center" + center
    self.locality   = locality
    self.port       = port
    self.voters     = []
    self.localities = []
    self.candidates = []
  

  def registerVoters(self):
    self.voters
  

  def registerLocalities(self):
    self.localities
  

  def registerCandidates(self):
    self.candidates
