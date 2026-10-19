# Spécification — OntoSim-Dis, Couche 4 : module OGMS et noyau 4-Core

> **Mise à jour du 19 octobre 2026.** Ce document a d'abord été le plan de construction des
> deux fichiers. Il décrit maintenant les fichiers tels qu'ils sont :
> `src/ontology/layer4-ogms.ttl` et `src/ontology/layer4_core.ttl`. Les écarts avec le plan
> d'origine sont signalés à leur place par la mention **Changé**.
>
> La fiche de 4-Core, avec ses résultats de validation, est `couche4-core.md`. Le module
> OGMS n'a pas encore de fiche : pour lui, ce document en tient lieu.

Plan de construction dans Protégé. **Deux fichiers, dans cet ordre** : le module d'import
OGMS d'abord, puisque 4-Core en dépend.

---

# Fichier 1 — Module d'import OGMS

| Élément | Valeur |
|---|---|
| Fichier | `src/ontology/layer4-ogms.ttl` |
| IRI | `https://w3id.org/ontosim-dis/layer4-ogms` |
| Version | `https://w3id.org/ontosim-dis/layer4-ogms/1.0` |
| Import | `https://w3id.org/ontosim-dis/layer1/1.0` |
| Source | OGMS (CC BY 4.0). L'audit compare les termes au fichier d'édition d'OGMS, `tools/ref/ogms-edit.owl`. |

**Pourquoi un fichier séparé (D1).** Ce qui n'est pas de vous reste visiblement distinct.
L'outil d'audit peut vérifier ce seul fichier contre la source officielle. Et les termes
d'IDO ou de Mondo rejoindront le même endroit.

**Deux avertissements.**

1. OGMS ne contient **aucune propriété d'objet ni aucune restriction**. Sa théorie de la
   maladie n'existe que dans les définitions textuelles. Les axiomes de liaison sont donc
   écrits dans 4-Core, pas ici.
2. Ne pas prendre ces termes dans IDO, qui en conserve des copies périmées : IDO place
   `extended organism` sous `object aggregate` alors qu'OGMS le place sous `material entity`,
   et garde pour `symptom` l'ancienne définition en qualité, révisée en processus en 2020.

Le commentaire de `hasMaterialBasisIn`, en 4-Core, en reprend l'essentiel.

## Les 10 termes importés

Le libellé et la définition officielle sont recopiés **mot pour mot** ; cinq termes ont aussi
une traduction française. **Changé :** le plan prévoyait d'annoter chaque terme avec
`dcterms:source` ; la source est donnée une seule fois, dans l'en-tête du module.

### Le triangle de la maladie

| IRI | Libellé | Parent |
|---|---|---|
| `OGMS_0000045` | disorder | `BFO_0000040` material entity |
| `OGMS_0000031` | disease | `BFO_0000016` disposition |
| `OGMS_0000063` | disease course | `BFO_0000015` process |
| `OGMS_0000087` | extended organism | `BFO_0000040` material entity |

Sur `OGMS_0000087`, ajouter une note : la définition mentionne un *object aggregate* mais le
parent asserté est *material entity*. **Pas encore fait.**

### Formes dynamiques du cours de maladie

| IRI | Libellé | Parent |
|---|---|---|
| `OGMS_0000066` | transient disease course | `OGMS_0000063` |
| `OGMS_0000064` | chronic disease course | `OGMS_0000063` |
| `OGMS_0000065` | progressive disease course | `OGMS_0000063` |
| `OGMS_0000094` | acute disease course | `OGMS_0000063` |

**Pourquoi elles comptent.** C'est une classification par la **dynamique**, non par le type de
maladie, et elle contraint la structure du modèle indépendamment du déterminant : retour
possible à l'état sain, état absorbant requis, progression monotone.

### Prédisposition et population

| IRI | Libellé | Parent |
|---|---|---|
| `OGMS_0000030` | predisposition to disease of type X | `BFO_0000016` |
| `OGMS_0000084` | organism population | `BFO_0000040` |

### Termes prévus mais non gardés

