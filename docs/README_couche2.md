# OntoSim-Dis — Couche 2 : modélisation et simulation

**Fichier :** `src/ontology/layer2_modsim.ttl`
**IRI :** `https://w3id.org/ontosim-dis/layer2` — version `1.0` (`https://w3id.org/ontosim-dis/layer2/1.0`)
**Importe :** `https://w3id.org/ontosim-dis/layer1/1.0`
**Licence :** CC BY 4.0
**Statut :** version de travail 1.0, pas encore publiée. Les changements sont suivis par git ;
une fois la couche publiée, toute modification donnera une nouvelle version.

## Rôle

La couche 2 répond à la question : **comment modéliser ?** Elle contient les concepts de
simulation communs à tous les paradigmes — compartiments (couche 3B) et agents
(couche 3A) — et indépendants de tout domaine médical. Aucun terme de cette couche ne
parle de maladie.

## Contenu

105 termes : 34 classes, dont 8 définies ; 19 propriétés d'objet ; 27 propriétés de
données ; 25 individus.

### Racine et modèle

| Classe | Parent | Ce qu'elle impose |
|---|---|---|
| `SimulationKnowledgeArtifact` | `IAO:information content entity` | — |
| `SimulationModel` | `SimulationKnowledgeArtifact` | exactement 1 structure ; au moins 1 paramètre ; au moins 1 méthode de validation ; au moins 1 scénario |
| `ModelStructureKnowledge` | `SimulationKnowledgeArtifact` | au moins 1 composant ; exactement 1 traitement du hasard, 1 type de temps, 1 type d'espace, 1 niveau de granularité |
| `ExecutionKnowledge` | `SimulationKnowledgeArtifact` | — |

`ModelStructureKnowledge` est le composant **MSK** du Quadruplet de recomposition, et
`ExecutionKnowledge` le composant **EK** : comment exécuter le modèle, avec quel
simulateur, combien de répétitions et quelle graine aléatoire. L'EK n'est pas l'exécution
elle-même, qui est un processus, mais la configuration que cette exécution applique.

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

`SimulationExecution` est un **processus**, pas un artefact d'information : elle se déroule
dans le temps. `SimulationObservation` désigne les données réelles observées, nécessaires
pour valider un modèle par comparaison.

### Lois de probabilité

| Classe | Parent | Ce qu'elle impose |
|---|---|---|
| `ProbabilityDistribution` | `SimulationKnowledgeArtifact` | — |
| `BernoulliDistribution` | `ProbabilityDistribution` | exactement 1 `probabilityParameter` |
| `BetaDistribution` | `ProbabilityDistribution` | exactement 1 `alphaParameter` et 1 `betaParameter` |
| `ExponentialDistribution` | `ProbabilityDistribution` | exactement 1 `lambdaParameter` |
| `GammaDistribution` | `ProbabilityDistribution` | exactement 1 `alphaParameter` et 1 `lambdaParameter` |
| `NormalDistribution` | `ProbabilityDistribution` | exactement 1 `meanParameter` et 1 `standardDeviationParameter` |
| `PoissonDistribution` | `ProbabilityDistribution` | exactement 1 `lambdaParameter` |
| `UniformDistribution` | `ProbabilityDistribution` | exactement 1 `lowerLimitParameter` et 1 `upperLimitParameter` |

Ce sont les sept lois d'OSDi. Un paramètre porte la sienne par `hasUncertaintyDistribution` :
au lieu d'une valeur unique, il porte la loi dont sa valeur est tirée à chaque répétition.
C'est ce qui rend possible l'analyse de sensibilité probabiliste.

### Listes de valeurs fermées

Chaque classe est définie par la liste exacte de ses valeurs (`owl:oneOf`), et les valeurs
sont déclarées toutes différentes, en deux groupes : les 16 valeurs des cinq premières
listes, puis les 9 valeurs des trois listes qui classent un modèle.

