# OntoSim-Dis, Couche 4-Core : noyau de la connaissance de la maladie

**Fichier :** `src/ontology/layer4_core.ttl`
**IRI :** `https://w3id.org/ontosim-dis/layer4-core`, version `https://w3id.org/ontosim-dis/layer4-core/1.0`
**Importe :** `https://w3id.org/ontosim-dis/layer2/1.0` et `https://w3id.org/ontosim-dis/layer4-ogms/1.0`
**Licence :** CC BY 4.0
**Statut :** contenu de la v1.1, numéro encore à 1.0.

## Rôle

4-Core répond à : **que modélise-t-on ?** C'est le module qui porte la contribution
scientifique de la thèse, la distinction entre un risque couplé à l'effectif d'une source et
un risque individuel et c'est aussi celui qui tient les ponts vers la couche 2.

**C'est un noyau commun à toutes les maladies**, pas seulement aux infectieuses. C'est la raison
du renommage OntoSim-Epi → OntoSim-Dis (décision A1) : les types de maladies se dérivent du
noyau, ils ne le définissent pas.

## Contenu

**24 classes, 23 propriétés d'objet, 12 propriétés de données, 8 classes définies,
26 restrictions, 4 disjonctions, 20 alignements.** 554 triplets, le module le plus dense.

### La maladie et ses pièces

| Classe | Parent | Ce qu'elle impose |
|---|---|---|
| `DiseaseKnowledgeTemplate` | `SimulationKnowledgeArtifact` | représente au moins une `disease` d'OGMS ; au moins **2** états de santé ; au moins 1 transition ; les formes de cours uniquement des `disease course` ; les facteurs de risque uniquement des `RiskFactor` |
| `HealthState` | **`CouplingSource`** | représente une phase d'un `disease course` |
| `HealthStateTransition` | `SimulationKnowledgeArtifact` | exactement 1 état de départ, 1 état d'arrivée ; au moins 1 déterminant |
| `IndividualAttribute` | `SimulationKnowledgeArtifact` |, |
| `RiskFactor` | `SimulationKnowledgeArtifact` |, |

**`HealthState` n'est pas un composant de modèle** (décision D18). C'était l'erreur de fond de
l'ancienne couche 4 où `SusceptibleState` et `InfectiousState` étaient à la fois des états
médicaux et des compartiments SEIR. Un état de santé est une **connaissance sur la maladie** ;
un compartiment ou un état d'agent est une **pièce de modèle qui le représente**, par
`representsHealthState`.

**Le « au moins 2 états de santé »** dit ce qu'une maladie exige pour être modélisable : s'il n'y
a qu'un état, il n'y a pas de dynamique.

### Les déterminants, le cœur de la thèse

| Classe | Parent | Ce qu'elle impose |
|---|---|---|
| `TransitionDeterminant` | `SimulationKnowledgeArtifact` | **définie** : `IndividualDeterminant or PopulationCoupledDeterminant` ; quantifiée uniquement par des `ModelParameter` |
| `IndividualDeterminant` | `TransitionDeterminant` | dépend d'au moins 1 `IndividualAttribute` |
| `PopulationCoupledDeterminant` | `TransitionDeterminant` | dépend de l'effectif d'au moins 1 **`CouplingSource`** |

Les deux sortes sont **déclarées disjointes**.

**`CouplingSource`**. Avant, le déterminant
couplé dépendait de l'effectif d'un `HealthState` : cela couvre la grippe et le COVID et exclut
la schistosomiase, où ce qui fait varier le risque est le nombre de cercaires dans un point
d'eau ou d'escargots infectés, qui ne sont pas des états de santé, puisque l'entité comptée
n'est pas l'individu dont on modélise la maladie.

```
CouplingSource
├── HealthState       (ici, 4-Core)
└── ReservoirState    (4-Infectious)
```

Le critère structurel passe ainsi de « risque couplé à l'état de la population humaine » à
**« risque couplé à l'effectif d'une source »**, plus général et plus exact.

**`quantifiedBy` porte sur `ModelParameter`** et non sur un `EpidemiologicalParameter` :
`osdi:EpidemiologicalParameter` désigne la prévalence et l'incidence, c'est-à-dire une mesure de
fréquence et non le taux qui gouverne une transition.

### Les 8 classes définies

Ce que le raisonneur sait déduire seul.

