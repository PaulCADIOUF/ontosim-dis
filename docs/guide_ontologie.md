# OntoSim-Dis — Guide : où se trouve quoi

Ce guide sert à une chose : quand on vous parle de population, de transmission, de
compartiment ou de coût, vous devez savoir **dans quel fichier cela se trouve, et pourquoi**.

Neuf fichiers, 325 termes au 18 octobre 2026. Voici la carte. Les nombres de termes à jour
sont en tête de `index_termes.md`, que le script `tools/index_termes.py` régénère.

---

# 1. Le principe en une phrase

Chaque couche répond à **une question différente**, et c'est la question qui décide où va un
terme.

| Couche | Question | Exemple de terme |
|---|---|---|
| **Couche 1** | Qu'est-ce qui existe, au sens le plus général ? | processus, information, disposition |
| **Couche 2** | Comment modélise-t-on ? | modèle, paramètre, état, transition |
| **Couche 3** | Avec quel paradigme ? | compartiment, flux, agent, interaction |
| **Couche 4** | Que modélise-t-on ? | maladie, état de santé, population, pathogène |
| **Couche 5** *(à venir)* | Quel cas précis ? | un modèle SIR publié, la schistosomiase au Sénégal |

**La règle de décision :** avant d'ajouter un terme, demandez-vous à quelle question il répond.
Si c'est « comment modéliser », il va en couche 2, même s'il parle de maladie dans votre tête.
Si c'est « que modélise-t-on », il va en couche 4, même s'il ressemble à un élément de modèle.

---

# 2. Les neuf fichiers

## Couche 1 — `layer1_foundational.ttl` (22 termes)

**Aucun terme n'est de vous.** Ce fichier ne contient que des termes recopiés de BFO, RO et
IAO : les catégories les plus générales qui existent — une chose, un processus, une
information, une disposition — et les relations qui les lient.

**Ce qu'on y cherche :** `process`, `disposition`, `information content entity`, `part of`,
`realized in`.

**Ce qu'on n'y met jamais :** rien de médical, rien de simulation. C'est écrit dans sa
définition : indépendante de tout domaine.

## Couche 2 — `layer2_modsim.ttl` (105 termes)

**Le vocabulaire de la simulation, valable pour tous les paradigmes et toutes les maladies.**

Ce qu'on y trouve, en six familles :

- **Le modèle et ce qui le décrit** : `SimulationModel`, `ModelStructureKnowledge` (le MSK du
  Quadruplet), `ExecutionKnowledge` (l'EK : quel simulateur, combien de répétitions, quelle
  graine aléatoire)
- **Les composants** : `StateComponent`, `TransitionComponent`, `ModelParameter`,
  `RuleComponent`, `EnvironmentComponent`
- **L'exécution** : `SimulationScenario`, `SimulationExecution`, `SimulationResult`,
  `SimulationObservation`
- **Les listes de valeurs** : le traitement du hasard (déterministe ou stochastique), le temps
  (continu ou discret), l'espace, la granularité, la méthode de validation
- **Le classement du modèle**, en trois listes : sa nature (`ModelNature` : mécaniste,
  empirique ou mixte), sa portée (`ModelScope` : générale ou spécifique) et son objectif
  (`ModelPurpose` : explorer une dynamique, anticiper une épidémie, améliorer les méthodes,
  étudier une épidémie passée). Elles servent à juger si un modèle peut être réutilisé ou
  recomposé pour une autre situation.
- **Les sept lois de probabilité**, reprises d'OSDi : bêta, gamma, normale, uniforme,
  exponentielle, Poisson, Bernoulli. Tout paramètre peut porter la sienne, pour dire son
  incertitude.

**Le piège à connaître.** `StateComponent` est une pièce de modèle, pas un état médical.
« Susceptible » ne se met pas ici.

## Couche 3 — deux fichiers, un par paradigme

Chacun répond à : comment ce modèle est-il construit ?

