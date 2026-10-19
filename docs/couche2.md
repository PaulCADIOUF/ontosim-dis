# OntoSim-Dis — Couche 2 : modélisation et simulation

**Fichier :** `src/ontology/layer2_modsim.ttl`
**IRI :** `https://w3id.org/ontosim-dis/layer2` — version `https://w3id.org/ontosim-dis/layer2/1.0`
**Importe :** `https://w3id.org/ontosim-dis/layer1/1.0`
**Licence :** CC BY 4.0
**Statut :** contenu de la v1.1, numéro encore à 1.0. Voir *Versionnement*.


## Rôle

La couche 2 répond à la question : **comment modéliser ?** Elle contient les concepts de
simulation communs à tous les paradigmes et indépendants de tout domaine médical. **Aucun terme
de cette couche ne parle de maladie.**

## Contenu

**34 classes, 19 propriétés d'objet, 27 propriétés de données, 25 individus, 8 classes définies,
24 restrictions, 13 alignements.** 893 triplets. L'index des termes en compte 105.

### Racine et modèle

| Classe | Parent | Ce qu'elle impose |
|---|---|---|
| `SimulationKnowledgeArtifact` | `IAO:information content entity` | — |
| `SimulationModel` | `SimulationKnowledgeArtifact` | exactement 1 structure ; au moins 1 paramètre ; au moins 1 méthode de validation ; au moins 1 scénario |
| `ModelStructureKnowledge` | `SimulationKnowledgeArtifact` | au moins 1 composant ; exactement 1 traitement du hasard (`ParadigmType`), 1 type de temps, 1 type d'espace, 1 niveau de granularité |
| `ExecutionKnowledge` | `SimulationKnowledgeArtifact` | — |

`ModelStructureKnowledge` est le composant **MSK** du Quadruplet de recomposition, et
`ExecutionKnowledge` le composant **EK** (décision D17, faite en octobre 2026) : comment
exécuter le modèle, avec quel simulateur, combien de répétitions et quelle graine aléatoire.
L'EK n'est pas l'exécution elle-même, qui est un processus, mais la configuration que cette
exécution applique.

### Composants du modèle

| Classe | Parent | Ce qu'elle impose |
|---|---|---|
| `ModelComponent` | `SimulationKnowledgeArtifact` | — |
| `StateComponent` | `ModelComponent` | — |
| `TransitionComponent` | `ModelComponent` | exactement 1 état de départ et 1 état d'arrivée |
| `RuleComponent` | `ModelComponent` | — |
| `EnvironmentComponent` | `ModelComponent` | — |
| `ModelParameter` | `ModelComponent` | — |
| `StaticParameter`, `DynamicParameter`, `InitialCondition` | `ModelParameter` | — |

### Exécution, résultats, scénarios

| Classe | Parent | Ce qu'elle impose |
|---|---|---|
| `SimulationExecution` | `BFO:process` | exactement 1 modèle exécuté ; exactement 1 EK appliquée |
| `SimulationResult` | `SimulationKnowledgeArtifact` | — |
| `SimulationObservation` | `SimulationKnowledgeArtifact` | — |
| `SimulationScenario` | `SimulationKnowledgeArtifact` | — |
| `InterventionScenario` | `SimulationScenario` | — |

`SimulationExecution` est un **processus**, pas un artefact d'information : elle se déroule dans
le temps. `SimulationObservation` désigne les données réelles observées, nécessaires pour
valider un modèle par comparaison.

### Les sept lois de probabilité

| Classe | Paramètres imposés |
|---|---|
| `ProbabilityDistribution` | (parent) |
| `BernoulliDistribution` | `probabilityParameter` exactement 1 |
| `BetaDistribution` | `alphaParameter` et `betaParameter`, exactement 1 chacun |
| `ExponentialDistribution` | `lambdaParameter` exactement 1 |
| `GammaDistribution` | `alphaParameter` et `lambdaParameter`, exactement 1 chacun |
| `NormalDistribution` | `meanParameter` et `standardDeviationParameter`, exactement 1 chacun |
| `PoissonDistribution` | `lambdaParameter` exactement 1 |
| `UniformDistribution` | `lowerLimitParameter` et `upperLimitParameter`, exactement 1 chacun |

