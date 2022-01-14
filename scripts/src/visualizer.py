#!/usr/bin/python3
import scripts.config.vars   as vars


def visualizer():
  
  assemblyRepsVotesR, congressRepsVotesR, abstentionsR, assemblyRepsR, congressRepsR = vars.Voting.resume()
  assemblyRepsVotes, congressRepsVotes, abstentions, assemblyReps, congressReps = vars.Voting.report()
  
  print("\nResumen:")
  
  for i in range(len(assemblyRepsVotesR)):
    print(f"\nLocalidad {i}:\n\
      % Votos representante de asamblea '{(assemblyRepsR[i]).decode()}': {assemblyRepsVotesR[i]}\n\
      % Votos representante de congreso '{(congressRepsR[i]).decode()}': {congressRepsVotesR[i]}\n\
      % Abtinencias: {abstentionsR[i]}\
    \n")
  
  print("\nReporte:")
  
  for i in range(len(assemblyRepsVotes)):
    print(f"\nLocalidad {i}:\n\
      Votos representante de asamblea '{(assemblyReps[i]).decode()}': {assemblyRepsVotes[i]}\n\
      Votos representante de congreso '{(congressReps[i]).decode()}': {congressRepsVotes[i]}\n\
      Abtinencias: {abstentions[i]}\
    \n")
