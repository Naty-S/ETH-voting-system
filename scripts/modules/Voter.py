#!/usr/bin/python3
import eth_keys      as eth


class Voter:

  def __init__(self, voter: int, locality: int, center: int) -> None:
    self.name       = bytes("Votante" + voter, 'utf-8')
    self.locality   = locality
    self.center     = center
    self.__mail     = self.name + "@gmail.com"
    self.privKey    = eth.keys.PrivateKey(b'\x01' * 32)
    self.address    = ""
