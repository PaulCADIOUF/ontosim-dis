# OntoSim-Dis, Couche 4-Core : noyau de la connaissance de la maladie

**Fichier :** `src/ontology/layer4_core.ttl`
**IRI :** `https://w3id.org/ontosim-dis/layer4-core`, version `https://w3id.org/ontosim-dis/layer4-core/1.1`
**Importe :** `https://w3id.org/ontosim-dis/layer2/1.1` et `https://w3id.org/ontosim-dis/layer4-ogms/1.1`
**Licence :** CC BY 4.0
**Statut :** version 1.1. Changé en octobre 2026 : une contrainte retirée sur
`IndividualDeterminant`, les disjonctions en deux groupes, un alignement remplacé par une
note. Voir *Versionnement*.

## Rôle

4-Core répond à : **que modélise-t-on ?** C'est le module qui porte la contribution
scientifique de la thèse, la distinction entre un risque couplé à l'effectif d'une source et
un risque individuel et c'est aussi celui qui tient les ponts vers la couche 2.

**C'est un noyau commun à toutes les maladies**, pas seulement aux infectieuses. C'est la raison
du renommage OntoSim-Epi → OntoSim-Dis (décision A1) : les types de maladies se dérivent du
noyau, ils ne le définissent pas.

## Contenu

**24 classes, 23 propriétés d'objet, 12 propriétés de données, 8 classes définies,
25 restrictions, 5 disjonctions, 19 alignements.** 558 triplets. L'index des termes en compte
59. C'est le module qui a le plus de restrictions.

### La maladie et ses pièces

| Classe | Parent | Ce qu'elle impose |
|---|---|---|
| `DiseaseKnowledgeTemplate` | `SimulationKnowledgeArtifact` | représente au moins une `disease` d'OGMS ; au moins **2** états de santé ; au moins 1 transition ; les formes de cours uniquement des `disease course` ; les facteurs de risque uniquement des `RiskFactor` |
| `HealthState` | **`CouplingSource`** | représente une phase d'un `disease course` |
| `HealthStateTransition` | `SimulationKnowledgeArtifact` | exactement 1 état de départ, 1 état d'arrivée ; au moins 1 déterminant |
| `IndividualAttribute` | `SimulationKnowledgeArtifact` | - |
| `RiskFactor` | `SimulationKnowledgeArtifact` | - |

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
| `IndividualDeterminant` | `TransitionDeterminant` | peut lire des `IndividualAttribute` (`dependsOnAttribute`), sans y être obligé |
| `PopulationCoupledDeterminant` | `TransitionDeterminant` | dépend de l'effectif d'au moins 1 **`CouplingSource`** |

Les deux sortes sont **déclarées disjointes**.

**Un déterminant individuel peut ne lire aucun attribut** (correction 7, 15 octobre 2026). Il
exigeait au moins un `IndividualAttribute` ; or le taux de guérison γ du modèle SIR est
individuel et ne lit rien : il ne dépend ni des autres individus, ni de l'âge, ni du sexe. La
contrainte a été retirée ; `dependsOnAttribute` sert à décrire, sans entrer dans un axiome.

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

**`AcuteCourseDiseaseKnowledge` a été ajoutée.** OGMS découpe les
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
compartiment (3B), un état d'agent (3A), un flux (3B) et une transition d'agent (3A) en
héritent automatiquement. **La
couche 4 n'a donc pas besoin d'importer la couche 3** et une couche de paradigme future
héritera des ponts sans qu'on y touche.