| Classe | Valeurs |
|---|---|
| `ParadigmType` | DETERMINISTIC, STOCHASTIC |
| `TemporalType` | CONTINUOUS, DISCRETE |
| `SpatialType` | NON_SPATIAL, NETWORK, GRID, GIS |
| `GranularityLevel` | INDIVIDUAL, GROUP, REGIONAL, MULTISCALE |
| `ValidationMethod` | ADEQUACY, CROSS_MODEL, HISTORICAL_DATA, STATISTICAL |
| `ModelNature` | MECHANISTIC, EMPIRICAL, GREY_BOX |
| `ModelScope` | GENERAL, SPECIFIC |
| `ModelPurpose` | DYNAMICS_RESEARCH, EPIDEMIC_PLANNING, METHODOLOGICAL_RESEARCH, RETROSPECTIVE_ANALYSIS |

**Un nom trompeur.** Malgré son nom, `ParadigmType` ne donne pas le paradigme de
modélisation (agents ou compartiments) mais le traitement du hasard : un modèle à
compartiments peut être déterministe ou stochastique. Le nom est gardé ; sa définition le dit.

**Le classement du modèle.** Les trois dernières listes disent si un modèle est mécaniste,
empirique ou mixte, s'il est général ou spécifique à une maladie, et à quoi il sert. Elles
servent à juger si un modèle peut être réutilisé ou recomposé pour une autre situation : on
ne recompose pas une boîte noire comme un modèle à mécanismes.

### Propriétés d'objet (19)

| Propriété | Domaine → Portée | Fonctionnelle |
|---|---|---|
| `hasStructureKnowledge` | SimulationModel → ModelStructureKnowledge | oui |
| `hasExecutionKnowledge` | SimulationModel → ExecutionKnowledge | non : un modèle peut être exécuté sous plusieurs configurations |
| `hasComponent` | ModelStructureKnowledge → ModelComponent | non |
| `hasParameter` | SimulationModel → ModelParameter | non |
| `hasUncertaintyDistribution` | ModelParameter → ProbabilityDistribution | non |
| `hasSourceState` | TransitionComponent → StateComponent | oui |
| `hasTargetState` | TransitionComponent → StateComponent | oui |
| `hasParadigm` | ModelStructureKnowledge → ParadigmType | oui |
| `hasTemporalType` | ModelStructureKnowledge → TemporalType | oui |
| `hasSpatialType` | ModelStructureKnowledge → SpatialType | oui |
| `hasGranularityLevel` | ModelStructureKnowledge → GranularityLevel | oui |
| `hasModelNature` | SimulationModel → ModelNature | oui |
| `hasModelScope` | SimulationModel → ModelScope | oui |
| `hasModelPurpose` | SimulationModel → ModelPurpose | non, délibérément : un modèle peut servir à plusieurs choses |
| `hasValidationMethod` | SimulationModel → ValidationMethod | non |
| `usesScenario` | SimulationModel → SimulationScenario | non |
| `executesModel` | SimulationExecution → SimulationModel | oui |
| `appliesExecutionKnowledge` | SimulationExecution → ExecutionKnowledge | oui |
| `producesResult` | SimulationExecution → SimulationResult | non |

### Propriétés de données (27)

- Sur `SimulationModel` : `modelName`, `modelDescription`, `modelVersion`, `creationDate`, `hasAuthor`
- Sur `ModelParameter` : `parameterName`, `parameterValue`, `defaultValue`, `parameterUnit`
- Sur `ModelStructureKnowledge` : `timeStepInDays`, `simulationDurationInDays`
- Sur `ExecutionKnowledge` : `simulatorName`, `simulatorVersion`, `numberOfRuns`, `randomSeed`
- Sur `SimulationExecution` : `executionStatus`
- Sur `SimulationScenario` : `scenarioDurationInDays`, `startDate`, `endDate`
- Sur `ProbabilityDistribution` : `alphaParameter`, `betaParameter`, `lambdaParameter`,
  `meanParameter`, `standardDeviationParameter`, `lowerLimitParameter`,
  `upperLimitParameter`, `probabilityParameter`