| Classe définie | Équivalence |
|---|---|
| `TransitionDeterminant` | `IndividualDeterminant or PopulationCoupledDeterminant` |
| `CoupledTransition` | `HealthStateTransition and (isGovernedBy some PopulationCoupledDeterminant)` |
| `CoupledDiseaseKnowledge` | `DiseaseKnowledgeTemplate and (hasStateTransition some CoupledTransition)` |
| `IndividualProgressionDiseaseKnowledge` | `DiseaseKnowledgeTemplate and (hasStateTransition only (isGovernedBy only IndividualDeterminant))` |
| `AcuteCourseDiseaseKnowledge` | `… and (hasDiseaseCourseShape some OGMS_0000094)` |
| `ChronicCourseDiseaseKnowledge` | `… and (hasDiseaseCourseShape some OGMS_0000064)` |
| `ProgressiveCourseDiseaseKnowledge` | `… and (hasDiseaseCourseShape some OGMS_0000065)` |
| `TransientCourseDiseaseKnowledge` | `… and (hasDiseaseCourseShape some OGMS_0000066)` |

**Deux axes de classification indépendants.** Le déterminant, couplé ou individuel et la
forme du cours, aiguë, chronique, progressive, transitoire. Une grippe est à la fois à cours
aigu et couplée et un diabète à cours chronique et individuel. Les deux autres combinaisons sont
possibles et rien ne les interdit. Les deux axes se croisent sans se confondre et c'est le
raisonneur qui place chaque maladie dans les deux.

**`AcuteCourseDiseaseKnowledge` a été ajoutée. OGMS découpe les
cours en quatre ; trois seulement avaient leur pendant. Exercée par
`tests/test_forme_du_cours.ttl`.

**`IndividualProgressionDiseaseKnowledge` n'est pas inférée et c'est la limite L1.** Dire
« toutes ses transitions sont individuelles » exige de prouver qu'il n'en existe pas d'autres,
ce qu'OWL en monde ouvert ne peut pas savoir. Avec deux axiomes de fermeture, la liste des
transitions de la maladie, la liste des déterminants de chaque transition, la classification
fonctionne. **PS.** : la détection positive du couplage marche sans rien
de spécial, la détection négative demande une fermeture explicite.

### Les cinq sous-propriétés d'`IAO:is about`

Un élément de modèle **parle de** quelque chose sans en être. Cinq propriétés le disent et
trois d'entre elles sont les **ponts de la décision D14** :

| Propriété | Domaine → Portée | Pont D14 ? |
|---|---|---|
| `representsHealthState` | **`StateComponent`** → `HealthState` | **oui** |
| `representsStateTransition` | **`TransitionComponent`** → `HealthStateTransition` | **oui** |
| `realisesDeterminant` | **`ModelComponent`** → `TransitionDeterminant` | **oui** |
| `representsDisease` | `DiseaseKnowledgeTemplate` → `OGMS:disease` | non |
| `representsPhaseOf` | `HealthState` → `OGMS:disease course` | non |

**Le point décisif : les domaines des trois premières sont des classes de la couche 2.** Un
compartiment (3B), un état d'agent (3A) et une étape de flux en héritent automatiquement. **La
couche 4 n'a donc pas besoin d'importer la couche 3** et une couche de paradigme future
héritera des ponts sans qu'on y touche.

> **PS.** Les trois ponts sont déclarés avec domaine et portée mais
> n'apparaissent dans **aucun axiome et aucun individu** des huit fichiers : l'audit les signale
> comme propriétés jamais utilisées. **Le pont est correct et il est vide.** C'est normal, il
> sert à décrire des modèles réels, ce qui vient après, mais ne l'écrivez pas comme un résultat
> acquis dans l'article sans joindre le jeu d'essai qui le montre. C'est le troisième test
> fonctionnel à écrire (M7).


### Les interventions

| Classe | Parent | Ce qu'elle impose |
|---|---|---|
| `Intervention` | `SimulationKnowledgeArtifact` | modifie au moins 1 déterminant |
| `PharmaceuticalIntervention` | `Intervention` |, |
| `Treatment`, `Vaccination` | `PharmaceuticalIntervention` |, |
| `NonPharmaceuticalIntervention` | `Intervention` |, |
| `DetectionIntervention` | `Intervention` | exactement 1 sensibilité et 1 spécificité, chacune un `ModelParameter` |
| `ScreeningIntervention`, `DiagnosisIntervention` | `DetectionIntervention` | disjointes entre elles |

`PharmaceuticalIntervention` ⊥ `NonPharmaceuticalIntervention`. La sensibilité et la spécificité
sont des **paramètres de modèle**, pas des nombres bruts : elles peuvent donc porter une loi
d'incertitude (couche 2).

Les six interventions non pharmaceutiques concrètes, isolement, quarantaine, masque etc.,
sont en 4-Infectious, avec la classe définie `TransmissionReducingIntervention`.

### Les références externes sont des textes

`hasRefToICD`, `hasRefToSNOMED`, `hasRefToDO` sont des **propriétés de données** mais pas des
alignements logiques. **On cite sans s'engager** : déclarer une équivalence OWL avec un code
CIM-10 engagerait le raisonneur sur une sémantique qu'on ne maîtrise pas. Les trois sont alignées
en `exactMatch` sur leurs équivalents OSDi, qui font le même choix.

