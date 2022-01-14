#!/usr/bin/python3
import secrets


class Voter:

  def __init__(self, voter: int, locality: int, center: int) -> None:
    self.name     = bytes("Votante" + str(voter), 'utf-8')
    self.locality = locality - 1
    self.center   = center
    self.__mail   = str(self.name) + "@gmail.com"
    self.privKey  = "0x" + secrets.token_hex(32)
    self.address  = ""