### `layer3a_mas.ttl` — agents (22 termes)
`AgentBasedModel`, `AgentType`, `AgentState`, `AgentTransition`, `InteractionType`, `Behavior`.
Le couplage y prend la forme d'une **transition déclenchée par une interaction**
(`InteractionTriggeredTransition`). C'est une classe définie : le raisonneur reconnaît seul
toute transition d'agent déclenchée par une interaction.

### `layer3b_equations.ttl` — compartiments (21 termes)
`CompartmentalModel`, `Compartment`, `TransitionFlow`, `RateSpecification`,
`DifferentialEquation`.
Le couplage y prend la forme d'un **taux qui dépend du contenu d'un compartiment**
(`CompartmentDependentRate`).

### Et les événements discrets ?
La couche 3C, celle des événements discrets (le paradigme de JaDES), a été retirée le
9 octobre 2026. Son retour reste à décider. En attendant, rien dans l'ontologie ne décrit une
activité, une ressource ou une file d'attente.

**Ce qu'on ne met jamais en couche 3 :** rien de médical. Pas de « patient infecté », pas de
« vaccination ». Un agent est un agent, un compartiment est un compartiment ; ce qu'ils
représentent se dit en couche 4.

## Couche 4 — cinq fichiers

### `layer4-ogms.ttl` — les termes empruntés (10 termes)
**Aucun terme n'est de vous.** Ce sont les termes d'OGMS, l'ontologie de référence de la
maladie : `disease`, `disorder`, `disease course` et ses quatre formes (aiguë, chronique,
progressive, transitoire), `organism population`, `extended organism`,
`predisposition to disease of type X`.

**Pourquoi un fichier à part :** pour qu'on voie d'un coup d'œil ce qui n'est pas de vous.

### `layer4_core.ttl` — le cœur (59 termes)
**Ce qui vaut pour toute maladie, transmissible ou non.**

- `DiseaseKnowledgeTemplate` — le DK du Quadruplet
- `HealthState`, `HealthStateTransition`
- `TransitionDeterminant`, avec ses deux branches : couplé à la population
  (`PopulationCoupledDeterminant`) ou individuel (`IndividualDeterminant`)
- `CouplingSource` — ce dont un déterminant couplé lit l'effectif : un état de santé, ou un
  état de réservoir déclaré en 4-Infectious
- `IndividualAttribute`, `RiskFactor`
- Les interventions : pharmaceutique, non pharmaceutique, de détection (dépistage, diagnostic)
- Les classes définies qui rangent une maladie : couplée ou à progression individuelle, et
  selon la forme de son cours
- **Les trois ponts** vers les modèles : `representsHealthState`, `representsStateTransition`,
  `realisesDeterminant` ; et le lien vers la maladie réelle d'OGMS : `representsDisease`

**C'est le fichier le plus important de toute l'ontologie.** C'est là que se trouve la
distinction qui fait votre contribution.

### `layer4-context.ttl` — le contexte (34 termes)
**Où, pour qui, dans quelles conditions.** C'est le CK du Quadruplet.

`ContextKnowledge`, `Population`, `GeographicRegion` avec ses quatre niveaux, `Climate`,
`HealthInfrastructure`.

**C'est ce qui vous distingue le plus d'OSDi**, dont la population est une cohorte clinique
sans géographie.

### `layer4_infectious.ttl` — l'extension transmissible (49 termes)
**Uniquement ce qui est propre aux maladies qui se transmettent.**

`InfectiousDiseaseKnowledge`, `Pathogen` et ses quatre sortes, les dix voies de transmission,
les quatre rôles épidémiologiques, les interventions qui réduisent la transmission, les
périodes de latence, d'incubation et de contagiosité.