**Changé :** le plan prévoyait 21 termes. Les onze suivants n'ont pas été gardés, parce
qu'aucun module ne les utilise (principe MIREOT) : `disease stage` (`OBI_0000278`), `onset`,
`remission`, `relapse`, `manifestation of a disease`, `symptom`, `recovered from disease`,
`bodily process`, `pathological bodily process`, `infectious disease process`,
`etiological process`.

S'ils reviennent un jour, deux points relevés pendant la conception restent valables : dans
la version courante d'OBI, le parent asserté de `OBI_0000278` est `GO_0008150`, alors
qu'OGMS le place sous `BFO_0000015` ; et `bodily process` (`OGMS_0000060`) n'a pas de
définition dans OGMS, ce qu'il faut indiquer plutôt que d'en inventer une.

---

# Fichier 2 — Couche 4-Core

| Élément | Valeur |
|---|---|
| Fichier | `src/ontology/layer4_core.ttl` |
| IRI | `https://w3id.org/ontosim-dis/layer4-core` |
| Version | `https://w3id.org/ontosim-dis/layer4-core/1.0` |
| Imports | `layer2/1.0` **et** `layer4-ogms/1.0` |

## Rôle

Répond à la question : **que modélise-t-on ?** Indépendant du type de maladie : ce qui est
propre aux maladies infectieuses est en 4-Infectious, le contexte en 4-Context, et les
contrôles entre maladie et modèles en 4-Checks.

**Principe central.** La frontière entre branches n'est pas médicale — transmissible contre
non transmissible — mais **structurelle** : le risque d'un individu dépend-il de l'état des
autres, ou seulement de ses propres attributs ? C'est cette distinction qui décide de la
famille de modèles utilisable.

## 1. Les axiomes qu'OGMS n'écrit pas

OGMS énonce sa théorie en texte seulement. On la rend calculable ici.

```
ds:hasMaterialBasisIn   domaine : OGMS:disease   portée : OGMS:disorder

OGMS:disease  ⊑ hasMaterialBasisIn some OGMS:disorder
OGMS:disease  ⊑ realized in only OGMS:disease course
OGMS:disorder ⊑ part of some OGMS:extended organism
```

`hasMaterialBasisIn` est déclarée chez vous, et non reprise d'IDO, pour ne pas dépendre d'une
ontologie dont on a vu qu'elle transporte des copies périmées.

## 2. Classes (16 nommées + 8 définies)

Préfixe `ds:` = `https://w3id.org/ontosim-dis#` (les fichiers utilisent `dsim:`).

### DK — la connaissance de maladie

| Classe | Parent | Restrictions |
|---|---|---|
| `ds:DiseaseKnowledgeTemplate` | `ds:SimulationKnowledgeArtifact` | `representsDisease some OGMS:disease` ; `hasHealthState min 2 HealthState` ; `hasStateTransition min 1 HealthStateTransition` ; `hasDiseaseCourseShape only OGMS:disease course` ; `hasRiskFactor only RiskFactor` |

Premier composant du Quadruplet. C'est un **artefact d'information** : il est *à propos* d'une
maladie, il n'est pas la maladie. Alignement : `skos:closeMatch osdi:Disease`.

### États de santé et transitions

| Classe | Parent | Restrictions |
|---|---|---|
| `ds:HealthState` | `ds:CouplingSource` | `representsPhaseOf some OGMS:disease course` |
| `ds:HealthStateTransition` | `ds:SimulationKnowledgeArtifact` | `hasSourceHealthState exactly 1 HealthState` ; `hasTargetHealthState exactly 1 HealthState` ; `isGovernedBy min 1 TransitionDeterminant` |

**Décision D18, à ne pas manquer.** `HealthState` n'est **pas** sous `StateComponent`. C'était
l'erreur de fond de l'ancienne couche 4, où `SusceptibleState` était à la fois un état médical
et un compartiment SEIR. Un état de santé est une connaissance ; un compartiment ou un état
d'agent est une pièce de modèle qui le **représente**.

Alignements : `HealthState` → `osdi:ClinicalProgressionElement` ;
`HealthStateTransition` → `osdi:Pathway`, toutes deux en `closeMatch`.

### La source du couplage

| Classe | Parent | Restrictions |
|---|---|---|
| `ds:CouplingSource` | `ds:SimulationKnowledgeArtifact` | — |

