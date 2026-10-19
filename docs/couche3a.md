# OntoSim-Dis — Couche 3A : paradigme multi-agents

**Fichier :** `src/ontology/layer3a_mas.ttl`
**IRI :** `https://w3id.org/ontosim-dis/layer3a` — version `https://w3id.org/ontosim-dis/layer3a/1.0`
**Importe :** `https://w3id.org/ontosim-dis/layer2/1.0`
**Licence :** CC BY 4.0
**Statut :** contenu modifié depuis la 1.0 (octobre 2026 : `InteractionTriggeredTransition`
devient une classe définie), numéro encore à 1.0. Voir *Versionnement*.

## Rôle

La couche 3A dit **comment** un modèle multi-agents est construit : des agents autonomes,
chacun suivant son comportement, qui interagissent et dont les interactions produisent le
comportement du système.

**Elle ne dit jamais quelle maladie le modèle représente** (décision D9). C'est pour cela que
`HumanAgent`, `VectorAgent`, `Susceptible`, `Infectious` et `Recovered` ont quitté cette couche :
ce sont des connaissances sur la maladie, elles appartiennent à la couche 4.

**Conséquence chiffrée de ce nettoyage :** 3A est passée de 58 à 10 classes.

## Contenu

**10 classes, 7 propriétés d'objet, 5 propriétés de données, 2 classes définies, 4 restrictions,
1 disjonction, 1 alignement.** 166 triplets. L'index des termes en compte 22.

### Le modèle et ses pièces

| Classe | Parent (couche 2) | Ce qu'elle impose |
|---|---|---|
| `AgentBasedModel` | `SimulationModel` | au moins 1 type d'agent ; au moins 1 comportement |
| `AgentType` | `ModelComponent` | — |
| `AgentState` | `StateComponent` | — |
| `AgentTransition` | `TransitionComponent` | hérite : exactement 1 état de départ et 1 d'arrivée |
| `Behavior` | `RuleComponent` | — |
| `EnvironmentModel` | `EnvironmentComponent` | — |
| `InteractionType` | `ModelComponent` | — |

Chaque classe se rattache à une classe de la couche 2 au lieu de redéfinir sa structure. C'est
ce qui fait qu'une transition d'agent a déjà un état de départ et un état d'arrivée sans qu'on
ait rien écrit ici.

### Les deux sortes de transition -- le cœur de la couche

| Classe | Parent | Ce qu'elle impose |
|---|---|---|
| `AttributeDrivenTransition` | `AgentTransition` | — |
| `InteractionTriggeredTransition` | `AgentTransition` | **classe définie** : toute transition d'agent déclenchée par au moins 1 `InteractionType` |

Les deux sont **déclarées disjointes** : une transition ne peut pas être à la fois déterminée
par les seuls attributs de l'agent et déclenchée par une interaction avec un autre.

`AttributeDrivenTransition` est la progression individuelle : l'âge de l'agent, le temps passé
dans son état courant. `InteractionTriggeredTransition` est le couplage : il faut un autre agent.

Conséquence de la disjonction et de la définition : une transition déclarée
`AttributeDrivenTransition` qui nomme une interaction déclenchante rend l'ontologie
incohérente. Le raisonneur la classe aussi `InteractionTriggeredTransition`, et les deux
s'excluent.

### Les deux classes définies

```
InteractionTriggeredTransition ≡ AgentTransition and (triggeredBy some InteractionType)
CoupledAgentBasedModel ≡ AgentBasedModel and (hasAgentTransition some InteractionTriggeredTransition)
```

Le raisonneur fait les deux pas : une transition d'agent qui nomme l'interaction qui la
déclenche est classée `InteractionTriggeredTransition`, puis son modèle est classé
`CoupledAgentBasedModel`.

**C'est la forme multi-agents du critère de couplage.** Un modèle dont au moins une transition
d'agent est déclenchée par une interaction est reconnu couplé par le raisonneur, sans qu'on
l'ait écrit. C'est le pendant exact de `CoupledCompartmentalModel` en 3B, qui passe par un taux
dépendant d'un compartiment.

Le parent explicite est conservé en plus de l'équivalence sur les deux classes : redondant pour
le raisonneur, mais lisible dans Protégé sans lancer HermiT. Choix assumé, appliqué de la même
façon en 3B.

### `triggeredBy` : de la restriction à la définition

La restriction `triggeredBy min 1 InteractionType` a été enlevée une première fois, puis
rétablie : sans elle, `InteractionTriggeredTransition` n'était qu'une étiquette qu'on colle à
la main et `triggeredBy` restait décorative. Le 15 octobre 2026 (correction 8), la condition
est passée dans la définition de la classe : elle n'est plus seulement imposée, elle suffit
pour classer.

**Limite connue.** En monde ouvert, le raisonneur ne conclut pas l'inverse : une transition
d'agent qui ne nomme aucune interaction n'est pas classée `AttributeDrivenTransition` pour
autant ; il faut le déclarer. Et une transition déclarée `InteractionTriggeredTransition` à la
main sans interaction nommée reste acceptée : l'interaction existe, on ne sait pas laquelle.
C'est le même phénomène que la limite L1 du registre.

### Lien avec 4-Checks

3A n'importe pas la couche 4. C'est le module 4-Checks (correction 9, 15 octobre 2026) qui
importe 3A, 3B et 4-Core et qui se sert de `AttributeDrivenTransition` :

```
StaticApproximationAgentTransition ≡ AttributeDrivenTransition
                                     and (representsStateTransition some CoupledTransition)
```

