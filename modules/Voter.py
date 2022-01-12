import eth_keys      as eth


class Voter:

  def __init__(self, voter: int, locality: str, center: int, cargo: int = -1) -> None:
    self.center   = "Centro" + center
    self.locality = locality
    self.name     = "Votante" + voter
    # Asamblea 0, Congreso 1
    self.cargo    = cargo
    self.wei      = 10000000
    self.mail     = self.name + "@gmail.com"
    self.privKey  = eth.keys.PrivateKey(b'\x01' * 32)
    self.publKey  = self.privKey.public_key
    self.address  = self.publKey.to_checksum_address()