C'est aussi là que se trouvent les **états de réservoir** (`ReservoirState`) : l'effectif d'un
stade libre du pathogène dans un milieu, comme les cercaires dans l'eau, ou d'un hôte non
humain, comme les escargots infectés. Une maladie infectieuse qui en déclare un est rangée
seule parmi les maladies à transmission environnementale
(`EnvironmentallyMediatedDiseaseKnowledge`). C'est ce qui rend la schistosomiase
représentable. Le cycle de l'escargot lui-même, c'est-à-dire la façon dont cet effectif
évolue, n'est pas encore décrit.

### `layer4-checks.ttl` — les contrôles (3 termes)
**Ce qui compare un modèle à la maladie qu'il représente.** Ce fichier ne décrit ni une
maladie ni un modèle : ses trois classes définies repèrent les **approximations statiques**,
c'est-à-dire les modèles qui représentent une transition couplée sans en réaliser le
couplage.

- `StaticApproximationFlow` — un flux qui représente une transition couplée, avec un taux
  constant
- `StaticApproximationAgentTransition` — une transition d'agent qui représente une transition
  couplée, mais que déclenchent les seuls attributs de l'agent
- `StaticApproximationModel` — un modèle qui contient au moins l'un des deux

**Pourquoi un fichier à part :** c'est le seul qui lit à la fois la maladie (4-Core) et les
paradigmes (3A, 3B). Mis en 4-Core, ces contrôles auraient fait dépendre la description de la
maladie des paradigmes.

## Couche 5 — à venir

Un fichier par cas étudié, du modèle SIR le plus simple à la schistosomiase au Sénégal. Chacun
décrira son cas avec le vocabulaire des couches 1 à 4 : la maladie, le contexte, le modèle et
ses paramètres. Ces fichiers viendront avec la représentation et la simulation des modèles,
dans `src/applications/`.

---

# 3. Le cas « population », pour bien comprendre

C'est le meilleur exemple, parce que l'idée de population apparaît **à cinq endroits
différents**, et que ce ne sont pas la même chose.

| Où | Terme | Ce que c'est |
|---|---|---|
| 4-Context | `Population` | Un groupe de gens dans un territoire, avec sa taille et sa densité |
| Module OGMS | `organism population` | La population réelle, au sens biologique |
| 3B | `Compartment` | Une case du modèle, qui compte ensemble les individus d'une même situation |
| 4-Core | `dependsOnCountIn` | La relation disant qu'un risque dépend d'un effectif |
| 4-Infectious | `NonHumanHostState` | L'effectif d'une population non humaine, comme les escargots infectés |

**Comment choisir.** On vous parle du Sénégal et de sa densité ? C'est 4-Context. On vous parle
du nombre d'infectés à un instant donné dans un modèle ? C'est un compartiment de 3B. On vous
parle de la force d'infection ? C'est le déterminant de 4-Core. On vous parle des escargots
infectés d'un point d'eau ? C'est un état de réservoir de 4-Infectious.

---

# 4. Le même mécanisme, vu à trois endroits

C'est l'idée centrale de votre ontologie. **Une maladie est décrite une fois, et chaque
paradigme s'y rattache.**

| Niveau | Terme | Fichier |
|---|---|---|
| La maladie | `PopulationCoupledDeterminant` | 4-Core |
| En compartiments | `CompartmentDependentRate` | 3B |
| En agents | `InteractionTriggeredTransition` | 3A |

Les deux formes de modèle sont reliées à la maladie par la même relation,
`realisesDeterminant`, déclarée en 4-Core.

Le raisonneur fait le reste. Il range seul un modèle parmi les modèles couplés
(`CoupledCompartmentalModel`, `CoupledAgentBasedModel`) dès qu'il contient un taux qui lit un
compartiment ou une transition déclenchée par une interaction. Et si un modèle représente une
transition couplée sans en réaliser le couplage, 4-Checks le range parmi les approximations
statiques.

---

# 5. Quand on vous demande, cherchez ici

