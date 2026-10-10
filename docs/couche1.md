# OntoSim-Dis — Couche 1 : fondations

**Fichier :** `src/ontology/layer1_foundational.ttl`
**IRI :** `https://w3id.org/ontosim-dis/layer1` — version `https://w3id.org/ontosim-dis/layer1/1.0`
**Importe :** rien. C'est la racine de l'empilement.
**Licence :** CC BY 4.0
**Statut :** fermée à la version 1.0. Toute modification donne une nouvelle version.

> **Corrigé le 9 octobre 2026.** La version précédente de cette fiche annonçait l'IRI
> `http://www.ontosim-dis.org/ontology/layer1`, qui est l'adresse intermédiaire d'avant la
> migration vers w3id. Le fichier n'a jamais porté cette adresse depuis la fermeture en 1.0.

## Rôle

La couche 1 contient les concepts fondateurs, indépendants de tout domaine applicatif. Elle
fournit aux autres couches les catégories les plus générales — chose, processus, information,
disposition — et les relations qui les lient. Elle ne contient **aucun terme médical** : c'est
la raison d'être du module d'import OGMS séparé (décision D1).

## Sources et versions

| Source | Version de référence | Méthode |
|---|---|---|
| BFO (Basic Formal Ontology) | 2.0 | MIREOT |
| RO (Relation Ontology) | 2026-09-04 | MIREOT |
| IAO (Information Artifact Ontology) | 2026-03-30 | MIREOT |

**Attention sur les fichiers de référence.** Les `bfo.owl` et `ogms.owl` servis à la racine de
leurs dépôts GitHub sont incomplets. Les bons chemins sont indiqués plus bas. Cette couche
n'emploie aucun terme d'OGMS, mais la remarque vaut pour la vérification de 4-OGMS.

## Contenu : 30 termes importés

Aucun terme propre. 13 classes, 16 propriétés d'objet, 1 propriété d'annotation.

### 13 classes

| IRI | Libellé | Parent | Utilisée par |
|---|---|---|---|
| `BFO_0000001` | entity | (racine) | ancêtre de tout |
| `BFO_0000002` | continuant | entity | ancêtre |
| `BFO_0000003` | occurrent | entity | ancêtre |
| `BFO_0000004` | independent continuant | continuant | ancêtre |
| `BFO_0000015` | process | occurrent | C2 (`SimulationExecution`), 4-OGMS (`disease course`) |
| `BFO_0000016` | disposition | realizable entity | 4-OGMS (`disease`, `predisposition`) |
| `BFO_0000017` | realizable entity | specifically dependent continuant | ancêtre de disposition |
| `BFO_0000019` | quality | specifically dependent continuant | disjonction seulement |
| `BFO_0000020` | specifically dependent continuant | continuant | ancêtre |
| `BFO_0000031` | generically dependent continuant | continuant | ancêtre d'information content entity |
| `BFO_0000040` | material entity | independent continuant | 4-OGMS (`disorder`, `extended organism`, `organism population`) |
| `BFO_0000141` | immaterial entity | independent continuant | disjonction seulement |
| `IAO_0000030` | information content entity | generically dependent continuant | C2 (`SimulationKnowledgeArtifact`) |

### 16 propriétés d'objet

| IRI | Libellé | Domaine → Portée | Caractéristique | Utilisée par |
|---|---|---|---|---|
| `BFO_0000050` | part of | — | transitive | sous-propriété d'`overlaps` |
| `BFO_0000054` | realized in | realizable entity → process | inverse de `realizes` | — |
| `BFO_0000055` | realizes | process → realizable entity | inverse de `realized in` | — |
| `IAO_0000136` | is about | information content entity → — | — | **4-Core : les 5 ponts** |
| `RO_0000052` | characteristic of | — | fonctionnelle, inverse de `has characteristic` | — |
| `RO_0000053` | has characteristic | — → specifically dependent continuant | inverse-fonctionnelle | parent de `has disposition` |
| `RO_0000056` | participates in | continuant → occurrent | inverse de `has participant` | **décision D4 en suspens** |
| `RO_0000057` | has participant | occurrent → continuant | — | parent de `has input` / `has output` |
| `RO_0000091` | has disposition | independent continuant → disposition | — | anticipé pour la couche 4 |
| `RO_0001025` | located in | independent continuant → independent continuant | transitive | — |
| `RO_0002131` | overlaps | — | symétrique | parent de `part of` |
| `RO_0002233` | has input | process → — | — | **décision D2 en suspens** |
| `RO_0002234` | has output | — | — | **décision D2 en suspens** |
| `RO_0002314` | characteristic of part of | — | — | parent de `characteristic of` |
| `RO_0002323` | mereotopologically related to | — | — | parent d'`overlaps` |
| `RO_0002502` | depends on | — | — | parent de `characteristic of part of` |

