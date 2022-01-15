#!/usr/bin/python3
import scripts.config.vars   as vars


def visualizer():
  
  assemblyRepsVotesR, congressRepsVotesR, abstentionsR, assemblyRepsR, congressRepsR = vars.Voting.resume()
  assemblyRepsVotes, congressRepsVotes, abstentions, assemblyReps, congressReps = vars.Voting.report()
  
  print("\nResumen:")
  
  for i in range(len(assemblyRepsVotesR)):
    print(f"\nLocalidad {i}:\n\
      El ganador a representante de asamblea '{(assemblyRepsR[i]).decode()}' recibio {assemblyRepsVotesR[i]}% de los votos\n\
      El ganador a representante de congreso '{(congressRepsR[i]).decode()}' recibio {congressRepsVotesR[i]}% de los votos\n\
      Abtinencias: {abstentionsR[i]}%\
    \n")
  
  print("\nReporte:")
  
  for i in range(len(assemblyRepsVotes)):
    print(f"\nLocalidad {i}:\n\
      El ganador a representante de asamblea '{(assemblyReps[i]).decode()}' recibio {assemblyRepsVotes[i]} votos\n\
      El ganador a representante de congreso '{(congressReps[i]).decode()}' recibio {congressRepsVotes[i]} votos\n\
      Abtinencias: {abstentions[i]}\
    \n")
