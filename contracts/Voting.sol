// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.8.0 <0.9.0;


contract Voting {

  enum State { Created, Voting, Closed }

  struct Locality {
    uint name;
    uint voters;  // number of voters
    uint votes;   // votes made
  }

  struct Voter {
    bytes32 name;
    bool voted;
    uint locality; // index
  }
  
  struct Candidate {
    bytes32 name;
    uint votes;
    uint cargo; // Asamblea = 1, Congreso = 2
  }

  // Votes done in the voting process
  uint public totalVotes;
  // State of the contract
  State public state;
  Locality[] public localities;

  // Winners by locality, each index represents a locality
  Candidate[] public assemblyReps;
  Candidate[] public congressReps;
  
  // Given the index in localities, returns its candidates
  mapping(uint => Candidate[]) public assemblyCandidates;
  mapping(uint => Candidate[]) public congressCandidates;

  Voter[] private validVoters;
  mapping(address => Voter) private voters;


  // Modifiers
  modifier inState(State _state) {
    require(state == _state, "No se puede ejecutar si el estado no es el correcto");
    _;
  }

  modifier localitiesRegistered() {
    require(localities.length > 0, "Las localidades no se han registrado");
    _;
  }

  modifier votersRegistered() {
    require(validVoters.length > 0, "Los votantes no se han registrado");
    _;
  }


  // Events
  event VoterVoted();
  event VotingClosed();


  // 
  constructor() {
    state = State.Created;
    totalVotes = 0;
  }


  function reset() public {
    
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


  function registerLocality(uint _name, uint _voters) public inState(State.Created) {

    localities.push(Locality(_name, _voters, 0));
  }


  function registerVoter(address _voter, bytes32 _name, uint _locality)
    public
    inState(State.Created)
    localitiesRegistered()
  {
    require(_locality < localities.length, "La localidad no existe");
    Voter memory voter = Voter(_name, false, _locality);
    voters[_voter] = voter;
    validVoters.push(voter);
  }
  

  function registerCandidate(address _candidate, bytes32 _name, uint _cargo, uint _locality)
    public
    inState(State.Created)
    votersRegistered()
  {
    require(_locality < localities.length, "La localidad no existe");
    require(_cargo == 1 || _cargo == 2, "Solo se puede registrar representante de Asamblea o Congreso");
    
    bool candidateIsValid = false;
  
    for (uint i = 0; i < validVoters.length; i++) {
      if (keccak256(abi.encode(voters[_candidate])) == keccak256(abi.encode(validVoters[i]))) {
        candidateIsValid = true;
      }
    }
    require(candidateIsValid, "El candidato debe ser un votante valido");

    Candidate memory candidate = Candidate(_name, 0, _cargo);

    if (_cargo == 1) {
      assemblyCandidates[_locality].push(candidate);
    } else {
      congressCandidates[_locality].push(candidate);
    }
  }


  function vote(address _voter, uint _assemblyChoice, uint _congressChoice) public inState(State.Voting) {
    
    require(!voters[_voter].voted, "Votante ya ejercio su derecho al voto");
    require(_assemblyChoice < assemblyCandidates[voters[_voter].locality].length, "El candidato no existe");
    require(_congressChoice < congressCandidates[voters[_voter].locality].length, "El candidato no existe");

    voters[_voter].voted = true;
    totalVotes += 1;
    localities[voters[_voter].locality].votes += 1;
    assemblyCandidates[voters[_voter].locality][_assemblyChoice].votes += 1;
    congressCandidates[voters[_voter].locality][_congressChoice].votes += 1;
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
      uint[] memory abstentions,
      bytes32[] memory assemblyRepsNames,
      bytes32[] memory congressRepsNames
    )
  {
    assemblyRepsVotes = new uint[](localities.length);
    congressRepsVotes = new uint[](localities.length);
    abstentions       = new uint[](localities.length);
    assemblyRepsNames = new bytes32[](localities.length);
    congressRepsNames = new bytes32[](localities.length);

    for (uint i = 0; i < localities.length; i++) {

      assemblyRepsVotes[i] = assemblyReps[i].votes * 100 / localities[i].voters;
      congressRepsVotes[i] = congressReps[i].votes * 100 / localities[i].voters;
      abstentions[i]       = ((localities[i].voters - localities[i].votes) * 100) / localities[i].voters;
      assemblyRepsNames[i] = assemblyReps[i].name;
      congressRepsNames[i] = congressReps[i].name;
    }
    return (assemblyRepsVotes, congressRepsVotes, abstentions, assemblyRepsNames, congressRepsNames);
  }
  
  // Partial results and abstention by locality
  function report() public view inState(State.Closed)
    returns(
      uint[] memory assemblyRepsVotes,
      uint[] memory congressRepsVotes,
      uint[] memory abstentions,
      bytes32[] memory assemblyRepsNames,
      bytes32[] memory congressRepsNames
    )
  {
    assemblyRepsVotes = new uint[](localities.length);
    congressRepsVotes = new uint[](localities.length);
    abstentions       = new uint[](localities.length);
    assemblyRepsNames = new bytes32[](localities.length);
    congressRepsNames = new bytes32[](localities.length);

    for (uint i = 0; i < localities.length; i++) {

      assemblyRepsVotes[i] = assemblyReps[i].votes;
      congressRepsVotes[i] = congressReps[i].votes;
      abstentions[i]       = localities[i].voters - localities[i].votes;
      assemblyRepsNames[i] = assemblyReps[i].name;
      congressRepsNames[i] = congressReps[i].name;
    }

    return (assemblyRepsVotes, congressRepsVotes, abstentions, assemblyRepsNames, congressRepsNames);
  }
}