Les domaines et portées vides sont ceux que RO ne déclare pas. **On ne les complète pas** : en
ajouter serait s'écarter de la source et c'est précisément ce que la méthode MIREOT interdit
(décision M5).

### 1 propriété d'annotation

`IAO_0000116` — *editor note*. C'est elle qui porte les notes de travail par opposition à
`rdfs:comment` qui porte la définition publiée (décision D28). Quatre notes d'éditeur existent
dans cette couche.

> **PS.:** le fichier déclare cinq propriétés
> d'annotation supplémentaires — `dcterms:created`, `dcterms:creator`, `dcterms:license`,
> `dcterms:source` et `dce:description` — qui servent à l'en-tête de l'ontologie et ne sont pas
> des termes importés par MIREOT. Les 30 termes MIREOT sont ceux de l'espace de noms `obo:`.

## Les six disjonctions

| Disjonction | Erreur de catégorie qu'elle attrape |
|---|---|
| continuant ⊥ occurrent | déclarer qu'un modèle est un processus |
| independent ⊥ specifically dependent continuant | ranger un paramètre sous une chose matérielle |
| independent ⊥ generically dependent continuant | ranger une information sous une chose |
| specifically ⊥ generically dependent continuant | confondre une qualité et une information |
| realizable entity ⊥ quality | traiter une disposition comme une qualité mesurée |
| material ⊥ immaterial entity | — |

**Ces disjonctions ont déjà servi.** C'est celle entre `independent continuant` et les
dépendants qui a révélé que `Researcher` et `Author` étaient rangés sous « artefact
d'information » alors qu'un chercheur est une personne (décision D5) : en déclarant un
chercheur matériel, HermiT rend la classe insatisfiable. Un garde-fou qui n'a jamais rien
attrapé n'a pas fait la preuve qu'il fonctionne.


---

## Validation

### 1. Audit automatique

**Résultat au 2026-10-08 : 0 erreur, 0 avertissement.** Audit relancé avec l'outil corrigé.
HermiT : aucune classe insatisfiable sur l'empilement complet.


**Pour reproduire :**

```
pip install rdflib owlready2          # et Java, pour HermiT
python3 tools/audit_ontosim.py --focus layer1_foundational.ttl \
    --load layer1_foundational.ttl \
    --ref tools/refs/ro.owl tools/refs/iao.owl tools/refs/bfo.owl
```

Fichiers de référence à télécharger une fois dans `tools/refs/` :

```
curl -LO https://raw.githubusercontent.com/oborel/obo-relations/master/ro.owl
curl -LO https://raw.githubusercontent.com/information-artifact-ontology/IAO/master/iao.owl
curl -LO https://raw.githubusercontent.com/BFO-ontology/BFO/master/releases/2.0/bfo.owl
```

L'outil vérifie la forme comme les libellés, références, hiérarchies, caractéristiques, cohérence.
**Il ne vérifie pas le sens** : c'est le rôle du registre des décisions et un texte faux est
toujours invisible à une machine.

### 2. OOPS!

A FAIRE!!!

### 3. Conformité MIREOT

Les 30 termes doivent correspondre à leur source officielle, libellé et parent direct.

---

## Versionnement

Le dépôt porte une version par état de l'empilement entier et non une étiquette par couche :
une adresse de version doit rester vraie et il est plus simple de garantir cela pour un
ensemble cohérent que pour huit fichiers numérotés séparément.

```
git add src/ontology/layer1_foundational.ttl docs/couche1.md
git commit -m "couche1 : ferme la v1.0, fondations BFO/RO/IAO par MIREOT"
```

L'étiquette `v1.0` et la copie figée dans `releases/1.0/` se posent pour les huit fichiers
ensemble.

---


<br>

<p align="center">
  🦋<br>
  <i>Fais avec amour et pour l'Amour.</i>
</p>