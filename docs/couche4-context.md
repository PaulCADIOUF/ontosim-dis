# OntoSim-Dis — Couche 4-Context : population, territoire, climat, infrastructure

**Fichier :** `src/ontology/layer4-context.ttl`
**IRI :** `https://w3id.org/ontosim-dis/layer4-context` — version `https://w3id.org/ontosim-dis/layer4-context/1.1`
**Importe :** `https://w3id.org/ontosim-dis/layer2/1.1`
**Licence :** CC BY 4.0
**Statut :** version 1.1. Aucun axiome n'a changé depuis la 1.0 ; seuls l'en-tête et des
textes ont été revus (octobre 2026 : guillemets d'en-tête corrigés, accents rétablis). Voir
*Versionnement*.

## Rôle

4-Context porte le composant **CK** du Quadruplet : **où et pour qui** le modèle a été
construit. Population, territoire, climat, infrastructure de santé.


## Contenu

**18 classes, 7 propriétés d'objet, 9 propriétés de données, 0 classe définie, 5 restrictions,
3 groupes de disjonctions, 2 alignements.** 250 triplets. L'index des termes en compte 34.

### La racine et son pont vers la couche 2

| Classe | Parent | Ce qu'elle impose |
|---|---|---|
| `ContextKnowledge` | `SimulationKnowledgeArtifact` | au moins 1 région géographique ; au moins 1 population ; climat uniquement `Climate` ; infrastructure uniquement `HealthInfrastructure` |

Le pont est `hasContextKnowledge`, de domaine **`SimulationModel`** (couche 2) et de portée
`ContextKnowledge`. Même principe que les ponts de D14 : le domaine est en couche 2, donc tout
modèle qu'il soit multi-agents, compartimental ou d'un paradigme futur peut déclarer son contexte sans
que cette couche connaisse les paradigmes.

### Les quatre familles

| Famille | Classes | Disjonction |
|---|---|---|
| Territoire | `GeographicRegion` ; `Country`, `AdministrativeRegion`, `District`, `City` | les quatre sortes s'excluent |
| Population | `Population` ; `UrbanPopulation`, `RuralPopulation`, `MixedPopulation` | les trois s'excluent |
| Climat | `Climate` ; `TropicalClimate`, `AridClimate`, `TemperateClimate` | les trois s'excluent |
| Infrastructure | `HealthInfrastructure` ; `Hospital`, `HealthCentre`, `VaccinationCentre` | — |

`Population` impose d'être située dans au moins une région : une population sans territoire ne
dit rien d'un contexte.

`AdministrativeRegion` correspond aux quatorze régions du Sénégal — la granularité à laquelle
les données sanitaires y sont produites.

### 7 propriétés d'objet

| Propriété | Domaine → Portée | Caractéristique |
|---|---|---|
| `hasContextKnowledge` | **`SimulationModel`** → ContextKnowledge | le pont |
| `hasGeographicRegion` | ContextKnowledge → GeographicRegion | — |
| `hasPopulation` | ContextKnowledge → Population | — |
| `hasClimate` | ContextKnowledge → Climate | — |
| `hasHealthInfrastructure` | ContextKnowledge → HealthInfrastructure | — |
| `isLocatedInRegion` | Population → GeographicRegion | — |
| `isSubRegionOf` | GeographicRegion → GeographicRegion | **transitive** |

**`isSubRegionOf` est transitive et c'est utile** : un district dans une région dans un pays
est dans ce pays, sans qu'on l'écrive.



### 9 propriétés de données

| Propriété | Sur | Type |
|---|---|---|
| `regionName`, `numberOfZones` | GeographicRegion | chaîne, entier |
| `populationSize`, `populationDensity`, `medianAge`, `averageHouseholdSize` | Population | entier, double, double, double |
| `avgTemperature`, `avgHumidity` | Climate | double |
| `hospitalCapacity` | HealthInfrastructure | entier |

`averageHouseholdSize` gouverne l'intensité des contacts domestiques ; `avgTemperature` et
`avgHumidity` sont déterminantes pour les maladies à vecteur et à transmission hydrique, où
elles gouvernent le cycle de vie du vecteur ou de l'hôte intermédiaire.

### 2 alignements

| OntoSim-Dis | Cible | Type |
|---|---|---|
| `Population` | `OGMS_0000084` *organism population* | relatedMatch |
| `Population` | `osdi:Population` | relatedMatch |

**Deux `relatedMatch` et rien de plus fort et c'est exact.** `OGMS_0000084` est un **agrégat
matériel** d'organismes ; `osdi:Population` est une cohorte clinique ; notre `Population` est la
**description** d'une population située. Les trois ne sont pas la même chose et un
`closeMatch` serait une surpromesse.

---

## Le seul module sans classe définie

4-Context est le seul des sept modules de contenu (tous sauf la couche 1 et le module OGMS, qui
importent des termes) à n'avoir **aucune classe définie**. Les autres en ont de 2 à 8. Ce n'est pas un défaut en soi : décrire un contexte est un travail de
vocabulaire et pas de classification.

**Mais c'est une occasion manquée et elle a un nom : la question Q19.**

> Q19 — *Quels paramètres d'un modèle doivent être réestimés si on change de contexte
> géographique ?*

**Cette question n'est pas répondable aujourd'hui.** Vérifié de nouveau le 19 octobre 2026 dans
les neuf fichiers :
**aucune propriété ne relie un `ModelParameter` à l'élément de contexte dont sa valeur dépend.**
On peut dire qu'un modèle suppose un climat tropical mais on ne peut pas dire que *tel paramètre* a
été estimé sous ce climat et devra être réestimé ailleurs.

Or Q19 est au cœur de notre thèse : réutiliser un modèle ailleurs que là où il a été construit.
Sans ce lien, l'ontologie décrit le contexte mais ne sait pas dire ce que changer de contexte
coûte. Q19 est notée `manque` dans `questions_de_competence.md`.

---

## Validation

### 1. Audit automatique

**Résultat au 19 octobre 2026 : 0 erreur, 2 avertissements.** 250 triplets. HermiT : aucune
classe insatisfiable. Les deux erreurs du 8 octobre (les guillemets d'en-tête) ont été
corrigées.

Les deux avertissements signalent `hasContextKnowledge` et `isSubRegionOf` comme déclarées sans
apparaître dans un axiome. **`hasContextKnowledge` est le pont de cette couche** : comme les
trois ponts de D14 en 4-Core, il est correct et vide. Il a besoin d'un jeu d'essai, pas d'une
suppression.

Pour reproduire, depuis la racine du dépôt : `bash tools/audit_tout.sh`, ou pour 4-Context
seule :

```
python tools/audit_ontosim.py --focus src/ontology/layer4-context.ttl \
    --load src/ontology/layer1_foundational.ttl src/ontology/layer2_modsim.ttl src/ontology/layer4-context.ttl \
    --ref tools/ref/ro.owl tools/ref/iao.owl tools/ref/bfo.owl tools/ref/ogms-edit.owl
```


### 2. Test à écrire

Un modèle déclarant une `ContextKnowledge` avec un climat tropical et une densité donnée doit
pouvoir être retrouvé par la requête Q18 — *quels modèles ont été construits pour un contexte
comparable à celui du Sénégal ?*

### 3. OOPS!

**Résultat sur la version 1.1** (octobre 2026). OOPS! a évalué le fichier complet, produit
par `tools/construire.sh` : aucun défaut critique. Pour cette couche, un seul défaut, mineur : P13, inverse non déclaré,
pour les 7 propriétés d'objet, avec la même réponse qu'en couche 2. Le rapport accompagne la documentation : lien « Evaluation » en tête de page.

---

## Décisions consignées

| Code | Décision |
|---|---|
| D16 | 4-Context porte le composant CK : population, région, climat, infrastructure. |
| — | `RO:located in` n'est pas réutilisée : elle relie des entités matérielles, nos régions sont des descriptions. |
| — | `isSubRegionOf` transitive. |
| — | Les deux alignements de `Population` sont des `relatedMatch` et pas plus fort : les trois concepts ne sont pas la même chose. |
| — | `Population` ne faisait **pas** doublon avec la couche 2 : la couche 2 ne la contient pas. Seul `DiseaseParameterSet` était un doublon. Erreur de diagnostic initiale, corrigée. |

---

## Versionnement

Le numéro de version suit l'empilement entier, pas ce fichier seul. Même sans changement
d'axiome, la couche est passée en 1.1 avec les autres, en un seul geste, et son import de la
couche 2 a suivi. Voir la fiche de la couche 2, *Versionnement*.

<br>

<p align="center">
  🦋<br>
  <i>Fais avec amour et pour l'Amour.</i>
</p>