### Disjonctions

Cinq classes mutuellement exclusives : `HealthState`, `HealthStateTransition`,
`IndividualAttribute`, `RiskFactor`, `TransitionDeterminant`. Plus les trois paires :
individuel ⊥ couplé, pharmaceutique ⊥ non pharmaceutique, dépistage ⊥ diagnostic.

### 20 alignements, 19 vers OSDi, 1 vers OGMS

**12 `exactMatch` :** `detects`, `hasEndAge`, `hasOnsetAge`, `hasSensitivity`, `hasSpecificity`,
`hasRefToDO`, `hasRefToICD`, `hasRefToSNOMED`, `DetectionIntervention`,
`DiagnosisIntervention`, `ScreeningIntervention`, `IndividualAttribute` → `osdi:Attribute`.

**7 `closeMatch` :** `DiseaseKnowledgeTemplate` → `osdi:Disease` ; `HealthState` →
`osdi:ClinicalProgressionElement` ; `HealthStateTransition` → `osdi:Pathway` ; `Intervention` →
`osdi:Intervention` ; `PharmaceuticalIntervention` → `osdi:TherapeuticIntervention` ;
`supersedesHealthState` → `osdi:supersedesClinicalProgression` ; `RiskFactor` →
`OGMS_0000030`.

**1 `relatedMatch` :** `TransitionDeterminant` → `osdi:hasRiskCharacterization`.

**Ce dernier alignement est le plus parlant de toute l'ontologie.** `TransitionDeterminant` est
une **classe** ; `osdi:hasRiskCharacterization` est une **propriété**.

---

## Validation

### 1. Audit automatique

**Résultat au 2026-10-08 : 0 erreur, 7 avertissements.** Le seul des huit fichiers sans erreur,
avec la couche 1.

Les sept avertissements signalent des propriétés déclarées sans axiome : `detects`, `hasEndAge`,
`hasOnsetAge`, `realisesDeterminant`, `representsHealthState`, `representsStateTransition`,
`supersedesHealthState`.

**Trois d'entre elles sont les ponts de D14.** Elles ne sortent pas : elles ont besoin d'un jeu
d'essai, pas d'une suppression. Les quatre autres relèvent de la revue finale.

HermiT : aucune classe insatisfiable.

```
python3 tools/audit_ontosim.py --focus layer4_core.ttl \
    --load layer1_foundational.ttl layer2_modsim.ttl layer4-ogms.ttl layer4_core.ttl \
    --ref tools/refs/*.owl
```

### 2. Test de classification

`tests/test_forme_du_cours.ttl`, une grippe à cours aigu est classée
`AcuteCourseDiseaseKnowledge`, un diabète à cours chronique tombe dans
`ChronicCourseDiseaseKnowledge` et aucune des deux n'entre dans la classe de l'autre.


### 3. Test à écrire

Un compartiment déclarant `representsHealthState` vers un état d'une
maladie couplée doit permettre de retrouver, par requête, que ce modèle représente cette
maladie. **C'est le test manquant**.

### 4. OOPS! 

A FAIRE
---

## Décisions consignées

| Code | Décision |
|---|---|
| D14 | Trois ponts, posés au niveau de la couche 2. La couche 4 n'importe pas la couche 3. |
| D16 | La couche 4 en trois modules. `DiseaseParameterSet` et `ClinicalState` supprimés. |
| D18 | `HealthState` est un artefact d'information, pas un composant de modèle. |
| D19 | Le déterminant couplé dépend d'un **effectif**, pas d'une population. |
| D22 | `CouplingSource` : le couplage n'est plus réservé aux états de santé humains. |
| D26 | Les quatre formes de cours d'OGMS ont chacune leur classe définie. |
| D28 | `rdfs:comment` est la définition ; les notes de travail vont dans `obo:IAO_0000116`. |
|- | `quantifiedBy` porte sur `ModelParameter`, pas sur `EpidemiologicalParameter`. |
|- | Le nom `hasSourceHealthState`, distinct de `hasSourceState` de la couche 2. |
|- | Les références externes sont des textes : on cite sans s'engager. |
| L1 | La détection négative du couplage demande des axiomes de fermeture. Découverte ici. |

---

## Versionnement

Le fichier porte `1.0` alors que son contenu est celui de la v1.1 : `CouplingSource` et
`AcuteCourseDiseaseKnowledge` ont été ajoutés après. Il est importé par 4-Infectious, qui devra
suivre la renumérotation.

```
git add src/ontology/layer4_core.ttl docs/couche4-core.md
git commit -m "docs : fiche de la couche 4-Core (D22, D26)"
```

<br>

<p align="center">
  🦋<br>
  <i>Fais avec amour et pour l'Amour.</i>
</p>