Les sept sont déclarées mutuellement disjointes et `hasUncertaintyDistribution` relie un
`ModelParameter` à la loi qui décrit son incertitude. Au lieu d'une valeur unique, le paramètre
porte la loi dont sa valeur est tirée à chaque répétition : c'est ce qui rend possible
l'analyse de sensibilité probabiliste.

**Pourquoi elles sont ici et pas ailleurs.** Elles sont nées de l'analyse du modèle PBD, qui est
un modèle à événements discrets — mais **« créé en travaillant sur la DES » n'est pas « est de
la DES »**. Le test est simple : *ce terme a-t-il un sens dans un modèle compartimental ?* Une
loi Beta sur β dans un SIR, oui. Elles sont donc restées quand la couche 3C a été supprimée
(décision D21) et elles sont en couche 2 parce qu'elles ne parlent ni de paradigme ni de
maladie.

### Listes de valeurs fermées

Chaque classe est **définie** par la liste exacte de ses valeurs et les 25 individus sont
déclarés différents par `owl:AllDifferent`, en deux groupes : les 16 valeurs des cinq premières
listes, puis les 9 valeurs des trois listes qui classent un modèle.

| Classe définie | Valeurs |
|---|---|
| `ParadigmType` | DETERMINISTIC, STOCHASTIC |
| `TemporalType` | CONTINUOUS, DISCRETE |
| `SpatialType` | NON_SPATIAL, NETWORK, GRID, GIS |
| `GranularityLevel` | INDIVIDUAL, GROUP, REGIONAL, MULTISCALE |
| `ValidationMethod` | ADEQUACY, CROSS_MODEL, HISTORICAL_DATA, STATISTICAL |
| `ModelNature` | MECHANISTIC, EMPIRICAL, GREY_BOX |
| `ModelScope` | GENERAL, SPECIFIC |
| `ModelPurpose` | DYNAMICS_RESEARCH, EPIDEMIC_PLANNING, METHODOLOGICAL_RESEARCH, RETROSPECTIVE_ANALYSIS |

**La déclaration de différence n'est pas une formalité.** En OWL, deux noms peuvent désigner la
même chose tant qu'on n'a pas dit le contraire : sans `AllDifferent`, un raisonneur peut
conclure que `DISCRETE` et `CONTINUOUS` sont le même individu plutôt que d'y voir une
contradiction.

**Un nom trompeur.** Malgré son nom, `ParadigmType` ne donne pas le paradigme de
modélisation (agents ou compartiments) mais le traitement du hasard : un modèle à
compartiments peut être déterministe ou stochastique. Le nom est gardé ; sa définition le dit.

**Le classement du modèle.** Les trois dernières listes, ajoutées en octobre 2026, disent si un
modèle est mécaniste, empirique ou mixte, s'il est général ou spécifique à une maladie, et à
quoi il sert. Elles servent à juger si un modèle peut être réutilisé ou recomposé pour une
autre situation : on ne recompose pas une boîte noire comme un modèle à mécanismes.

### 19 propriétés d'objet