**Changé (octobre 2026, décision D19 élargie).** Ce dont un déterminant couplé lit l'effectif
courant. Classe abstraite : on n'en crée jamais d'instance directe. Elle a deux sortes : un
état de santé humain (`HealthState`, ici) et un état de réservoir (`ReservoirState`, en
4-Infectious), comme les escargots infectés de la schistosomiase.

### Déterminants — la vraie frontière

| Classe | Parent | Restrictions |
|---|---|---|
| `ds:TransitionDeterminant` | `ds:SimulationKnowledgeArtifact` | `quantifiedBy only ModelParameter` ; **≡** `PopulationCoupledDeterminant or IndividualDeterminant` |
| `ds:PopulationCoupledDeterminant` | `ds:TransitionDeterminant` | `dependsOnCountIn min 1 CouplingSource` |
| `ds:IndividualDeterminant` | `ds:TransitionDeterminant` | — |

Les deux sous-classes sont **disjointes**. Une transition peut en revanche être gouvernée par
un déterminant de chaque sorte.

**Changé :** le plan demandait `dependsOnCountIn min 1 HealthState` ; c'est maintenant
`CouplingSource`, pour que le risque puisse dépendre d'un réservoir. Le plan demandait aussi
`dependsOnAttribute min 1 IndividualAttribute` sur `IndividualDeterminant` : la restriction
a été retirée en octobre 2026, car un déterminant individuel peut ne lire aucun attribut,
comme le taux de guérison γ du modèle SIR.

`PopulationCoupledDeterminant` est **absent d'OSDi** : c'est l'apport d'OntoSim-Dis.
`TransitionDeterminant` non plus n'a pas d'équivalent dans OSDi, qui rattache le risque à un
élément de progression clinique par la propriété `hasRiskCharacterization` ; une note de
l'éditeur le dit sur la classe.

**Décision D19.** Le déterminant couplé dépend d'un **effectif dans une catégorie**, pas
d'une population en général. C'est plus juste — la force d'infection dépend du nombre
d'infectieux — et cela évite à 4-Core de dépendre de 4-Context.

### Attributs et facteurs de risque

| Classe | Parent | Alignement |
|---|---|---|
| `ds:IndividualAttribute` | `ds:SimulationKnowledgeArtifact` | `exactMatch osdi:Attribute` |
| `ds:RiskFactor` | `ds:SimulationKnowledgeArtifact` | `closeMatch OGMS_0000030` |

### Interventions

**Changé :** absentes du plan, ajoutées depuis.

| Classe | Parent | Restrictions | Alignement |
|---|---|---|---|
| `ds:Intervention` | `ds:SimulationKnowledgeArtifact` | `modifiesDeterminant min 1 TransitionDeterminant` | `closeMatch osdi:Intervention` |
| `ds:PharmaceuticalIntervention` | `ds:Intervention` | — | `closeMatch osdi:TherapeuticIntervention` |
| `ds:NonPharmaceuticalIntervention` | `ds:Intervention` | — | — |
| `ds:Treatment`, `ds:Vaccination` | `ds:PharmaceuticalIntervention` | — | — |
| `ds:DetectionIntervention` | `ds:Intervention` | `hasSensitivity exactly 1 ModelParameter` ; `hasSpecificity exactly 1 ModelParameter` | `exactMatch osdi:DetectionIntervention` |
| `ds:DiagnosisIntervention`, `ds:ScreeningIntervention` | `ds:DetectionIntervention` | — | `exactMatch` vers les classes OSDi de même nom |

Une intervention n'a de sens formel que par le déterminant qu'elle modifie : sans
`modifiesDeterminant`, c'est une étiquette. La détection n'est ni un traitement ni une
mesure comportementale : elle a une sensibilité et une spécificité, données par des
paramètres pour pouvoir porter leur incertitude.

### Disjonctions

**Changé (octobre 2026).** Le plan déclarait disjointes, en un seul groupe, `HealthState`,
`HealthStateTransition`, `TransitionDeterminant`, `IndividualAttribute` et `RiskFactor`. Un
attribut individuel peut pourtant être un facteur de risque, comme l'âge. Il y a donc deux
groupes :

- `HealthState`, `HealthStateTransition`, `IndividualAttribute`, `TransitionDeterminant` ;
- `HealthState`, `HealthStateTransition`, `RiskFactor`, `TransitionDeterminant`.