> **PS.** Les trois ponts sont déclarés avec domaine et portée mais n'apparaissent dans
> **aucun individu** des neuf fichiers, ni dans aucun axiome de ce module : l'audit de 4-Core
> les signale comme propriétés jamais utilisées. Depuis le 15 octobre 2026,
> `representsStateTransition` entre dans les définitions du module 4-Checks
> (`StaticApproximationFlow`, `StaticApproximationAgentTransition`), que l'audit de 4-Core ne
> charge pas. **Le pont est correct et, hors de 4-Checks, il est vide.** C'est normal, il
> sert à décrire des modèles réels, ce qui vient après, mais ne l'écrivez pas comme un résultat
> acquis dans l'article sans joindre le jeu d'essai qui le montre. C'est le troisième test
> fonctionnel à écrire (M7).


### Les interventions

| Classe | Parent | Ce qu'elle impose |
|---|---|---|
| `Intervention` | `SimulationKnowledgeArtifact` | modifie au moins 1 déterminant |
| `PharmaceuticalIntervention` | `Intervention` | - |
| `Treatment`, `Vaccination` | `PharmaceuticalIntervention` | - |
| `NonPharmaceuticalIntervention` | `Intervention` | - |
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

Deux groupes de quatre classes mutuellement exclusives :

- `HealthState`, `HealthStateTransition`, `IndividualAttribute`, `TransitionDeterminant` ;
- `HealthState`, `HealthStateTransition`, `RiskFactor`, `TransitionDeterminant`.

Plus les trois paires : individuel ⊥ couplé, pharmaceutique ⊥ non pharmaceutique,
dépistage ⊥ diagnostic.

**Pourquoi deux groupes** (correction 6, 10 octobre 2026). Les cinq classes formaient un seul
groupe, ce qui interdisait à un attribut individuel d'être aussi un facteur de risque. Or l'âge
est les deux. `IndividualAttribute` et `RiskFactor` ne sont donc plus disjoints. C'est ce qui
ouvre à la question Q6 un chemin d'une transition vers ses facteurs de risque, par les
attributs que lit son déterminant ; Q6 reste notée `manque`, car ce chemin ne couvre que les
attributs déclarés aussi facteurs de risque.

### 19 alignements, 18 vers OSDi, 1 vers OGMS

**12 `exactMatch` :** `detects`, `hasEndAge`, `hasOnsetAge`, `hasSensitivity`, `hasSpecificity`,
`hasRefToDO`, `hasRefToICD`, `hasRefToSNOMED`, `DetectionIntervention`,
`DiagnosisIntervention`, `ScreeningIntervention`, `IndividualAttribute` → `osdi:Attribute`.

**7 `closeMatch` :** `DiseaseKnowledgeTemplate` → `osdi:Disease` ; `HealthState` →
`osdi:ClinicalProgressionElement` ; `HealthStateTransition` → `osdi:Pathway` ; `Intervention` →
`osdi:Intervention` ; `PharmaceuticalIntervention` → `osdi:TherapeuticIntervention` ;
`supersedesHealthState` → `osdi:supersedesClinicalProgression` ; `RiskFactor` →
`OGMS_0000030`.

**L'alignement retiré est le plus parlant de toute l'ontologie** (correction 5).
`TransitionDeterminant` était relié par `relatedMatch` à `osdi:hasRiskCharacterization` : une
**classe** à une **propriété**. Retiré le 10 octobre 2026, il est remplacé par une note de
l'éditeur (`obo:IAO_0000116`), ajoutée le 19 octobre : « Pas d'équivalent dans OSDi ». OSDi
n'a pas de classe pour ce qui gouverne une transition ; il rattache le risque à un élément de
progression clinique par une propriété dont la valeur est un paramètre. Ce que 4-Core nomme,
OSDi le laisse dans une propriété.

---

## Validation

### 1. Audit automatique

**Résultat au 19 octobre 2026 : 0 erreur, 8 avertissements.** 558 triplets. HermiT : aucune
classe insatisfiable.

Les huit avertissements signalent des propriétés déclarées sans axiome : `dependsOnAttribute`,
`detects`, `hasEndAge`, `hasOnsetAge`, `realisesDeterminant`, `representsHealthState`,
`representsStateTransition`, `supersedesHealthState`. `dependsOnAttribute` s'y est ajoutée
avec la correction 7, qui a retiré la seule contrainte où elle figurait.

