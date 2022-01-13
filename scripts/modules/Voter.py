import eth_keys      as eth


class Voter:

  def __init__(self, voter: int, locality: str, center: int) -> None:
    self.name       = "Votante" + voter
    self.locality   = locality
    self.center     = center
    self.__mail     = self.name + "@gmail.com"
    self.privKey    = eth.keys.PrivateKey(b'\x01' * 32)
    # self.__publKey  = self.privKey.public_key
    # self.address    = self.publKey.to_checksum_address()
    self.address    = ""
