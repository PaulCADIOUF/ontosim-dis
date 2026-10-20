# OntoSim-Dis — Couche 1 : fondations

**Fichier :** `src/ontology/layer1_foundational.ttl`
**IRI :** `https://w3id.org/ontosim-dis/layer1` — version `https://w3id.org/ontosim-dis/layer1/1.1`
**Importe :** rien. C'est la racine de l'empilement.
**Licence :** CC BY 4.0
**Statut :** version 1.1 (octobre 2026 : sept relations retirées et notes revues depuis la
1.0). Voir *Versionnement*.

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
leurs dépôts GitHub sont incomplets. Les bons fichiers sont déjà dans `tools/ref/` (voir
`tools/ref/LISEZMOI.md`). Cette couche n'emploie aucun terme d'OGMS, mais la remarque vaut
pour la vérification de 4-OGMS.

## Contenu : 23 termes importés

Aucun terme propre. 13 classes, 9 propriétés d'objet, 1 propriété d'annotation.
L'index des termes en compte 22 : il ne compte pas la propriété d'annotation.

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

### 9 propriétés d'objet

| IRI | Libellé | Domaine → Portée | Caractéristique | Utilisée par |
|---|---|---|---|---|
| `BFO_0000050` | part of | — | transitive | 4-Core : un désordre fait partie d'un organisme étendu |
| `BFO_0000054` | realized in | realizable entity → process | inverse de `realizes` | 4-Core : une maladie se réalise dans un cours de maladie |
| `BFO_0000055` | realizes | process → realizable entity | inverse de `realized in` | — |
| `IAO_0000136` | is about | information content entity → — | — | **4-Core : les 5 ponts** |
| `RO_0000057` | has participant | occurrent → continuant | — | parent de `has input` / `has output` |
| `RO_0002131` | overlaps | — | symétrique | parent de `part of` |
| `RO_0002233` | has input | process → — | — | **décision D2 en suspens** |
| `RO_0002234` | has output | — | — | **décision D2 en suspens** |
| `RO_0002323` | mereotopologically related to | — | — | parent d'`overlaps` |

**Sept relations retirées le 10 octobre 2026**, parce qu'aucun module ne les utilisait
(principe MIREOT : on n'importe que ce qui sert) : `characteristic of` (`RO_0000052`),
`has characteristic` (`RO_0000053`), `characteristic of part of` (`RO_0002314`),
`depends on` (`RO_0002502`), `has disposition` (`RO_0000091`), `participates in`
(`RO_0000056`), `located in` (`RO_0001025`). `located in` relie des entités matérielles :
4-Context a sa propre relation, `isSubRegionOf`. `participates in` portait la décision D4,
devenue sans objet (voir plus bas).

Les domaines et portées vides sont ceux que RO ne déclare pas. **On ne les complète pas** : en
ajouter serait s'écarter de la source et c'est précisément ce que la méthode MIREOT interdit
(décision M5).

### 1 propriété d'annotation

`IAO_0000116` — *editor note*. C'est elle qui porte les notes de travail par opposition à
`rdfs:comment` qui porte la définition publiée (décision D28). Six termes en portent une :
`entity`, `continuant`, `occurrent`, `information content entity`, `has input` et
`has output`.

> **PS.:** le fichier déclare cinq propriétés
> d'annotation supplémentaires — `dcterms:created`, `dcterms:creator`, `dcterms:license`,
> `dcterms:source` et `dce:description` — qui servent à l'en-tête de l'ontologie et ne sont pas
> des termes importés par MIREOT. Les 23 termes MIREOT sont ceux de l'espace de noms `obo:`.

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

**Résultat au 19 octobre 2026 : 0 erreur, 0 avertissement.** 131 triplets.
HermiT : aucune classe insatisfiable sur l'empilement complet.

**Pour reproduire,** depuis la racine du dépôt (installation : voir `tools/README.md`) :

```
bash tools/audit_tout.sh
```

ou, pour cette couche seule :

```
python tools/audit_ontosim.py --focus src/ontology/layer1_foundational.ttl \
    --load src/ontology/layer1_foundational.ttl \
    --ref tools/ref/ro.owl tools/ref/iao.owl tools/ref/bfo.owl
```

Les fichiers de référence sont déjà dans `tools/ref/` : rien à télécharger.

L'outil vérifie la forme comme les libellés, références, hiérarchies, caractéristiques, cohérence.
**Il ne vérifie pas le sens** : c'est le rôle du registre des décisions et un texte faux est
toujours invisible à une machine.

### 2. OOPS!

**Résultat sur la version 1.1** (octobre 2026). OOPS! a évalué le fichier complet, produit
par `tools/construire.sh` : aucun défaut critique. Pour cette couche, quatre défauts, tous prévus et voulus :

| Défaut OOPS! | Niveau | Termes concernés | Réponse |
|---|---|---|---|
| P11 domaine ou portée manquant | important | `part of`, `overlaps`, `mereotopologically related to`, `is about`, `has input`, `has output` | Conforme aux sources, qui ne les déclarent pas (décision M5). |
| P13 inverse non déclaré | mineur | les mêmes sauf `overlaps`, qui est symétrique, plus `has participant` | Principe MIREOT : on n'importe pas les inverses qu'aucune couche n'utilise. |
| P08 annotation manquante | mineur | `immaterial entity` | BFO 2.0 ne lui donne pas de définition, seulement une note ; la règle C1-16 interdit d'en inventer une. |
| P04 élément isolé | mineur | `entity` | C'est la racine de BFO : rien au-dessus d'elle. |

Le détournement d'espace de noms (P40), attendu avec MIREOT, n'a pas été signalé. Le rapport accompagne la documentation : lien « Evaluation » en tête de page.

### 3. Conformité MIREOT

Les 22 termes importés doivent correspondre à leur source officielle, libellé et parent direct.
C'est le contrôle [4] de l'audit : aucun écart au 19 octobre 2026.

---

## Versionnement

Le dépôt porte une version par état de l'empilement entier et non une étiquette par couche :
une adresse de version doit rester vraie et il est plus simple de garantir cela pour un
ensemble cohérent que pour dix fichiers numérotés séparément.

L'empilement est en 1.1 depuis octobre 2026, fichier ombrelle compris : `tools/version.py`
change le numéro dans tous les fichiers d'un seul geste. À la publication, l'étiquette Git
`v1.1` se posera pour tout l'ensemble, et la copie figée de la version ira sur le site, dans
un dossier à son numéro.

---

## Décisions

Le détail des décisions de cette couche, avec leurs raisons, est dans
`cahier_conception_couche1.md` (entrées C1-01 à C1-16).

| Code | Question | État |
|---|---|---|
| D1 | Où placer OGMS ? | **Tranchée** : module d'import à part, `layer4-ogms.ttl` |
| D2 | `has input` / `has output` : retirer, ou remplacer par `has specified input/output` d'OBI ? | **En suspens**, jusqu'à la conception de la recomposition |
| D4 | Un agent participe-t-il directement à la simulation ? | **Sans objet** : la couche 3A ne décrit que des catégories d'agents, et `participates in` a été retiré |

---


<br>

<p align="center">
  🦋<br>
  <i>Fais avec amour et pour l'Amour.</i>
</p>