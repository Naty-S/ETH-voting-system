import eth_keys      as eth


class Voter:

  def __init__(self, voter: int, locality: str, center: int, cargo: int = -1) -> None:
    # Asamblea 0, Congreso 1
    self.cargo      = cargo
    self.__locality = locality
    self.__center   = center
    self.__name     = "Votante" + voter
    self.__wei      = 10000000
    self.__mail     = self.name + "@gmail.com"
    self.__privKey  = eth.keys.PrivateKey(b'\x01' * 32)
    self.__publKey  = self.privKey.public_key
    self.__address  = self.publKey.to_checksum_address()