| On vous parle de… | Regardez dans |
|---|---|
| une maladie, ses états, comment on passe de l'un à l'autre | 4-Core |
| un agent pathogène, une voie de transmission, l'incubation | 4-Infectious |
| un réservoir : des escargots infectés, des cercaires dans l'eau | 4-Infectious |
| une population, une région, un climat, un hôpital | 4-Context |
| un modèle, ses paramètres, son exécution, son simulateur | Couche 2 |
| un modèle mécaniste ou empirique, général ou spécifique, son objectif | Couche 2 |
| une loi de probabilité, une incertitude | Couche 2 |
| un compartiment, un flux, une équation différentielle | 3B |
| un agent, une interaction, un comportement | 3A |
| un modèle qui ignore le couplage de la maladie | 4-Checks |
| une vaccination, un traitement, un dépistage | 4-Core |
| une quarantaine, un masque, une distanciation | 4-Infectious |
| une activité, une ressource, une file, un événement daté | **nulle part pour l'instant — la couche 3C a été retirée** |
| un coût, une utilité, un QALY | **nulle part — hors périmètre, c'est OSDi** |

---

# 6. Les six pièges qui reviennent

**1. État de santé contre composant d'état.** `HealthState` est en 4-Core : c'est une
connaissance sur la maladie. `StateComponent` est en couche 2 : c'est une pièce de modèle. Un
compartiment **représente** un état de santé ; il n'en est pas un.

**2. Deux relations qui se ressemblent.** `hasSourceState` en couche 2 relie des composants de
modèle. `hasSourceHealthState` en 4-Core relie des connaissances. Ne les confondez pas.

**3. Infectieux n'est pas couplé.** Une maladie est infectieuse si elle a un pathogène. Elle est
couplée si un de ses déterminants dépend d'un effectif. Ce sont deux règles séparées.

**4. Le paradigme ne connaît pas la maladie.** Si vous avez envie d'écrire « patient infecté »
en couche 3, c'est que le terme va en couche 4.

**5. Des noms qui trompent.** `ParadigmType` ne donne pas le paradigme (agents ou
compartiments), mais le traitement du hasard : déterministe ou stochastique. `ConstantRate` ne
veut pas dire fixe dans le temps, mais indépendant des compartiments : un taux saisonnier en
est un. Lisez la définition, pas seulement le nom.

**6. Signalé n'est pas interdit.** Un modèle que 4-Checks range parmi les approximations
statiques n'est pas faux : il ignore les effets indirects, comme l'immunité de groupe. C'est
acceptable quand l'intervention étudiée ne change pas la transmission. Le raisonneur le
signale ; c'est à vous d'en juger.

---

# 7. Le Quadruplet, où sont ses quatre pattes

| Composant | Terme | Fichier |
|---|---|---|
| **DK** — connaissance de maladie | `DiseaseKnowledgeTemplate` | 4-Core |
| **CK** — connaissance de contexte | `ContextKnowledge` | 4-Context |
| **MSK** — connaissance de structure | `ModelStructureKnowledge` | Couche 2 |
| **EK** — connaissance d'exécution | `ExecutionKnowledge` | Couche 2 |

Les quatre pattes sont en place : l'EK a été ajoutée en couche 2, comme le prévoyait la
décision D17.

---

# 8. Pour chercher un terme précis

Le fichier `index_termes.md` donne tous les termes par ordre alphabétique, avec pour chacun son
module, sa nature et sa définition. Ne le modifiez pas à la main : après chaque changement de
l'ontologie, régénérez-le depuis la racine du dépôt avec

    python tools/index_termes.py

Pour un module précis, sa **fiche** donne le détail : contenu, raisons des choix, résultats
de l'audit et des tests, décisions. Il y en a six, dans `docs/` : `couche1.md`, `couche2.md`,
`couche3a.md`, `couche3b.md`, `couche4-core.md` et `couche4-context.md`. Les modules OGMS,
4-Infectious et 4-Checks n'en ont pas encore. La liste de tous les documents est dans
`docs/README.md`.
