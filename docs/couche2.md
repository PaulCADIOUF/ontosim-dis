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

**30 classes, 14 propriétés d'objet, 27 propriétés de données, 16 individus, 5 classes définies,
23 restrictions, 13 alignements.** 743 triplets.

### Racine et modèle

| Classe | Parent | Ce qu'elle impose |
|---|---|---|
| `SimulationKnowledgeArtifact` | `IAO:information content entity` | — |
| `SimulationModel` | `SimulationKnowledgeArtifact` | exactement 1 structure ; au moins 1 paramètre ; au moins 1 méthode de validation ; au moins 1 scénario |
| `ModelStructureKnowledge` | `SimulationKnowledgeArtifact` | au moins 1 composant ; exactement 1 paradigme, 1 type de temps, 1 type d'espace, 1 niveau de granularité |

`ModelStructureKnowledge` est le composant **MSK** du Quadruplet de recomposition.

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
| `SimulationExecution` | `BFO:process` | exactement 1 modèle exécuté |
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
| `GammaDistribution` | `alphaParameter` et `lambdaParameter` |
| `NormalDistribution` | `meanParameter` et `standardDeviationParameter` |
| `PoissonDistribution` | `lambdaParameter` exactement 1 |
| `UniformDistribution` | `lowerLimitParameter` et `upperLimitParameter` |

Les sept sont déclarées mutuellement disjointes et `hasUncertaintyDistribution` relie un
`ModelParameter` à la loi qui décrit son incertitude.

**Pourquoi elles sont ici et pas ailleurs.** Elles sont nées de l'analyse du modèle PBD, qui est
un modèle à événements discrets — mais **« créé en travaillant sur la DES » n'est pas « est de
la DES »**. Le test est simple : *ce terme a-t-il un sens dans un modèle compartimental ?* Une
loi Beta sur β dans un SIR, oui. Elles sont donc restées quand la couche 3C a été supprimée
(décision D21) et elles sont en couche 2 parce qu'elles ne parlent ni de paradigme ni de
maladie.

### Listes de valeurs fermées

Chaque classe est **définie** par la liste exacte de ses valeurs et les 16 individus sont
déclarés tous différents par `owl:AllDifferent`.

| Classe définie | Valeurs |
|---|---|
| `ParadigmType` | DETERMINISTIC, STOCHASTIC |
| `TemporalType` | CONTINUOUS, DISCRETE |
| `SpatialType` | NON_SPATIAL, NETWORK, GRID, GIS |
| `GranularityLevel` | INDIVIDUAL, GROUP, REGIONAL, MULTISCALE |
| `ValidationMethod` | ADEQUACY, CROSS_MODEL, HISTORICAL_DATA, STATISTICAL |

**La déclaration de différence n'est pas une formalité.** En OWL, deux noms peuvent désigner la
même chose tant qu'on n'a pas dit le contraire : sans `AllDifferent`, un raisonneur peut
conclure que `DISCRETE` et `CONTINUOUS` sont le même individu plutôt que d'y voir une
contradiction.

### 14 propriétés d'objet

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

### 27 propriétés de données

- Sur `SimulationModel` : `modelName`, `modelDescription`, `modelVersion`, `creationDate`, `hasAuthor`
- Sur `ModelParameter` : `parameterName`, `parameterValue`, `defaultValue`, `parameterUnit`
- Sur `ModelStructureKnowledge` : `timeStepInDays`, `simulationDurationInDays`
- Sur `SimulationExecution` : `simulatorName`, `simulatorVersion`, `numberOfRuns`, `randomSeed`, `executionStatus`
- Sur `SimulationScenario` : `scenarioDurationInDays`, `startDate`, `endDate`
- Sur `ProbabilityDistribution` : `alphaParameter`, `betaParameter`, `lambdaParameter`, `meanParameter`, `standardDeviationParameter`, `probabilityParameter`, `lowerLimitParameter`, `upperLimitParameter`

Les durées sont des **nombres en jours** et non un type de durée. L'unité est inscrite dans le nom pour éviter toute ambiguïté.

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