Une transition d'agent pilotée par les seuls attributs, qui représente une transition couplée
de la maladie, est une **approximation statique** : le modèle ignore le couplage. Son modèle
est classé `StaticApproximationModel`. C'est un signalement, pas une erreur : l'approximation
peut convenir à la question posée. Une transition d'agent qui ne nomme aucune interaction et
n'est pas déclarée pilotée par attribut ne donne rien : ni couplée, ni approximation.

### 7 propriétés d'objet

| Propriété | Domaine → Portée | Caractéristique |
|---|---|---|
| `hasAgentType` | AgentBasedModel → AgentType | — |
| `hasAgentTransition` | AgentBasedModel → AgentTransition | — |
| `hasBehavior` | AgentBasedModel → Behavior | — |
| `triggeredBy` | AgentTransition → InteractionType | — |
| `hasAgentState` | AgentType → AgentState | — |
| `hasEnvironmentModel` | AgentBasedModel → EnvironmentModel | fonctionnelle |
| `involvesAgentType` | InteractionType → AgentType | — |

### 5 propriétés de données

| Propriété | Sur | Type |
|---|---|---|
| `agentTypeName` | AgentType | chaîne |
| `initialAgentCount` | AgentType | entier |
| `behaviorExpression` | Behavior | chaîne |
| `contactRatePerDay` | InteractionType | double |
| `interactionProbability` | InteractionType | double |

### Alignement

| OntoSim-Dis | OSDi | Type |
|---|---|---|
| `AgentBasedModel` | `osdi:AgentBasedModel` | exactMatch |

Un seul alignement, mais c'est un `exactMatch` sur la classe qui compte.

---

## Validation

### 1. Audit automatique

**Résultat au 19 octobre 2026 : 0 erreur, 3 avertissements.** 166 triplets. HermiT : aucune
classe insatisfiable. Les deux erreurs du 8 octobre (les guillemets d'en-tête) ont été
corrigées.

Les trois avertissements signalent `hasAgentState`, `hasEnvironmentModel` et `involvesAgentType`
comme déclarées sans apparaître dans un axiome. **Conservées sciemment** : elles servent à
décrire un modèle, elles ne servent pas au raisonnement. La revue finale des propriétés
décoratives tranchera leur sort.

Pour reproduire, depuis la racine du dépôt : `bash tools/audit_tout.sh`, ou pour 3A seule :

```
python tools/audit_ontosim.py --focus src/ontology/layer3a_mas.ttl \
    --load src/ontology/layer1_foundational.ttl src/ontology/layer2_modsim.ttl src/ontology/layer3a_mas.ttl \
    --ref tools/ref/ro.owl tools/ref/iao.owl tools/ref/bfo.owl tools/ref/ogms-edit.owl
```

### 2. Test de classification

Un modèle multi-agents déclarant une transition déclenchée par interaction doit être classé
`CoupledAgentBasedModel` par le raisonneur, sans qu'on l'ait écrit. Un modèle dont toutes les
transitions sont pilotées par attribut ne doit pas l'être. **Vérifié le 19 octobre 2026**, avec
HermiT : la transition qui nomme son interaction est classée `InteractionTriggeredTransition`,
son modèle `CoupledAgentBasedModel` ; le modèle à transitions pilotées par attribut ne l'est
pas.

### 3. Test du garde-fou

Une transition déclarée à la fois `AttributeDrivenTransition` et
`InteractionTriggeredTransition` doit rendre l'ontologie incohérente. **Vérifié le
19 octobre 2026**, comme le cas d'une transition `AttributeDrivenTransition` qui nomme une
interaction déclenchante.

### 4. OOPS!

A FAIRE

Soumettre le fichier sur https://oops.linkeddata.es et sauvegarder le rapport. Défauts
probables : les mêmes qu'en couche 2, inverses non déclarés (P13) et espaces de noms
extérieurs (P40), avec la même réponse. Toutes les propriétés ont un domaine et une portée.

---

## Décisions consignées

| Code | Décision |
|---|---|
| D9 | La couche 3 ne décrit que des paradigmes, jamais de maladie. 58 classes → 10. |
| — | Disjonction des deux sortes de transition : garde-fou vérifié. |
| — | `triggeredBy min 1 InteractionType` rétablie : sans elle, `InteractionTriggeredTransition` n'est qu'une étiquette. |
| — | `InteractionTriggeredTransition` devient une classe définie (correction 8, 15 octobre 2026) : le raisonneur la reconnaît d'après l'interaction qui la déclenche. |
| — | Parent explicite conservé sur les classes définies, de façon cohérente avec 3B. |
| — | Trois propriétés sans axiome conservées : utilisables pour décrire, inutiles au raisonnement. |

D4 (un agent participe-t-il directement à la simulation ?) est **sans objet** : en BFO, une
information n'agit pas, et `AgentType` est la description d'une catégorie d'agents, pas un
agent qui participe à une exécution. `participates in` a d'ailleurs été retiré de la couche 1.

## Décisions ouvertes

| Code | Question | À trancher lors de |
|---|---|---|
| — | Sort de `hasAgentState`, `hasEnvironmentModel`, `involvesAgentType` | Revue finale |

---

## Versionnement

Le numéro de version suit l'empilement entier, pas ce fichier seul. Le contenu a changé depuis
la 1.0 (classe définie, correction 8) : la couche passera à 1.1 avec les autres, en un seul
geste. Voir la fiche de la couche 2, *Versionnement*.

<br>

<p align="center">
  🦋<br>
  <i>Fais avec amour et pour l'Amour.</i>
</p>