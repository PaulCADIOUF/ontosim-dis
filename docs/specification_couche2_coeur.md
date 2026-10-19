# Spécification — OntoSim-Dis, Couche 2 (cœur) — version 1.0

> **Document historique, mis à jour le 19 octobre 2026.** Ce plan de construction de la
> version 1.0 (septembre 2026) a été exécuté. Le contenu actuel de la couche est décrit dans
> sa fiche, `couche2.md`. Depuis ce plan, la couche a reçu :
> - les sept lois de probabilité d'OSDi, et `hasUncertaintyDistribution` pour les rattacher
>   aux paramètres ;
> - l'EK, `ExecutionKnowledge` (décision D17), qui porte désormais le simulateur, le nombre de
>   répétitions et la graine ;
> - les trois listes qui classent un modèle : `ModelNature`, `ModelScope`, `ModelPurpose`.
>
> Les corrections faites pendant ou après la construction sont signalées à leur place, par
> la mention **Corrigé**.

Plan de construction dans Protégé. Construire un **nouveau fichier** à partir de cette
spécification. L'ancien `layer2-simulation.ttl` reste intact et sert d'archive.

## Adresses

| Élément | Valeur |
|---|---|
| IRI de l'ontologie | `https://w3id.org/ontosim-dis/layer2` |
| IRI de version | `https://w3id.org/ontosim-dis/layer2/1.0` |
| Espace de noms des termes | `https://w3id.org/ontosim-dis#` (commun à toutes les couches) |
| Import | `https://w3id.org/ontosim-dis/layer1/1.0` |

**Pourquoi un espace de noms commun à toutes les couches.** Une classe garde le même nom
si on la déplace d'un fichier à l'autre, ce qui est exactement ce qu'on fait aujourd'hui
avec la recomposition.

**Pourquoi w3id.** L'adresse reste valable même si l'hébergement change. C'est ce
qu'utilise OSDi (`https://w3id.org/ontologies-ULL/OSDi#`). L'enregistrement se fait plus
tard, par une demande sur le dépôt GitHub de w3id ; l'adresse peut être utilisée avant.

**Conséquence sur la couche 1.** Changer seulement l'IRI de l'ontologie
(`https://w3id.org/ontosim-dis/layer1`) et l'IRI de version. Aucun terme ne change, ils sont
tous dans l'espace `obo:`. **Corrigé :** le plan prévoyait de passer la couche 1 en version
1.1 ; elle a gardé le numéro 1.0 (`.../layer1/1.0`), aucune version n'ayant encore été
publiée.

---

## Rôle de la couche

La couche 2 répond à la question : **comment modéliser ?** Elle contient les concepts de
simulation communs à tous les paradigmes (compartimental, agents, événements discrets),
et rien de propre à un domaine médical.

---

## 1. Classes du cœur (22)

Préfixe `ds:` = `https://w3id.org/ontosim-dis#` (les fichiers utilisent `dsim:`, qui
désigne le même espace).

### Racine

| Classe | Parent | Définition à écrire |
|---|---|---|
| `ds:SimulationKnowledgeArtifact` | `obo:IAO_0000030` | Artefact d'information portant une connaissance utilisée pour construire, décrire ou exécuter un modèle de simulation. |

### Modèle et structure

| Classe | Parent | Restrictions |
|---|---|---|
| `ds:SimulationModel` | `ds:SimulationKnowledgeArtifact` | `hasStructureKnowledge exactly 1 ModelStructureKnowledge` ; `hasParameter min 1 ModelParameter` ; `hasValidationMethod min 1 ValidationMethod` ; `usesScenario min 1 SimulationScenario` |
| `ds:ModelStructureKnowledge` | `ds:SimulationKnowledgeArtifact` | `hasComponent min 1 ModelComponent` ; `hasParadigm exactly 1 ParadigmType` ; `hasTemporalType exactly 1 TemporalType` ; `hasSpatialType exactly 1 SpatialType` ; `hasGranularityLevel exactly 1 GranularityLevel` |

`ModelStructureKnowledge` est le composant MSK du Quadruplet.

### Composants du modèle