Le simulateur, le nombre de répétitions et la graine sont portés par l'EK, et non par
l'exécution : ils décrivent la configuration, que plusieurs exécutions peuvent appliquer.
L'état d'une exécution (en cours, terminée...) reste sur l'exécution.

Les durées sont des nombres en jours, et non un type de durée : `xsd:dayTimeDuration`
ne fait pas partie des types reconnus par OWL 2, et son emploi faisait sortir l'ontologie
d'OWL 2 DL. L'unité est inscrite dans le nom pour éviter toute ambiguïté.

### Disjonctions

- Les cinq sortes de composants s'excluent : `StateComponent`, `TransitionComponent`,
  `RuleComponent`, `EnvironmentComponent`, `ModelParameter`.
- `StaticParameter` ⊥ `DynamicParameter` : un paramètre ne peut pas être à la fois
  constant et variable dans le temps.
- Les sept lois de probabilité s'excluent deux à deux.

### Alignements vers OSDi (13)

| OntoSim-Dis | OSDi | Type |
|---|---|---|
| `SimulationModel` | `osdi:Model` | closeMatch |
| `ModelParameter` | `osdi:Parameter` | closeMatch |
| `InterventionScenario` | `osdi:Intervention` | closeMatch |
| `ProbabilityDistribution` | `osdi:ProbabilityDistributionExpression` | closeMatch |
| `hasUncertaintyDistribution` | `osdi:hasUncertaintyCharacterization` | closeMatch |
| les sept lois (`BernoulliDistribution`...) | `osdi:BernoulliDistributionExpression`... | exactMatch |
| `hasAuthor` | `osdi:hasAuthor` | exactMatch |

---

## Validation

### 1. Audit automatique

**Résultat au 19 octobre 2026 :** 0 erreur ; HermiT trouve la couche cohérente, sans
classe insatisfiable (893 triplets). Six avertissements « propriété jamais utilisée » :
`hasExecutionKnowledge`, `hasModelNature`, `hasModelPurpose`, `hasModelScope`,
`hasUncertaintyDistribution`, `producesResult`. Ils sont attendus : ces propriétés servent
quand on décrit un modèle précis, ce que feront les fichiers de la couche 5.

**Pour reproduire,** depuis la racine du dépôt (installation : voir `tools/README.md`) :

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

Deux tests, refaits le 19 octobre 2026 avec HermiT :

- un individu déclaré à la fois `StaticParameter` et `DynamicParameter` rend l'ontologie
  **incohérente**, comme attendu : les disjonctions fonctionnent réellement ;
- une exécution qui applique deux EK déclarées différentes rend l'ontologie
  **incohérente**, comme attendu : une exécution applique une configuration et une seule.

Le second test ne fonctionne que si les deux EK sont déclarées différentes
(`owl:AllDifferent`). Sans cela, le raisonneur conclut que c'est la même EK : c'est la
limite L3, à prévoir dans l'outil qui produira les descriptions.

Deux erreurs ont été trouvées par ces contrôles pendant la construction, et corrigées :

- les restrictions de transition avaient été posées sur `StateComponent` au lieu de
  `TransitionComponent`, ce qui rendait `StateComponent` insatisfiable — donc un modèle
  sans états possibles. C'est la disjonction des composants qui l'a révélé ;
- l'emploi de `xsd:dayTimeDuration` faisait déclarer trois propriétés à la fois comme
  propriétés d'objet et de données.

### 3. OOPS! (à faire)

Soumettre le fichier sur https://oops.linkeddata.es et sauvegarder le rapport.

