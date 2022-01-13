"""
Definir localidades (localidades.txt)
Generar votantes
Generar centros de votación
Levantar centros de votación

Configurar escenario electoral

Levantar nodos ETH localmente
Definir nodo ETH para cada centro de votación
Iniciar proceso de votación
"""

from src.genCenter import centroVotacion
from src.genVoters import genVotantes


def main():

  genVotantes("-f ../data/localities.txt")
  centroVotacion()