| Propriété | Domaine → Portée | Fonctionnelle |
|---|---|---|
| `hasStructureKnowledge` | SimulationModel → ModelStructureKnowledge | oui |
| `hasComponent` | ModelStructureKnowledge → ModelComponent | non |
| `hasParameter` | SimulationModel → ModelParameter | non |
| `hasSourceState` | TransitionComponent → StateComponent | oui |
| `hasTargetState` | TransitionComponent → StateComponent | oui |
| `hasParadigm` | ModelStructureKnowledge → ParadigmType | oui |
| `hasTemporalType` | ModelStructureKnowledge → TemporalType | oui |
| `hasSpatialType` | ModelStructureKnowledge → SpatialType | oui |
| `hasGranularityLevel` | ModelStructureKnowledge → GranularityLevel | oui |
| `hasValidationMethod` | SimulationModel → ValidationMethod | non |
| `usesScenario` | SimulationModel → SimulationScenario | non |
| `executesModel` | SimulationExecution → SimulationModel | oui |
| `producesResult` | SimulationExecution → SimulationResult | non |
| `hasUncertaintyDistribution` | ModelParameter → ProbabilityDistribution | non |
| `hasExecutionKnowledge` | SimulationModel → ExecutionKnowledge | non : un modèle peut être exécuté sous plusieurs configurations |
| `appliesExecutionKnowledge` | SimulationExecution → ExecutionKnowledge | oui |
| `hasModelNature` | SimulationModel → ModelNature | oui |
| `hasModelScope` | SimulationModel → ModelScope | oui |
| `hasModelPurpose` | SimulationModel → ModelPurpose | non, délibérément : un modèle peut servir à plusieurs choses |

### 27 propriétés de données

- Sur `SimulationModel` : `modelName`, `modelDescription`, `modelVersion`, `creationDate`, `hasAuthor`
- Sur `ModelParameter` : `parameterName`, `parameterValue`, `defaultValue`, `parameterUnit`
- Sur `ModelStructureKnowledge` : `timeStepInDays`, `simulationDurationInDays`
- Sur `ExecutionKnowledge` : `simulatorName`, `simulatorVersion`, `numberOfRuns`, `randomSeed`
- Sur `SimulationExecution` : `executionStatus`
- Sur `SimulationScenario` : `scenarioDurationInDays`, `startDate`, `endDate`
- Sur `ProbabilityDistribution` : `alphaParameter`, `betaParameter`, `lambdaParameter`, `meanParameter`, `standardDeviationParameter`, `probabilityParameter`, `lowerLimitParameter`, `upperLimitParameter`

Les durées sont des **nombres en jours** et non un type de durée : `xsd:dayTimeDuration` ne
fait pas partie des types reconnus par OWL 2 et son emploi faisait sortir l'ontologie d'OWL 2
DL. L'unité est inscrite dans le nom pour éviter toute ambiguïté.

Le simulateur, sa version, le nombre de répétitions et la graine étaient sur
`SimulationExecution` ; ils sont passés sur l'EK avec la décision D17, parce qu'ils décrivent
la configuration, que plusieurs exécutions peuvent appliquer. L'état d'une exécution reste
sur l'exécution.

### Disjonctions

- Les cinq sortes de composants s'excluent : `StateComponent`, `TransitionComponent`,
  `RuleComponent`, `EnvironmentComponent`, `ModelParameter`.
- Les sept lois de probabilité s'excluent entre elles.
- `StaticParameter` ⊥ `DynamicParameter` : un paramètre ne peut pas être à la fois constant et
  variable dans le temps.

### 13 alignements vers OSDi

| OntoSim-Dis | OSDi | Type |
|---|---|---|
| `BernoulliDistribution` … `UniformDistribution` (7) | `…DistributionExpression` | exactMatch |
| `hasAuthor` | `osdi:hasAuthor` | exactMatch |
| `ProbabilityDistribution` | `osdi:ProbabilityDistributionExpression` | closeMatch |
| `hasUncertaintyDistribution` | `osdi:hasUncertaintyCharacterization` | closeMatch |
| `SimulationModel` | `osdi:Model` | closeMatch |
| `ModelParameter` | `osdi:Parameter` | closeMatch |
| `InterventionScenario` | `osdi:Intervention` | closeMatch |

Les sept lois sont alignées en `exactMatch` : c'est le groupe d'alignements le plus solide de
toute l'ontologie et il vient directement de l'analyse du modèle PBD.