| Défaut probable | Concerne | Réponse |
|---|---|---|
| Inverse non déclaré (P13) | les 19 propriétés d'objet | **Justifier** : aucun usage ne demande le sens inverse pour l'instant. À revoir si une couche supérieure en a besoin. |
| Détournement d'espace de noms (P40) | `obo:` et `osdi:` | **Justifier** : termes importés par MIREOT et cibles d'alignement, dans leur espace d'origine. |
| Annotations manquantes (P08) | aucune | Toutes les entités ont libellé et commentaire. |
| Domaine ou portée manquant (P11) | aucune | Toutes les propriétés en ont. |

---

## Versionnement

La couche est suivie dans le dépôt, avec les autres modules. Quand elle sera publiée,
marquer sa version d'une étiquette :

```
git tag -a layer2-v1.0 -m "Couche 2, version 1.0"
git push --tags
```

---

## Décisions consignées

| Code | Décision |
|---|---|
| D5 | L'auteur d'un modèle est un texte, comme dans OSDi, et non une classe : un chercheur est une personne, pas un artefact d'information. |
| D6 | Une seule hiérarchie de composants ; `ParameterComponent` et `ModelParameter` sont fusionnés. |
| D7 | Les types de modèles deviennent des classes dans les couches de paradigme, alignées sur OSDi, et non des individus. |
| D8 | La machinerie de recomposition sort de la couche 2 et attend la décision D2. |
| D17 | L'EK, connaissance d'exécution, est en couche 2 : `ExecutionKnowledge` porte le simulateur, le nombre de répétitions et la graine, et une exécution en applique exactement une. |
| — | Trois listes fermées classent un modèle : sa nature, sa portée et son objectif. |
| — | `ParadigmType` garde son nom, malgré son sens (le traitement du hasard) : sa définition le dit. |

## Décisions ouvertes

| Code | Question | État |
|---|---|---|
| D1 | Où placer OGMS ? | **Tranchée** : module d'import à part, `layer4-ogms.ttl` |
| D2 | Relations d'entrée et de sortie de la recomposition | **En suspens**, jusqu'à la conception de la recomposition |
| D4 | Un `Agent` participe-t-il directement à la simulation ? | **Sans objet** : la couche 3A ne décrit que des catégories d'agents |

## Ce que les autres couches reprennent de la couche 2

| Couche | Ce qu'elle spécialise ou relie |
|---|---|
| 3A | `AgentBasedModel ⊑ SimulationModel` ; `AgentState ⊑ StateComponent` ; `AgentTransition ⊑ TransitionComponent` ; `Behavior ⊑ RuleComponent` ; `EnvironmentModel ⊑ EnvironmentComponent` ; `AgentType` et `InteractionType ⊑ ModelComponent` |
| 3B | `CompartmentalModel ⊑ SimulationModel` ; `Compartment ⊑ StateComponent` ; `TransitionFlow ⊑ TransitionComponent` ; `RateSpecification ⊑ ModelParameter` ; `DifferentialEquation ⊑ ModelComponent` |
| 4-Core | Les trois ponts partent de classes de la couche 2 (décision D14) : `representsHealthState` d'un `StateComponent`, `representsStateTransition` d'un `TransitionComponent`, `realisesDeterminant` d'un `ModelComponent`. Une transition d'état de santé n'est **pas** un `TransitionComponent` (décision D18) : c'est une connaissance, qu'une transition de modèle représente. |
| 4-Context | `hasContextKnowledge` relie un `SimulationModel` à son contexte. |
| 4-Checks | `StaticApproximationModel ⊑ SimulationModel`. |

La couche des événements discrets (3C) a été retirée le 9 octobre 2026 ; son retour reste à
décider.

## Ce qui n'est pas dans cette couche

Mis de côté dans l'ancien fichier `layer2-simulation.ttl`, en attente de la décision D2 :
compositions de modèles, règles de synchronisation, contraintes de compatibilité,
correspondances de paramètres, structure abstraite, provenance, générateur automatique.
Ces éléments iront dans un futur module de recomposition, quand celle-ci sera conçue.
