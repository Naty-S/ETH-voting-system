// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.7.0 <0.9.0;


contract Voting {

  enum State { Created, Voting, Closed }

  enum Cargo{
    Asamblea, // 0
    Congreso // 1
  }

  struct Locality {
    bytes32 name;
    uint centers; // number of voting centers
    uint voters;  // number of voters
    uint votes;   // votes made
  }

  struct Center {
    uint name;
    uint locality; // index
  }
  
  struct Voter {
    bytes32 name;
    bool voted;
    uint locality; // index
  }
  
  struct Candidate {
    uint votes;
    Cargo cargo;
  }

  uint public totalVotes;
  State public state;
  Locality[] public localities;

  // Winners by locality, each index represents a locality
  Candidate[] public assemblyReps;
  Candidate[] public congressReps;
  
  // Index locality to candidate
  mapping(uint => Candidate[]) public assemblyCandidates;
  mapping(uint => Candidate[]) public congressCandidates;

  Voter[] private validVoters;
  mapping(address => Voter) private voters;

  modifier inState(State _state) {
    require(state == _state);
    _;
  }

  event VotingClosed();

  // 
  constructor() public {
    state = State.Created;
    totalVotes = 0;
  }


  function reset() public inState(State.Closed) {
    
    state = State.Created;
    totalVotes = 0;

    for (uint i = 0; i < localities.length; i++) {
      
      for (uint j = 0; j < assemblyCandidates[i].length; j++) {
        
        assemblyCandidates[i][j].votes = 0;
      }

      for (uint j = 0; j < congressCandidates[i].length; j++) {
          
        congressCandidates[i][j].votes = 0;
      }
    }

    delete assemblyReps;
    delete congressReps;
  }


  function startVoting() public inState(State.Created) {
    state = State.Voting;
  }


  function registerLocality(bytes32 _name, uint _voters, uint _centers) public inState(State.Created) {

    localities.push(Locality(_name, _centers, _voters, 0));
  }


  function registerVoter(address _voter, bytes32 _name, uint _locality) public inState(State.Created) {

    require(_locality < localities.length, "La localidad no existe");
    Voter memory voter = Voter(_name, false, _locality);
    voters[_voter] = voter;
    validVoters.push(voter);
  }
  

  function registerCandidate(address _candidate, uint _cargo, uint _locality) public inState(State.Created) {
    
    require(_locality < localities.length, "La localidad no existe");
    require(_cargo == 0 || _cargo == 1, "Solo se puede votar por representante de Asamblea o Congreso");
    
    bool candidateIsValid = false;
  
    for (uint i = 0; i < validVoters.length; i++) {
      if (keccak256(abi.encode(voters[_candidate])) == keccak256(abi.encode(validVoters[i]))) {
        candidateIsValid = true;
      }
      
    }
    require(candidateIsValid, "El candidato debe ser un votante valido");

    if (_cargo == 0) {
      assemblyCandidates[_locality].push(Candidate(0, Cargo.Asamblea));
    } else {
      congressCandidates[_locality].push(Candidate(0, Cargo.Congreso));
    }
  }


  function vote(address _voter, uint _cargo, uint _choice) public inState(State.Voting) {
    
    require(!voters[_voter].voted, "Votante ya ejercio su derecho al voto");
    require(_cargo == 0 || _cargo == 1, "Solo se puede votar por representante de Asamblea o Congreso");
    // _choice < length

    voters[_voter].voted = true;
    localities[voters[_voter].locality].votes++;
    totalVotes++;
    
    if (_cargo == 0) {
      assemblyCandidates[voters[_voter].locality][_choice].votes++;
    } else {
      congressCandidates[voters[_voter].locality][_choice].votes++;
    }
  }

  // Close voting and select winner by locality
  function closeVoting() public inState(State.Voting) {
    
    state = State.Closed;
    emit VotingClosed();

    uint assemblyVotes = 0;
    uint congressVotes = 0;
    Candidate memory assemblyRep;
    Candidate memory congressRep;

    for (uint i = 0; i < localities.length; i++) {
      
      for (uint j = 0; j < assemblyCandidates[i].length; j++) {
        
        if (assemblyCandidates[i][j].votes > assemblyVotes) {
            
          assemblyVotes = assemblyCandidates[i][j].votes;
          assemblyRep   = assemblyCandidates[i][j];
        }
      }
      assemblyReps.push(assemblyRep);

      for (uint j = 0; j < congressCandidates[i].length; j++) {
          
        if (congressCandidates[i][j].votes > congressVotes) {
          
          congressVotes = congressCandidates[i][j].votes;
          congressRep   = congressCandidates[i][j];
        }
      }
      congressReps.push(congressRep);
    }
  }

  // Winners and abstention % by locality
  function resume() public view inState(State.Closed)
    returns(
      uint[] memory assemblyRepsVotes,
      uint[] memory congressRepsVotes,
      uint[] memory abstentions
    )
  {
    assemblyRepsVotes = new uint[](localities.length);
    congressRepsVotes = new uint[](localities.length);
    abstentions = new uint[](localities.length);

    for (uint i = 0; i < localities.length; i++) {

      assemblyRepsVotes[i] = localities[i].votes / assemblyReps[i].votes;
      congressRepsVotes[i] = localities[i].votes / congressReps[i].votes;
      abstentions[i] = localities[i].voters / localities[i].votes;
    }
  }
  
  // Winners votes count and abstention by locality
  function report() public view inState(State.Closed)
    returns(
      uint[] memory assemblyRepsVotes,
      uint[] memory congressRepsVotes,
      uint[] memory abstentions
    )
  {
    assemblyRepsVotes = new uint[](localities.length);
    congressRepsVotes = new uint[](localities.length);
    abstentions = new uint[](localities.length);

    for (uint i = 0; i < localities.length; i++) {

      assemblyRepsVotes[i] = assemblyReps[i].votes;
      congressRepsVotes[i] = congressReps[i].votes;
      abstentions[i] = localities[i].voters - localities[i].votes;
    }
  }
}
