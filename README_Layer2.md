# OntoSim-Dis — Couche 2 : modélisation et simulation

Fichier : layer2_modsim.ttl
IRI :  https://w3id.org/ontosim-dis/layer2 
version : 1.0
Importe : https://w3id.org/ontosim-dis/layer1/1.0`
Licence : CC BY 4.0
Statut : prête à être fermée à la version 1.0.

## Rôle
Cette couche contient les concepts de simulation qui sont communs à tous les paradigmes que ca soient compartimental, agents, événements discrets et rappellons aussi qu'aucun terme de cette couche ne parle de maladie donc elle est independants de tout domaine médical.

## Contenu
22 classes, 13 propriétés d'objet, 19 propriétés de données, 16 individus.

### Racine et modèle
- SimulationKnowledgeArtifact
- SimulationModel avec exactement 1 structure / au moins 1 paramètre / au moins 1 méthode de validation / au moins 1 scénario
- ModelStructureKnowledge avec au moins 1 composant / exactement 1 paradigme, 1 type de temps, 1 type d'espace, 1 niveau de granularité
ModelStructureKnowledge est quand meme composant MSK du Quadruplet de recomposition mais sur cette premiere version la recomposition n'est pas travaillée comme etant une priorité.

### Composants du modèle
ModelComponent
StateComponent
TransitionComponent avec exactement 1 état de départ et 1 état d'arrivée
RuleComponent
EnvironmentComponent
ModelParameter
StaticParameter
DynamicParameter
InitialCondition

### Exécution, résultats, scénarios
SimulationExecution avec exactement 1 modèle exécuté
SimulationResult
SimulationObservation
SimulationScenario
InterventionScenario

Il est important de rappeler que SimulationExecution est un processus et non un artefact d'information car elle se deroule dans le temps.
Notez aussi que SimulationObservation designe les donnees reelles observees qui sont necessaires pour valider un modele de comparaison.

### Listes de valeurs fermées

Chaque classe est définie par la liste exacte de ses valeurs  
les 16 individus sont déclarés tous différents.  

ParadigmType     :: DETERMINISTIC, STOCHASTIC  
TemporalType     :: CONTINUOUS, DISCRETE  
SpatialType      :: NON_SPATIAL, NETWORK, GRID, GIS  
GranularityLevel :: INDIVIDUAL, GROUP, REGIONAL, MULTISCALE  
ValidationMethod :: ADEQUACY, CROSS_MODEL, HISTORICAL_DATA, STATISTICAL

### Propriétés d'objet (13)
Propriétés (Domaine-->Portée)

hasStructureKnowledge (SimulationModel --> ModelStructureKnowledge)
hasComponent (ModelStructureKnowledge --> ModelComponent)
hasParameter (SimulationModel --> ModelParameter)
hasSourceState (TransitionComponent --> StateComponent)
hasTargetState (TransitionComponent --> StateComponent)
hasParadigm (ModelStructureKnowledge --> ParadigmType)
hasTemporalType (ModelStructureKnowledge --> TemporalType)
hasSpatialType (ModelStructureKnowledge --> SpatialType)
hasGranularityLevel (ModelStructureKnowledge --> GranularityLevel)
hasValidationMethod (SimulationModel --> ValidationMethod)
usesScenario (SimulationModel --> SimulationScenario)
executesModel (SimulationExecution --> SimulationModel)
producesResult (SimulationExecution --> SimulationResult)

### Propriétés de données (19)
- Propriétes dont SimulationModel est le domain : modelName, modelDescription, modelVersion, creationDate, hasAuthor  

- Propriétes dont ModelParameter est le domain : parameterName, parameterValue, defaultValue, parameterUnit  

- Propriétes dont ModelStructureKnowledge est le domain : timeStepInDays, simulationDurationInDays

- Propriétes dont SimulationExecution est le domain : simulatorName, simulatorVersion, numberOfRuns, randomSeed, executionStatus  

- Propriétes dont SimulationScenario est le domain : scenarioDurationInDays, startDate, endDate  

Pour le moment, les durees sont des nombres en jours et l'unité est inscrite dans le nom pour éviter toute ambiguité.

### Disjonctions
Les 5 éléments de composants s'excluent. C'est StateComponent, TransitionComponent, RuleComponent, EnvironmentComponent, ModelParameter.  

Un parametre ne peut pas etre à la fois constant et variable dans le temps.

### Alignements
Nous avons des classes/propriétés qui s'alignent avec OSDi. Parmi elles nous avons :  
SimulationModel qui s'aligne avec osdi:Model  
ModelParameter qui s'aligne avec osdi:Parameter  
InterventionScenario qui s'aligne avec osdi:Intervention  
hasAuthor qui s'aligne avec osdi:hasAuthor  

## Validation

### 1. Audit automatique
Test réalisé le 24/09/2026 : 0 erreurs, 0 avertissements.
Ce qui prouve que l'ontologie est cohérente selon HermiT.

A noter que l'outil actuellement utilisé vérifie la forme(libellés, références, hiérarchies, caractéristiques, cohérence), il ne verifie pas reellement le sens, chose qui sera faite sur le cahier de conception.

### 2. Test des garde-fous
Un individu déclaré à la fois StaticParameter et DynamicParameter rend l'ontologie incohérente, comme attendu. Les disjonctions fonctionnent réellement.
  
### 3. OOPS!
Vérification que l'on va faire apres la création des 4 couches

## Versionnement
Plus tard !

## Décisions consignées
- L'auteur d'un modele devient un texte et non une classe c'est à dire que un chercheur est une personne et non un artefact d'information comme dans OSDi.  

- Contrairement à notre version ancienne, nous avons opté pour une seule hiérarchie de composants ce qui fait que ParameterComponent et ModelParameter sont fusionnés.  

- Pour avoir un alignement sur OSDi, nous avons opté pour mettre les types de modèles sous forme de classes et non sous formes d'individus.

- La recomposition est mise en pause, pour le moment, ici sur cette version.