**Les trois propriétés SKOS sont déclarées `owl:AnnotationProperty`** dans ce fichier. Sans
cela, un outil OWL peut les prendre pour des propriétés d'objet et les alignements deviennent
des axiomes logiques portant sur des IRI externes : l'ontologie sortirait silencieusement d'OWL
2 DL (décision D29).

---

## Validation

### 1. Audit automatique

**Résultat au 19 octobre 2026 : 0 erreur, 6 avertissements.** 893 triplets. HermiT : aucune
classe insatisfiable. Les deux erreurs du 8 octobre (les guillemets en trop dans `created` et
`versionInfo`) ont été corrigées.

Les six avertissements signalent des propriétés déclarées sans apparaître dans un axiome :
`hasExecutionKnowledge`, `hasModelNature`, `hasModelPurpose`, `hasModelScope`,
`hasUncertaintyDistribution`, `producesResult`. Elles servent à décrire un modèle précis, ce
que feront les fichiers de la couche 5, pas à raisonner ; la revue finale des propriétés
décoratives tranchera.

Pour reproduire, depuis la racine du dépôt (installation : voir `tools/README.md`) :

```
bash tools/audit_tout.sh
```

ou, pour la couche 2 seule :

```
python tools/audit_ontosim.py --focus src/ontology/layer2_modsim.ttl \
    --load src/ontology/layer1_foundational.ttl src/ontology/layer2_modsim.ttl \
    --ref tools/ref/ro.owl tools/ref/iao.owl tools/ref/bfo.owl tools/ref/ogms-edit.owl
```

### 2. Test des garde-fous

Un individu déclaré à la fois `StaticParameter` et `DynamicParameter` rend l'ontologie
**incohérente**, comme attendu. Les disjonctions fonctionnent réellement. Refait le
19 octobre 2026.

Une exécution qui applique deux EK déclarées différentes rend aussi l'ontologie
**incohérente** : une exécution applique une configuration et une seule. Vérifié le
19 octobre 2026. Sans `owl:AllDifferent` sur les deux EK, le raisonneur conclurait que c'est
la même : c'est la limite L3, à prévoir dans l'outil qui produira les descriptions.

**Deux erreurs ont été trouvées par ces contrôles pendant la construction et corrigées :**

- les restrictions de transition avaient été posées sur `StateComponent` au lieu de
  `TransitionComponent`, ce qui rendait `StateComponent` insatisfiable — donc un modèle sans
  états possibles. C'est la disjonction des cinq composants qui l'a révélé ;
- l'emploi de `xsd:dayTimeDuration` faisait déclarer trois propriétés à la fois comme
  propriétés d'objet et de données.

### 3. OOPS!

A FAIRE!!!

Soumettre le fichier sur https://oops.linkeddata.es et sauvegarder le rapport.

**Défauts probables, et réponse préparée.**

| Défaut probable | Concerne | Réponse |
|---|---|---|
| Inverse non déclaré (P13) | les 19 propriétés d'objet | Aucun usage ne demande le sens inverse pour l'instant. À revoir si une couche supérieure en a besoin. |
| Détournement d'espace de noms (P40) | `obo:` et `osdi:` | Termes importés par MIREOT et cibles d'alignement, dans leur espace d'origine. |
| Annotations manquantes (P08) | aucune | Toutes les entités ont libellé et commentaire. |
| Domaine ou portée manquant (P11) | aucune | Toutes les propriétés en ont (vérifié le 19 octobre 2026). |

---

## Versionnement

**Le fichier porte `1.0` alors que son contenu est celui de la v1.1.** Les sept lois de
probabilité, leurs huit paramètres et `hasUncertaintyDistribution` ont été ajoutés après la
fermeture, puis, en octobre 2026, l'EK et les trois listes qui classent un modèle.

