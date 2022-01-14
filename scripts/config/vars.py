import brownie as br

# Tells if the voting scenary was initialized or not
scenaryInit = False

# Contract can be accesed from any where
Voting = br.Voting.deploy({'from': br.accounts[0]})
