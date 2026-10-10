# OntoSim-Dis

*An OWL 2 ontology of diseases and of the simulation models that represent them.*

OntoSim-Dis est une ontologie OWL 2 DL. Elle décrit une maladie, c'est-à-dire ses états de santé, les transitions entre ces états et ce qui gouverne chaque transition. Elle décrit aussi les modèles de simulation qui représentent cette maladie : modèles à compartiments et modèles multi-agents.

Sa distinction centrale porte sur le risque : dépend-il de l'état de la population, comme dans une maladie transmissible, ou seulement de l'individu ? On décrit les transitions d'une maladie et le raisonneur en déduit si elle est couplée à la population.

Ce dépôt accompagne la thèse de doctorat de **Paul Cheikh Anta Diouf**,
Université Assane Seck de Ziguinchor, laboratoire LI3.

## Contenu

| Dossier | Contenu |
|---|---|
| `src/ontology/` | les 8 modules de l'ontologie, en Turtle |
| `tests/` | des cas de test à ouvrir avec l'ontologie |
| `tools/` | les scripts de vérification |
| `docs/` | les documents de conception |

## Les modules

| Fichier | Contenu | Importe |
|---|---|---|
| `layer1_foundational.ttl` | termes repris de BFO, RO et IAO | — |
| `layer2_modsim.ttl` | modélisation et simulation, communes à tous les types de modèles | couche 1 |
| `layer3a_mas.ttl` | modèles multi-agents | couche 2 |
| `layer3b_equations.ttl` | modèles à compartiments | couche 2 |
| `layer4-ogms.ttl` | termes repris d'OGMS | couche 1 |
| `layer4_core.ttl` | la maladie : états de santé, transitions, déterminants | couche 2, OGMS |
| `layer4_infectious.ttl` | maladies transmissibles : pathogène, voie de transmission, réservoir | 4-Core |
| `layer4-context.ttl` | contexte : population, région, climat, structures de santé | couche 2 |

## Ouvrir l'ontologie

Ouvrir un module dans [Protégé](https://protege.stanford.edu/) (version 5.6 ou plus récente), directement depuis `src/ontology/` : Protégé trouve dans ce même dossier les modules qu'il importe.

Raisonneur conseillé : HermiT.

## Licence

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) : réutilisation libre, à condition de citer l'auteur.

<br>

<p align="center">
  🦋<br>
  <i>Fait avec amour et pour l'amour.</i>
</p>