**Trois d'entre elles sont les ponts de D14.** Elles ne sortent pas : elles ont besoin d'un jeu
d'essai, pas d'une suppression. `representsStateTransition` sert déjà dans 4-Checks, que cet
audit ne charge pas. Les cinq autres relèvent de la revue finale.

Pour reproduire, depuis la racine du dépôt : `bash tools/audit_tout.sh`, ou pour 4-Core seule :

```
python tools/audit_ontosim.py --focus src/ontology/layer4_core.ttl \
    --load src/ontology/layer1_foundational.ttl src/ontology/layer2_modsim.ttl src/ontology/layer4-ogms.ttl src/ontology/layer4_core.ttl \
    --ref tools/ref/ro.owl tools/ref/iao.owl tools/ref/bfo.owl tools/ref/ogms-edit.owl
```

### 2. Test de classification

`tests/test_forme_du_cours.ttl`, une grippe à cours aigu est classée
`AcuteCourseDiseaseKnowledge`, un diabète à cours chronique tombe dans
`ChronicCourseDiseaseKnowledge` et aucune des deux n'entre dans la classe de l'autre. Refait le
19 octobre 2026 avec HermiT.

Le même jour, trois autres cas, vérifiés à la main avec HermiT :

- une maladie dont une transition est gouvernée par un déterminant couplé est classée
  `CoupledDiseaseKnowledge` ;
- une maladie dont la seule transition est gouvernée par un déterminant individuel n'est
  **pas** classée `IndividualProgressionDiseaseKnowledge` : c'est la limite L1 ;
- avec les deux axiomes de fermeture (la liste des transitions de la maladie, la liste des
  déterminants de la transition), elle l'est.


### 3. Test à écrire

Un compartiment déclarant `representsHealthState` vers un état d'une
maladie couplée doit permettre de retrouver, par requête, que ce modèle représente cette
maladie. **C'est le test manquant**.

Le pont `representsStateTransition` a déjà été exercé à la main le 19 octobre 2026, par les
contrôles de 4-Checks (trois cas de taux, voir la fiche 3B). Il reste à écrire, dans `tests/`,
un fichier qui exerce les trois ponts.

### 4. OOPS! 

A FAIRE

Soumettre le fichier sur https://oops.linkeddata.es et sauvegarder le rapport. Défauts
probables : les mêmes qu'en couche 2, inverses non déclarés (P13) et espaces de noms
extérieurs (P40), avec la même réponse. Toutes les propriétés ont un domaine et une portée.

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
|- | Correction 5 : le `relatedMatch` de `TransitionDeterminant` vers une propriété d'OSDi est retiré et remplacé par une note de l'éditeur. |
|- | Correction 6 : disjonctions en deux groupes ; un attribut individuel peut aussi être un facteur de risque. |
|- | Correction 7 : un déterminant individuel peut ne lire aucun attribut. |
|- | La couche 4 compte maintenant cinq fichiers : 4-OGMS (import, D1), 4-Core, 4-Infectious, 4-Context, et 4-Checks, ajouté par la correction 9 (15 octobre 2026) pour relier la maladie aux modèles des couches 3A et 3B. |
| L1 | La détection négative du couplage demande des axiomes de fermeture. Découverte ici. |

---

## Versionnement

Le module est en 1.1 depuis octobre 2026. Depuis la 1.0, il a reçu `CouplingSource`,
`AcuteCourseDiseaseKnowledge` et les corrections 5, 6 et 7. Il est importé par 4-Infectious,
par 4-Checks et par l'ombrelle, qui ont suivi. Le numéro suit l'empilement entier, en un seul
geste : voir la fiche de la couche 2, *Versionnement*.

<br>

<p align="center">
  🦋<br>
  <i>Fais avec amour et pour l'Amour.</i>
</p>