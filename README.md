\# OntoSim-Dis



\*An OWL 2 ontology of diseases and of the simulation models that represent them.\*



OntoSim-Dis est une ontologie OWL 2 DL. Elle décrit une maladie, c'est-à-dire ses états de santé, les transitions entre ces états et ce qui gouverne chaque transition. Elle décrit aussi les modèles de simulation qui représentent cette maladie : modèles à compartiments et modèles multi-agents.



Sa distinction centrale porte sur le risque : dépend-il de l'état de la population, comme dans une maladie transmissible ou seulement de l'individu ? On décrit les transitions d'une maladie et le raisonneur en déduit si elle est couplée à la population.



Ceci est la these de mon doctorat et mon nom est Paul Cheikh Anta Diouf.
Université Assane Seck de Ziguinchor, laboratoire LI3.



\## Contenu



| Dossier | Contenu |

|---|---|

| `src/ontology/` | les 8 modules de l'ontologie, en Turtle |

| `tests/` | des cas de test à ouvrir avec l'ontologie |

| `tools/` | les scripts de vérification |

| `docs/` | les documents de conception |



\## Les modules



| Fichier | Contenu | Importe |

|---|---|---|

| `layer1\_foundational.ttl` | termes repris de BFO, RO et IAO | — |

| `layer2\_modsim.ttl` | modélisation et simulation, communes à tous les types de modèles | couche 1 |

| `layer3a\_mas.ttl` | modèles multi-agents | couche 2 |

| `layer3b\_equations.ttl` | modèles à compartiments | couche 2 |

| `layer4-ogms.ttl` | termes repris d'OGMS | couche 1 |

| `layer4\_core.ttl` | la maladie : états de santé, transitions, déterminants | couche 2, OGMS |

| `layer4\_infectious.ttl` | maladies transmissibles : pathogène, voie de transmission, réservoir | 4-Core |

| `layer4-context.ttl` | contexte : population, région, climat, structures de santé | couche 2 |



\## Ouvrir l'ontologie



Ouvrir un module dans Protégé (version 5.6 ou plus récente), directement depuis `src/ontology/` : Protégé trouve dans ce même dossier les modules qu'il importe. Raisonneur conseillé : HermiT.



\## Licence



\[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) : réutilisation libre, à condition de citer l'auteur.



<br>

<p align="center">
  🦋<br>
  <i>Fais avec Amour et pour l'Amour.</i>
</p>