La renumérotation se fait **pour l'empilement entier et en un seul geste**, juste avant
l'étiquette Git : neuf `versionIRI`, neuf `owl:versionInfo` et onze `owl:imports` passent à
`1.1` ensemble. Cette couche est importée par quatre fichiers — 3A, 3B, 4-Core et 4-Context —
qui devront suivre. Un import qui pointe vers une version inexistante, c'est Protégé qui ne
charge plus la couche.


---

## Décisions consignées

| Code | Décision |
|---|---|
| D5 | L'auteur d'un modèle est un texte, comme dans OSDi et non une classe : un chercheur est une personne, pas un artefact d'information. |
| D6 | Une seule hiérarchie de composants ; `ParameterComponent` et `ModelParameter` sont fusionnés. |
| D7 | Les types de modèles deviennent des classes dans les couches de paradigme, alignées sur OSDi et non des individus. |
| D8 | La machinerie de recomposition sort de la couche 2 et attend la décision D2. |
| D21 | Les sept lois de probabilité restent ici après la suppression de la couche 3C : elles sont indépendantes du paradigme. |
| D29 | Les trois propriétés SKOS sont déclarées comme propriétés d'annotation. |
| D17 | L'EK est en couche 2 : `ExecutionKnowledge` porte le simulateur, le nombre de répétitions et la graine, et une exécution en applique exactement une. |
| — | Trois listes fermées classent un modèle : sa nature, sa portée et son objectif. |
| — | `ParadigmType` garde son nom ; sa définition dit qu'il s'agit du traitement du hasard. |

## Décisions ouvertes qui touchent cette couche

| Code | Question | À trancher lors de |
|---|---|---|
| D2 | Relations d'entrée et de sortie de la recomposition | Conception de la recomposition |
| — | Revue finale de `hasUncertaintyDistribution` et `producesResult` | Fin de la couche 3 |
| — | Alignement fin des sept lois avec les sous-classes d'OSDi | Mapping |


## Conséquences pour les couches suivantes

| Couche | Ce qui en dépend |
|---|---|
| 3A | `AgentBasedModel ⊑ SimulationModel` ; `AgentState ⊑ StateComponent` ; `AgentTransition ⊑ TransitionComponent` ; `Behavior ⊑ RuleComponent` ; `EnvironmentModel ⊑ EnvironmentComponent` ; `AgentType` et `InteractionType ⊑ ModelComponent` |
| 3B | `CompartmentalModel ⊑ SimulationModel` ; `Compartment ⊑ StateComponent` ; `TransitionFlow ⊑ TransitionComponent` ; `RateSpecification ⊑ ModelParameter` ; `DifferentialEquation ⊑ ModelComponent` |
| 4-Core | **les trois ponts de D14** ont leur domaine ici : `representsHealthState` sur `StateComponent`, `representsStateTransition` sur `TransitionComponent`, `realisesDeterminant` sur `ModelComponent`. C'est pour cela que la couche 4 n'a pas besoin d'importer la couche 3. |
| 4-Context | `hasContextKnowledge` a pour domaine `SimulationModel` |
| 4-Checks | `StaticApproximationModel ⊑ SimulationModel` |
| 5 | Les fichiers d'application, un par cas étudié, décriront des modèles avec ce vocabulaire ; la recomposition aura son propre module. |

Une transition d'état de santé n'est **pas** un `TransitionComponent` (décision D18) : c'est une
connaissance sur la maladie, qu'une transition de modèle représente par le pont
`representsStateTransition`.

La couche des événements discrets (3C) a été retirée le 9 octobre 2026 ; son retour reste à
décider.

## Ce qui n'est pas dans cette couche

Mis de côté dans l'ancien fichier `layer2-simulation.ttl`, en attente de la décision D2 :
compositions de modèles, règles de synchronisation, contraintes de compatibilité,
correspondances de paramètres, structure abstraite, provenance, générateur automatique.
Ces éléments iront dans le futur module de recomposition.


<br>

<p align="center">
  🦋<br>
  <i>Fais avec amour et pour l'Amour.</i>
</p>