S'y ajoutent : `IndividualDeterminant` ⊥ `PopulationCoupledDeterminant` ;
`PharmaceuticalIntervention` ⊥ `NonPharmaceuticalIntervention` ;
`DiagnosisIntervention` ⊥ `ScreeningIntervention`.

## 3. Les trois ponts (décision D14)

| Propriété | Domaine | Portée |
|---|---|---|
| `ds:representsHealthState` | `ds:StateComponent` [C2] | `ds:HealthState` |
| `ds:representsStateTransition` | `ds:TransitionComponent` [C2] | `ds:HealthStateTransition` |
| `ds:realisesDeterminant` | `ds:ModelComponent` [C2] | `ds:TransitionDeterminant` |

Toutes trois **sous-propriétés de `IAO:is about`** : un élément de modèle *parle de* quelque
chose sans en être.

**Le point décisif : leurs domaines sont des classes de la couche 2.** Un compartiment [3B] et
un état d'agent [3A] en héritent automatiquement. **La couche 4 n'a donc pas besoin
d'importer la couche 3.** **Changé :** le plan citait aussi l'étape de flux de la couche 3C,
retirée le 9 octobre 2026.

## 4. Pont vers le monde réel

| Propriété | Domaine | Portée |
|---|---|---|
| `ds:representsDisease` | `DiseaseKnowledgeTemplate` | `OGMS:disease` |
| `ds:representsPhaseOf` | `HealthState` | `OGMS:disease course` |

Toutes deux sous-propriétés de `IAO:is about`. Ce sont les seuls points de contact entre la
couche informationnelle d'OntoSim-Dis et l'ontologie réaliste OGMS.

## 5. Autres propriétés d'objet (17)

| Propriété | Domaine → Portée | Fonctionnelle |
|---|---|---|
| `hasHealthState` | DiseaseKnowledgeTemplate → HealthState | non |
| `hasStateTransition` | DiseaseKnowledgeTemplate → HealthStateTransition | non |
| `hasSourceHealthState` | HealthStateTransition → HealthState | **oui** |
| `hasTargetHealthState` | HealthStateTransition → HealthState | **oui** |
| `isGovernedBy` | HealthStateTransition → TransitionDeterminant | non |
| `dependsOnCountIn` | PopulationCoupledDeterminant → CouplingSource | non |
| `dependsOnAttribute` | IndividualDeterminant → IndividualAttribute | non |
| `quantifiedBy` | TransitionDeterminant → ModelParameter [C2] | non |
| `hasRiskFactor` | DiseaseKnowledgeTemplate → RiskFactor | non |
| `supersedesHealthState` | HealthState → HealthState | non |
| `hasDiseaseCourseShape` | DiseaseKnowledgeTemplate → OGMS:disease course | non |
| `hasOnsetAge` | HealthState → ModelParameter [C2] | **oui** |
| `hasEndAge` | HealthState → ModelParameter [C2] | **oui** |
| `modifiesDeterminant` | Intervention → TransitionDeterminant | non |
| `detects` | DetectionIntervention → DiseaseKnowledgeTemplate | non |
| `hasSensitivity` | DetectionIntervention → ModelParameter [C2] | **oui** |
| `hasSpecificity` | DetectionIntervention → ModelParameter [C2] | **oui** |

Avec `hasMaterialBasisIn` (section 1), les trois ponts et les deux liens vers OGMS, 4-Core a
23 propriétés d'objet. **Changé :** les six dernières lignes du tableau ont été ajoutées
après le plan, avec les interventions et les âges.

**Attention aux noms.** `hasSourceHealthState` est distincte de `hasSourceState` de la couche 2 :
la première relie des connaissances, la seconde des composants de modèle. Ne pas les confondre.

`quantifiedBy` porte sur `ModelParameter` et **non** sur `osdi:EpidemiologicalParameter`, qui
désigne la prévalence et l'incidence — une mesure de fréquence, pas un taux de transition.

`hasOnsetAge` et `hasEndAge` donnent l'âge à partir duquel un individu peut entrer dans un état,
et celui au-delà duquel il n'y est plus. Ils passent eux aussi par un paramètre.