| Classe | Parent | Restrictions |
|---|---|---|
| `ds:ModelComponent` | `ds:SimulationKnowledgeArtifact` | — |
| `ds:StateComponent` | `ds:ModelComponent` | — |
| `ds:TransitionComponent` | `ds:ModelComponent` | `hasSourceState exactly 1 StateComponent` ; `hasTargetState exactly 1 StateComponent` |
| `ds:RuleComponent` | `ds:ModelComponent` | — |
| `ds:EnvironmentComponent` | `ds:ModelComponent` | — |
| `ds:ModelParameter` | `ds:ModelComponent` | — |
| `ds:StaticParameter` | `ds:ModelParameter` | — |
| `ds:DynamicParameter` | `ds:ModelParameter` | — |
| `ds:InitialCondition` | `ds:ModelParameter` | — |

**La nouveauté importante : `TransitionComponent`.** Une transition relie un état de départ
à un état d'arrivée, quel que soit le paradigme. Cette structure, qui était dans la couche 4,
descend ici. Les couches 3B (`TransitionFlow`) et 3A (`AgentTransition`) la spécialisent au
lieu de la redéfinir.

**Corrigé :** le plan prévoyait aussi `HealthStateTransition ⊑ TransitionComponent` en
couche 4. La décision D18 l'a écarté : une transition d'état de santé est une connaissance
sur la maladie, pas une pièce de modèle ; une transition de modèle la **représente**, par le
pont `representsStateTransition` (décision D14).

**`StaticParameter` et `DynamicParameter` : les déclarer disjoints.** Un paramètre ne peut
pas être à la fois constant et variable dans le temps.

### Exécution et résultats

| Classe | Parent | Restrictions |
|---|---|---|
| `ds:SimulationExecution` | `obo:BFO_0000015` (process) | `executesModel exactly 1 SimulationModel` |
| `ds:SimulationResult` | `ds:SimulationKnowledgeArtifact` | — |
| `ds:SimulationObservation` | `ds:SimulationKnowledgeArtifact` | — |

`SimulationObservation` : données réelles observées, servant à valider un modèle par
comparaison avec ses résultats. Gardée parce que la validation de l'article
(reproduire un modèle publié) en a besoin.

### Scénarios

| Classe | Parent |
|---|---|
| `ds:SimulationScenario` | `ds:SimulationKnowledgeArtifact` |
| `ds:InterventionScenario` | `ds:SimulationScenario` |

`InterventionScenario` est gardé parce que les interventions (vaccination, traitement)
existent dans OSDi et seront utiles au mapping.

### Listes de valeurs fermées

Chaque classe est **définie par la liste exacte de ses valeurs** (`owl:oneOf`), et les
valeurs sont déclarées **toutes différentes** (`owl:AllDifferent`). Ainsi le raisonneur sait
qu'il n'en existe pas d'autres.

| Classe | Valeurs |
|---|---|
| `ds:ParadigmType` | `DETERMINISTIC`, `STOCHASTIC` |
| `ds:TemporalType` | `CONTINUOUS`, `DISCRETE` |
| `ds:SpatialType` | `NON_SPATIAL`, `NETWORK`, `GRID`, `GIS` |
| `ds:GranularityLevel` | `INDIVIDUAL`, `GROUP`, `REGIONAL`, `MULTISCALE` |
| `ds:ValidationMethod` | `ADEQUACY`, `CROSS_MODEL`, `HISTORICAL_DATA`, `STATISTICAL` |

