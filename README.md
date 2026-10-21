# OntoSim-Dis

*An OWL 2 ontology of disease simulation models.*

OntoSim-Dis est une ontologie OWL 2 DL des modèles de simulation des maladies. Elle décrit un modèle, à compartiments ou multi-agents : sa structure, ses paramètres, son exécution. Elle décrit aussi ce qu'il représente : la maladie, c'est-à-dire ses états de santé, les transitions entre ces états et ce qui gouverne chaque transition, et le contexte pour lequel le modèle a été construit.

Sa distinction centrale porte sur le risque : dépend-il de l'état de la population, comme dans une maladie transmissible, ou seulement de l'individu ? On décrit un modèle et la maladie qu'il représente, et le raisonneur en déduit si la maladie est couplée à la population, et si le modèle réalise ce couplage.

Ce dépôt accompagne la thèse de doctorat de **Paul Cheikh Anta Diouf**,
Université Assane Seck de Ziguinchor, laboratoire LI3.

## Contenu

| Dossier | Contenu |
|---|---|
| `src/ontology/` | les 9 modules de l'ontologie et le fichier ombrelle qui les réunit, en Turtle |
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
| `layer4-checks.ttl` | contrôles entre maladie et modèles : approximations statiques | 3A, 3B, 4-Core |
| `ontosim-dis.ttl` | l'ontologie complète : aucun terme, les métadonnées de l'ensemble | les 9 modules |

## Ouvrir l'ontologie

Ouvrir un module dans [Protégé](https://protege.stanford.edu/) (version 5.6 ou plus récente), directement depuis `src/ontology/` : Protégé trouve dans ce même dossier les modules qu'il importe, grâce au fichier `catalog-v001.xml`. Pour avoir toute l'ontologie d'un coup, ouvrir `ontosim-dis.ttl`.

Raisonneur conseillé : HermiT.

## Licence

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) : réutilisation libre, à condition de citer l'auteur.

<br>

<p align="center">
  🦋<br>
  <i>Fait avec amour et pour l'amour.</i>
</p>