## 6. Classes définies (8)

```
CoupledTransition ≡ HealthStateTransition
                    ⊓ isGovernedBy some PopulationCoupledDeterminant

CoupledDiseaseKnowledge ≡ DiseaseKnowledgeTemplate
                          ⊓ hasStateTransition some CoupledTransition

IndividualProgressionDiseaseKnowledge ≡ DiseaseKnowledgeTemplate
       ⊓ hasStateTransition only (isGovernedBy only IndividualDeterminant)

TransientCourseDiseaseKnowledge   ≡ DKT ⊓ hasDiseaseCourseShape some OGMS_0000066
ChronicCourseDiseaseKnowledge     ≡ DKT ⊓ hasDiseaseCourseShape some OGMS_0000064
ProgressiveCourseDiseaseKnowledge ≡ DKT ⊓ hasDiseaseCourseShape some OGMS_0000065
AcuteCourseDiseaseKnowledge       ≡ DKT ⊓ hasDiseaseCourseShape some OGMS_0000094

TransitionDeterminant ≡ PopulationCoupledDeterminant ⊔ IndividualDeterminant
```

Le raisonneur classe ici toute maladie dont une transition dépend de l'état de la population,
**sans qu'on ait déclaré qu'elle est infectieuse**.

**Changé :** le plan en comptait 6. S'y ajoutent la forme aiguë, quatrième forme de cours
reconnue par OGMS, et `TransitionDeterminant`, définie comme l'union de ses deux sortes.

## 7. Propriétés de données (12)

| Propriété | Domaine | Type |
|---|---|---|
| `diseaseName` | DiseaseKnowledgeTemplate | string |
| `caseFatalityRate` | DiseaseKnowledgeTemplate | double, entre 0 et 1 |
| `hasRefToICD` | DiseaseKnowledgeTemplate | string — `exactMatch osdi:hasRefToICD` |
| `hasRefToDO` | DiseaseKnowledgeTemplate | string — `exactMatch osdi:hasRefToDO` |
| `hasRefToSNOMED` | DiseaseKnowledgeTemplate | string — `exactMatch osdi:hasRefToSNOMED` |
| `healthStateName` | HealthState | string |
| `isAbsorbingState` | HealthState | boolean |
| `determinantExpression` | TransitionDeterminant | string |
| `coverageRate` | Intervention | double, entre 0 et 1 |
| `interventionIntensity` | Intervention | double, entre 0 et 1 |
| `interventionStartDate` | Intervention | dateTime |
| `interventionEndDate` | Intervention | dateTime |

Les trois références externes rattachent la taxonomie médicale, **délibérément tenue hors de
la structure** de l'ontologie. **Changé :** les quatre propriétés des interventions ont été
ajoutées après le plan.

## 8. Alignements vers OSDi (18)

| Type | Termes d'OntoSim-Dis |
|---|---|
| `exactMatch` (12) | `IndividualAttribute` → `osdi:Attribute` ; `DetectionIntervention`, `DiagnosisIntervention`, `ScreeningIntervention`, `detects`, `hasSensitivity`, `hasSpecificity`, `hasOnsetAge`, `hasEndAge`, `hasRefToICD`, `hasRefToDO`, `hasRefToSNOMED` → le terme OSDi de même nom |
| `closeMatch` (6) | `DiseaseKnowledgeTemplate` → `osdi:Disease` ; `HealthState` → `osdi:ClinicalProgressionElement` ; `HealthStateTransition` → `osdi:Pathway` ; `Intervention` → `osdi:Intervention` ; `PharmaceuticalIntervention` → `osdi:TherapeuticIntervention` ; `supersedesHealthState` → `osdi:supersedesClinicalProgression` |

S'y ajoute un alignement vers OGMS : `RiskFactor` `closeMatch` `OGMS_0000030`.

---

# Contrôles

## Audit

**Résultat au 19 octobre 2026 :** 0 erreur sur chacun des deux fichiers ; HermiT les trouve
cohérents. Le module OGMS n'a aucun avertissement. 4-Core en a huit, « propriété jamais
utilisée » : `dependsOnAttribute`, `detects`, `hasEndAge`, `hasOnsetAge`,
`realisesDeterminant`, `representsHealthState`, `representsStateTransition`,
`supersedesHealthState`. Ils sont attendus : ces propriétés servent quand on décrit une
maladie ou un modèle précis, ce que feront les fichiers de la couche 5.