Toutes sont sous `ds:SimulationKnowledgeArtifact`. Chaque valeur reçoit un libellé et un
commentaire (l'ancienne couche en avait très peu).

---

## 2. Propriétés d'objet (13)

| Propriété | Domaine | Portée | Remarque |
|---|---|---|---|
| `ds:hasStructureKnowledge` | SimulationModel | ModelStructureKnowledge | fonctionnelle |
| `ds:hasComponent` | ModelStructureKnowledge | ModelComponent | |
| `ds:hasParameter` | SimulationModel | ModelParameter | |
| `ds:hasSourceState` | TransitionComponent | StateComponent | fonctionnelle — **nouvelle** |
| `ds:hasTargetState` | TransitionComponent | StateComponent | fonctionnelle — **nouvelle** |
| `ds:hasParadigm` | ModelStructureKnowledge | ParadigmType | fonctionnelle |
| `ds:hasTemporalType` | ModelStructureKnowledge | TemporalType | fonctionnelle |
| `ds:hasSpatialType` | ModelStructureKnowledge | SpatialType | fonctionnelle |
| `ds:hasGranularityLevel` | ModelStructureKnowledge | GranularityLevel | fonctionnelle |
| `ds:hasValidationMethod` | SimulationModel | ValidationMethod | |
| `ds:usesScenario` | SimulationModel | SimulationScenario | |
| `ds:executesModel` | SimulationExecution | SimulationModel | fonctionnelle — **portée changée** |
| `ds:producesResult` | SimulationExecution | SimulationResult | |

**`executesModel` change de portée.** Avant, l'exécution portait sur une
`AbstractModelStructure`, représentation intermédiaire de la recomposition. Dans le chemin
de l'article (OSDi → JaDES → exécution), c'est le modèle lui-même qui s'exécute.

## 3. Propriétés de données (19)

| Propriété | Domaine | Type |
|---|---|---|
| `ds:modelName` | SimulationModel | string |
| `ds:modelDescription` | SimulationModel | string |
| `ds:modelVersion` | SimulationModel | string |
| `ds:creationDate` | SimulationModel | dateTime |
| `ds:hasAuthor` | SimulationModel | string — **nouvelle, alignée sur OSDi** |
| `ds:parameterName` | ModelParameter | string |
| `ds:parameterValue` | ModelParameter | double |
| `ds:defaultValue` | ModelParameter | double |
| `ds:parameterUnit` | ModelParameter | string |
| `ds:timeStepInDays` | ModelStructureKnowledge | double |
| `ds:simulationDurationInDays` | ModelStructureKnowledge | double |
| `ds:simulatorName` | ExecutionKnowledge | string |
| `ds:simulatorVersion` | ExecutionKnowledge | string |
| `ds:numberOfRuns` | ExecutionKnowledge | integer |
| `ds:randomSeed` | ExecutionKnowledge | integer |
| `ds:executionStatus` | SimulationExecution | string |
| `ds:scenarioDurationInDays`, `ds:startDate`, `ds:endDate` | SimulationScenario | double, dateTime, dateTime |

`startDate` et `endDate` étaient sur `TemporalScenario`, supprimé : ils remontent sur
`SimulationScenario`.

**Corrigé pendant la construction :** le plan donnait aux trois durées le type
`xsd:dayTimeDuration`, qui ne fait pas partie des types reconnus par OWL 2 et faisait sortir
l'ontologie d'OWL 2 DL. Ce sont des nombres en jours, et l'unité est inscrite dans leur nom :
`timeStepInDays`, `simulationDurationInDays`, `scenarioDurationInDays`.

**Corrigé avec la décision D17 :** le simulateur, sa version, le nombre de répétitions et la
graine étaient sur `SimulationExecution`. Ils sont passés sur `ExecutionKnowledge`, la
configuration que l'exécution applique ; seul l'état de l'exécution reste sur elle.

Ajouter `skos:exactMatch osdi:hasAuthor` sur `ds:hasAuthor`.

---

## 4. Ce qui part dans le futur module de recomposition

**Rien à reconstruire maintenant.** Ces éléments restent dans l'ancien fichier, qui sert
d'archive. Ils seront repris quand la décision D2 sera prise, dans un fichier
`layer2-recomposition` que la couche 5 importera.

- **Compositions** : `ModelComposition` et ses 4 sous-classes ; `combinesModel`, `hasComposition`
- **Synchronisation** : `SynchronizationRule` et ses 3 sous-classes ; `hasSynchronizationRule`, `syncInterface`
- **Compatibilité** : `CompatibilityConstraint` et ses 5 sous-classes ; `hasCompatibilityConstraint`
- **Correspondances** : `ParameterMapping` et ses 3 sous-classes ; `mapsSourceParameter`, `mapsTargetParameter`, `mappingFormula`
- **Entrées/sorties** : `InputComponent`, `OutputComponent` ; `hasInputComponent`, `hasOutputComponent`, `feedsInto`
- **Couplage** : `CouplingType` et ses 3 valeurs ; `hasCouplingType`, `coupledWith`
- **Structure abstraite** : `AbstractModelStructure` et ses 6 sous-classes ; `representedAs`
- **Provenance** : `ModelProvenance`, `ProvenanceStore`, `hasProvenance`, `derivedFrom`
- **Générateur** : `AutomaticGenerator`, `generatedBy` — note pour la reprise : le placer
  sous `IAO:software` (IAO_0000010), qui est un artefact d'information. Cela règle la
  question D4 pour le logiciel : le programme est une information, son exécution est un
  processus.

**Pourquoi.** Aucune couche ne les utilise. L'article de validation représente et simule
des modèles publiés ; il ne passe pas par la recomposition.

---

## 5. Ce qui est supprimé, et pourquoi

| Élément | Raison |
|---|---|
| `Author`, `Researcher`, `Institution`, `hasAuthor` (objet), `hasInstitution`, `fullName`, `email`, `orcid` | Un chercheur n'est pas un artefact d'information (erreur démontrée par HermiT). L'auteur devient un texte, comme dans OSDi. |
| Classes `prov:` et `foaf:` | Non alignées sur BFO, et plus nécessaires. |
| `ModelType` et ses valeurs `AGENT_BASED`, `COMPARTMENTAL`, `DISCRETE_EVENT`, `HYBRID`, `SYSTEM_DYNAMICS` ; `hasModelType` | Double emploi avec les classes de modèles des couches 3 (D7). Aucune couche ne les utilisait. |
| `HYBRID_PARADIGM` | Un modèle hybride est une composition : il relève de la recomposition. |
| `ParameterComponent` | Fusionné dans `ModelParameter` (D6). |
| `MandatoryParameter`, `OptionalParameter` | Obligatoire ou facultatif dépend du modèle, pas du paramètre : à exprimer par une restriction sur le modèle. |
| `ConstraintParameter` | Définition trop vague, jamais utilisé. |
| `DiseaseScenario`, `ExperimentalScenario`, `PopulationScenario`, `SpatialScenario`, `TemporalScenario` | Vides et jamais utilisés. |

---

## 6. Conséquences sur les autres couches

| Couche | Changement prévu | Ce qu'il est devenu (19 octobre 2026) |
|---|---|---|
| 3B | `EpidemiologicalParameter ⊑ ModelParameter` (au lieu de `ParameterComponent`) | Fait autrement : la couche 3B n'a plus de paramètre épidémiologique ; c'est `RateSpecification ⊑ ModelParameter`. |
| 3A | Ajouter une classe `AgentBasedModel ⊑ SimulationModel` (aujourd'hui, seul le type `AGENT_BASED` existait) | Fait. |
| 3 | **Question ouverte majeure** : aucune couche ne couvre les modèles à événements discrets, alors que c'est le paradigme de JaDES et d'OSDi (`DiscreteEventSimulationModel`). | Une couche 3C a été construite, puis retirée le 9 octobre 2026 ; son retour reste à décider. |
| 4-core | `HealthStateTransition ⊑ TransitionComponent`, et ses propriétés `hasSourceState`/`hasTargetState` deviennent des spécialisations de celles de la couche 2. | **Écarté** (décision D18) : la transition d'état de santé reste une connaissance, reliée aux modèles par les ponts (D14). `hasSourceHealthState` et `hasTargetHealthState` sont des propriétés distinctes. |
| 5 | En suspens avec la recomposition. | La couche 5 contiendra les applications, un fichier par cas étudié ; la recomposition aura son propre module. |

---

## 7. Contrôle attendu à la fin

- Audit : 0 erreur, 0 avertissement ; HermiT cohérent.
- Test à refaire : déclarer temporairement un individu à la fois `StaticParameter` et
  `DynamicParameter` ; HermiT doit signaler une incohérence. Puis retirer le test.
- OOPS!, cahier de conception, commit, étiquettes `layer1-v1.1` et `layer2-v1.0`.

**État au 19 octobre 2026.** Audit fait : 0 erreur, HermiT cohérent ; les six avertissements
restants sont des propriétés qui ne servent qu'à décrire un modèle précis (voir
`couche2.md`). Test de disjonction refait : incohérence signalée, comme attendu.
Restent à faire : OOPS!, et l'étiquette de version au moment de publier. La règle a changé
depuis ce plan : il n'y a plus une étiquette par couche, le numéro suit l'empilement entier et
une seule étiquette Git marque les neuf modules ensemble (voir `couche2.md`,
*Versionnement*).