**Résultat au 2026-10-08 : 2 erreurs, 2 avertissements.**

Les deux erreurs sont de tenue de dossier, pas de logique :

```
X [1b] valeur entre guillemets dans la valeur : layer2 created = "2026"
X [1b] valeur entre guillemets dans la valeur : layer2 versionInfo = "1.0"
```

La valeur contient ses propres guillemets, parce que Protégé ajoute les siens. À corriger —
Partie IX.1 du registre.

Les deux avertissements signalent `hasUncertaintyDistribution` et `producesResult` comme
déclarées sans apparaître dans un axiome. Les deux servent à décrire, pas à raisonner ; la
revue finale des propriétés décoratives tranchera.

HermiT : aucune classe insatisfiable.

```
python3 tools/audit_ontosim.py --focus layer2_modsim.ttl \
    --load layer1_foundational.ttl layer2_modsim.ttl \
    --ref tools/refs/*.owl
```

### 2. Test des garde-fous

Un individu déclaré à la fois `StaticParameter` et `DynamicParameter` rend l'ontologie
**incohérente**, comme attendu. Les disjonctions fonctionnent réellement.

**Deux erreurs ont été trouvées par ces contrôles pendant la construction et corrigées :**

- les restrictions de transition avaient été posées sur `StateComponent` au lieu de
  `TransitionComponent`, ce qui rendait `StateComponent` insatisfiable — donc un modèle sans
  états possibles. C'est la disjonction des cinq composants qui l'a révélé ;
- l'emploi de `xsd:dayTimeDuration` faisait déclarer trois propriétés à la fois comme
  propriétés d'objet et de données.

### 3. OOPS!

A FAIRE!!!
---

## Versionnement

**Le fichier porte `1.0` alors que son contenu est celui de la v1.1.** Les sept lois de
probabilité, leurs huit paramètres et `hasUncertaintyDistribution` ont été ajoutés après la
fermeture.

La renumérotation se fait **pour l'empilement entier et en un seul geste**, juste avant
l'étiquette Git : huit `versionIRI`, huit `owl:versionInfo` et neuf `owl:imports` passent à
`1.1` ensemble. Cette couche est importée par quatre fichiers — 3A, 3B, 4-Core et 4-Context —
qui devront suivre. Un import qui pointe vers une version inexistante, c'est Protégé qui ne
charge plus la couche.

```
git add src/ontology/layer2_modsim.ttl docs/couche2.md
git commit -m "layer2 : corrige les guillemets dans created et versionInfo"
```

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

## Décisions ouvertes qui touchent cette couche

| Code | Question | À trancher lors de |
|---|---|---|
| D2 | Relations d'entrée et de sortie de la recomposition | Conception de la recomposition |
| D17 | **`ExecutionKnowledge` n'existe pas** : à créer ici, sous `SimulationKnowledgeArtifact` | Avant la description d'une maladie réelle |
| — | Revue finale de `hasUncertaintyDistribution` et `producesResult` | Fin de la couche 3 |
| — | Alignement fin des sept lois avec les sous-classes d'OSDi | Mapping |


## Conséquences pour les couches suivantes

| Couche | Ce qui en dépend |
|---|---|
| 3A | `AgentBasedModel ⊑ SimulationModel` ; `AgentState ⊑ StateComponent` ; `AgentTransition ⊑ TransitionComponent` |
| 3B | `CompartmentalModel ⊑ SimulationModel` ; `Compartment ⊑ StateComponent` ; `TransitionFlow ⊑ TransitionComponent` ; `RateSpecification ⊑ ModelParameter` |
| 4-Core | **les trois ponts de D14** ont leur domaine ici : `representsHealthState` sur `StateComponent`, `representsStateTransition` sur `TransitionComponent`, `realisesDeterminant` sur `ModelComponent`. C'est pour cela que la couche 4 n'a pas besoin d'importer la couche 3. |
| 4-Context | `hasContextKnowledge` a pour domaine `SimulationModel` |
| 5 | En attente, avec la recomposition |


<br>

<p align="center">
  🦋<br>
  <i>Fais avec amour et pour l'Amour.</i>
</p>