Pour reproduire : `bash tools/audit_tout.sh`, depuis la racine du dépôt.

## Test de classification

Décrire deux maladies : l'une avec une transition gouvernée par un déterminant couplé, l'autre
avec un déterminant individuel seulement. Vérifier que le raisonneur classe la première, et
seulement elle, sous `CoupledDiseaseKnowledge`.

**Fait le 19 octobre 2026 :** la première est classée `CoupledDiseaseKnowledge`, la seconde
ne l'est pas. La seconde n'est pas non plus classée `IndividualProgressionDiseaseKnowledge` :
c'est la limite L1, ci-dessous.

## Test du pont (le plus important)

**Changé.** Le plan attendait que le raisonneur classe un modèle comme couplé à partir du seul
couplage de la maladie. Ce n'est pas ainsi que l'ontologie fonctionne : le couplage d'un
modèle se lit sur le modèle lui-même (un taux qui lit un compartiment), et les ponts servent
à **comparer** le modèle à la maladie qu'il représente. C'est le rôle de 4-Checks.

**Fait le 19 octobre 2026**, sur un modèle compartimental [3B] dont le flux représente une
transition couplée de la maladie :

| Taux du flux | Ce que conclut le raisonneur |
|---|---|
| lit un compartiment (`CompartmentDependentRate`) | modèle couplé (`CoupledCompartmentalModel`) |
| constant (`ConstantRate`) | approximation statique (`StaticApproximationModel`, 4-Checks) |
| de sorte non précisée | rien : en monde ouvert, il ne peut pas trancher |

C'est la chaîne complète, de la connaissance médicale au paradigme. Le dernier cas dit ce que
l'outil qui produira les descriptions devra faire : toujours déclarer la sorte du taux.

## Limite connue à consigner (L1)

`IndividualProgressionDiseaseKnowledge` **ne sera pas inférée** sans axiomes de fermeture :
en monde ouvert, dire « toutes ses transitions sont individuelles » exige de prouver qu'il n'en
existe pas d'autres. Vérifié : avec deux fermetures — la liste des transitions de la maladie, et
la liste des déterminants de chaque transition — la classification fonctionne.

À écrire dans l'article plutôt qu'à cacher : la détection positive du couplage marche sans rien
de spécial, la détection négative demande une fermeture explicite.

## Limite connue à consigner (L3)

Les propriétés fonctionnelles ne protègent que si les individus sont déclarés **distincts**.
Sans `owl:AllDifferent`, donner deux états de départ à une transition ne provoque pas d'erreur :
le raisonneur conclut que les deux états sont le même. À prévoir dans l'outil qui produira les
descriptions.

---

# Décisions à consigner

| Code | Décision |
|---|---|
| D1 | OGMS dans un module d'import séparé |
| D14 | Trois ponts, posés au niveau de la couche 2, pour que la couche 4 n'importe pas la couche 3 |
| D16 | La couche 4 en plusieurs modules : Core, Context, Infectious. **Changé :** s'y ajoute 4-Checks, pour les contrôles entre maladie et modèles. |
| D18 | `HealthState` n'est pas un composant de modèle |
| D19 | Le déterminant couplé dépend d'un effectif dans une catégorie, pas d'une population. **Changé :** la catégorie est une `CouplingSource`, état de santé ou état de réservoir. |
| — | Les axiomes manquants d'OGMS sont écrits par nous, `hasMaterialBasisIn` déclarée localement plutôt que reprise d'IDO |
| — | La forme du cours de maladie comme second axe de contrainte, orthogonal au déterminant |
| — | Un attribut individuel peut être un facteur de risque : les deux classes ne sont pas disjointes (octobre 2026) |
| — | Un déterminant individuel peut ne lire aucun attribut (octobre 2026) |
| — | `TransitionDeterminant` n'a pas d'équivalent dans OSDi ; une note de l'éditeur le dit (octobre 2026) |
| — | Une approximation statique est signalée par 4-Checks, pas interdite : le modèle reste cohérent (octobre 2026) |
