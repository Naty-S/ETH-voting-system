import eth_keys      as eth

import modules.Vote as vote

class Voter:

  def __init__(self, voter:int, locality: str, center: int) -> None:
    self.center   = "Centro" + center
    self.locality = locality
    self.name     = "Votante" + voter
    self.wei      = 10000000
    self.mail     = self.name + "@gmail.com"
    self.privKey  = eth.keys.PrivateKey(b'\x01' * 32)
    self.publKey  = self.privKey.public_key
    self.address  = self.publKey.to_checksum_address()
    self.vote     = None
  

  def vote(self):
    self.vote = vote.Vote()
