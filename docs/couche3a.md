# OntoSim-Dis — Couche 3A : paradigme multi-agents

**Fichier :** `src/ontology/layer3a_mas.ttl`
**IRI :** `https://w3id.org/ontosim-dis/layer3a` — version `https://w3id.org/ontosim-dis/layer3a/1.0`
**Importe :** `https://w3id.org/ontosim-dis/layer2/1.0`
**Licence :** CC BY 4.0
**Statut :** prête à être fermée à la version 1.0, après correction des guillemets d'en-tête.

## Rôle

La couche 3A dit **comment** un modèle multi-agents est construit : des agents autonomes,
chacun suivant son comportement, qui interagissent et dont les interactions produisent le
comportement du système.

**Elle ne dit jamais quelle maladie le modèle représente** (décision D9). C'est pour cela que
`HumanAgent`, `VectorAgent`, `Susceptible`, `Infectious` et `Recovered` ont quitté cette couche :
ce sont des connaissances sur la maladie, elles appartiennent à la couche 4.

**Conséquence chiffrée de ce nettoyage :** 3A est passée de 58 à 10 classes.

## Contenu

**10 classes, 7 propriétés d'objet, 5 propriétés de données, 1 classe définie, 4 restrictions,
1 disjonction, 1 alignement.** 161 triplets.

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
| `InteractionTriggeredTransition` | `AgentTransition` | `triggeredBy` au moins 1 `InteractionType` |

Les deux sont **déclarées disjointes** : une transition ne peut pas être à la fois déterminée
par les seuls attributs de l'agent et déclenchée par une interaction avec un autre.

`AttributeDrivenTransition` est la progression individuelle : l'âge de l'agent, le temps passé
dans son état courant. `InteractionTriggeredTransition` est le couplage : il faut un autre agent.

### La classe définie

```
CoupledAgentBasedModel ≡ AgentBasedModel and (hasAgentTransition some InteractionTriggeredTransition)
```

**C'est la forme multi-agents du critère de couplage.** Un modèle dont au moins une transition
d'agent est déclenchée par une interaction est reconnu couplé par le raisonneur, sans qu'on
l'ait écrit. C'est le pendant exact de `CoupledCompartmentalModel` en 3B, qui passe par un taux
dépendant d'un compartiment.

Le parent explicite `AgentBasedModel` est conservé en plus de l'équivalence : redondant pour le
raisonneur, mais lisible dans Protégé sans lancer HermiT. Choix assumé, appliqué de la même
façon en 3B.

### `triggeredBy min 1 InteractionType` — retirée, puis remise

Cette restriction a été enlevée une première fois, puis rétablie. Sans elle,
`InteractionTriggeredTransition` n'est qu'une étiquette qu'on colle à la main et `triggeredBy`
reste décorative : rien n'oblige à dire *quelle* interaction déclenche la transition.

**Limite connue** Cette restriction impose qu'il existe au moins une
interaction, mais en monde ouvert elle n'oblige pas à la déclarer : une transition marquée
`InteractionTriggeredTransition` sans interaction nommée reste acceptée. C'est le même phénomène
que la limite L1 du registre.

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

**Résultat au 2026-10-08 : 2 erreurs, 3 avertissements.**

Les deux erreurs sont les guillemets d'en-tête, lignes 15 et 26 — tenue de dossier, Partie IX.1
du registre.

Les trois avertissements signalent `hasAgentState`, `hasEnvironmentModel` et `involvesAgentType`
comme déclarées sans apparaître dans un axiome. **Conservées sciemment** : elles servent à
décrire un modèle, elles ne servent pas au raisonnement. La revue finale des propriétés
décoratives tranchera leur sort.

HermiT : aucune classe insatisfiable.

```
python3 tools/audit_ontosim.py --focus layer3a_mas.ttl \
    --load layer1_foundational.ttl layer2_modsim.ttl layer3a_mas.ttl \
    --ref tools/refs/*.owl
```

### 2. Test de classification

Un modèle multi-agents déclarant une transition déclenchée par interaction doit être classé
`CoupledAgentBasedModel` par le raisonneur, sans qu'on l'ait écrit. Un modèle dont toutes les
transitions sont pilotées par attribut ne doit pas l'être.

### 3. Test du garde-fou

Une transition déclarée à la fois `AttributeDrivenTransition` et
`InteractionTriggeredTransition` doit rendre l'ontologie incohérente. **Vérifié.**

### 4. OOPS!

A FAIRE
---

## Décisions consignées

| Code | Décision |
|---|---|
| D9 | La couche 3 ne décrit que des paradigmes, jamais de maladie. 58 classes → 10. |
| — | Disjonction des deux sortes de transition : garde-fou vérifié. |
| — | `triggeredBy min 1 InteractionType` rétablie : sans elle, la classe définie n'est qu'une étiquette. |
| — | Parent explicite conservé sur la classe définie, de façon cohérente avec 3B. |
| — | Trois propriétés sans axiome conservées : utilisables pour décrire, inutiles au raisonnement. |

## Décisions ouvertes

| Code | Question | À trancher lors de |
|---|---|---|
| D4 | Un agent participe-t-il directement à la simulation ? En BFO, une information n'agit pas : c'est sa réalisation concrète qui participe à un processus. Si `AgentType` est la **description** d'un agent, il ne participe pas. | Reprise de cette couche |
| — | Sort de `hasAgentState`, `hasEnvironmentModel`, `involvesAgentType` | Revue finale |

---

## Versionnement

```
git add src/ontology/layer3a_mas.ttl docs/couche3a.md
git commit -m "layer3a : corrige les guillemets dans created et versionInfo"
```

Le numéro de version suit l'empilement entier, pas ce fichier seul.

<br>

<p align="center">
  🦋<br>
  <i>Fais avec amour et pour l'Amour.</i>
</p>