# OntoSim-Dis — Couche 1 : fondations

**Fichier :** `src/ontology/layer1_foundational.ttl`
**IRI :** `https://w3id.org/ontosim-dis/layer1` — version `1.0` (`https://w3id.org/ontosim-dis/layer1/1.0`)
**Licence :** CC BY 4.0
**Statut :** version de travail 1.0, pas encore publiée. Les changements sont suivis par git ;
une fois la couche publiée, toute modification donnera une nouvelle version.

## Rôle

La couche 1 contient les concepts fondateurs, indépendants de tout domaine applicatif.
Elle fournit aux autres couches les catégories les plus générales (chose, processus,
information, disposition) et les relations qui les lient. Elle ne contient **aucun terme
médical** (voir C1-03 dans le cahier de conception).

## Sources et versions

| Source | Version de référence | Méthode |
|---|---|---|
| BFO (Basic Formal Ontology) | 2.0 | MIREOT |
| RO (Relation Ontology) | 2026-09-04 | MIREOT |
| IAO (Information Artifact Ontology) | 2026-03-30 | MIREOT |

Les fichiers officiels de ces versions sont dans `tools/ref/`. L'audit compare à eux le
libellé et le parent de chaque terme recopié.

**Règle des commentaires.** Ce que dit la source va dans `rdfs:comment` : c'est sa
définition officielle, et rien d'autre. Ce qu'OntoSim-Dis ajoute va dans une note de
l'éditeur (`editor note`, IAO_0000116). Voir C1-16.

## Contenu : 13 classes

| IRI | Libellé | Utilisé par | Sert de parent à |
|---|---|---|---|
| BFO_0000001 | entity | (racine) | continuant, occurrent |
| BFO_0000002 | continuant | (ancêtre) | independent, specifically et generically dependent continuant |
| BFO_0000003 | occurrent | (ancêtre) | process |
| BFO_0000004 | independent continuant | (ancêtre) | material entity, immaterial entity |
| BFO_0000015 | process | C2 (`SimulationExecution`), OGMS (`disease course`) | — |
| BFO_0000016 | disposition | OGMS (`disease`, `predisposition to disease of type X`) | — |
| BFO_0000017 | realizable entity | (ancêtre) | disposition |
| BFO_0000019 | quality | disjonction seulement (C1-11) | — |
| BFO_0000020 | specifically dependent continuant | (ancêtre) | realizable entity, quality |
| BFO_0000031 | generically dependent continuant | (ancêtre) | information content entity |
| BFO_0000040 | material entity | OGMS (`disorder`, `organism population`, `extended organism`) | — |
| BFO_0000141 | immaterial entity | disjonction seulement (C1-07) | — |
| IAO_0000030 | information content entity | C2 (`SimulationKnowledgeArtifact`, parent de tous les artefacts de connaissance) | — |

## Contenu : 9 propriétés d'objet

| IRI | Libellé | Utilisé par | Remarque |
|---|---|---|---|
| BFO_0000050 | part of | 4-Core : un désordre fait partie d'un organisme étendu | transitive |
| BFO_0000054 | realized in | 4-Core : une maladie se réalise dans un cours de maladie | inverse de realizes |
| BFO_0000055 | realizes | (inverse) | inverse de realized in |
| IAO_0000136 | is about | 4-Core : parent des ponts `representsDisease`, `representsHealthState`, `representsStateTransition`, `representsPhaseOf`, `realisesDeterminant` | pont information → réalité |
| RO_0000057 | has participant | (parent) | parent de has input / has output |
| RO_0002131 | overlaps | (parent) | symétrique ; parent de part of |
| RO_0002233 | has input | aucun module pour l'instant | **décision D2 en suspens** (C1-13) |
| RO_0002234 | has output | aucun module pour l'instant | **décision D2 en suspens** (C1-13) |
| RO_0002323 | mereotopologically related to | (parent) | parent de overlaps |

Sept relations de RO qu'aucun module n'utilisait ont été retirées en octobre 2026 : voir C1-06.

## Disjonctions

continuant ⊥ occurrent ; independent ⊥ specifically dependent ⊥ generically dependent
continuant ; material ⊥ immaterial entity ; realizable entity ⊥ quality.
Le rôle de chacune est expliqué dans le cahier de conception (C1-11).

---

## Validation

### 1. Audit automatique

**Résultat au 19 octobre 2026 :** 0 erreur, 0 avertissement. HermiT trouve la couche
cohérente, sans classe insatisfiable (131 triplets, 13 classes, 9 propriétés d'objet).

**Pour reproduire,** depuis la racine du dépôt (installation : voir `tools/README.md`) :

```
bash tools/audit_tout.sh
```

ou, pour la couche 1 seule :

```
python tools/audit_ontosim.py --focus src/ontology/layer1_foundational.ttl \
    --load src/ontology/layer1_foundational.ttl \
    --ref tools/ref/ro.owl tools/ref/iao.owl tools/ref/bfo.owl
```

L'outil vérifie la forme (libellés, références, hiérarchies, caractéristiques, cohérence).
**Il ne vérifie pas le sens** : c'est le rôle du cahier de conception.

### 2. OOPS! (à faire)

Soumettre `layer1_foundational.ttl` sur https://oops.linkeddata.es et sauvegarder le rapport
sous `oops_couche1_AAAA-MM-JJ`.

**Défauts probables, et réponse préparée.** Un pré-contrôle permet d'anticiper ce qu'OOPS!
risque de signaler. Pour une ontologie construite par MIREOT, la plupart sont attendus et se
justifient :

| Défaut OOPS! (code probable) | Termes concernés | Réponse |
|---|---|---|
| Annotations manquantes (P08) | `immaterial entity` | **Justifier** : BFO 2.0 ne lui donne pas de définition, seulement une note. |
| Domaine ou portée manquant (P11) | 6 propriétés : `part of`, `overlaps`, `mereotopologically related to`, `is about`, `has input`, `has output` | **Justifier** : conforme aux sources, qui ne les déclarent pas. En ajouter serait s'écarter de la source. |
| Inverse non déclaré (P13) | 6 propriétés, dont `part of`, `is about`, `has participant` | **Justifier** : principe MIREOT, on n'importe pas les inverses (`has part`, `participates in`...) qu'aucune couche n'utilise. |
| Détournement d'espace de noms (P40) | tous les termes `obo:` | **Justifier** : attendu avec MIREOT, qui recopie des termes dans leur espace de noms d'origine pour garantir l'interopérabilité. |

Les codes de défauts sont indicatifs : vérifiez-les dans le rapport réel, et consignez
chaque réponse dans le cahier de conception.

---

## Versionnement

La couche est suivie dans le dépôt, avec les autres modules. Quand elle sera publiée,
marquer sa version d'une étiquette :

```
git tag -a layer1-v1.0 -m "Couche 1, version 1.0"
git push --tags
```

---

## Décisions

| Code | Question | État |
|---|---|---|
| D1 | Où placer OGMS ? | **Tranchée** : dans un module d'import à part, `layer4-ogms.ttl`, chargé par 4-Core (C1-03) |
| D2 | `has input` / `has output` : retirer, ou remplacer par `has specified input/output` d'OBI ? | **En suspens**, jusqu'à la conception de la recomposition (C1-13) |
| D4 | Un `Agent` participe-t-il directement à la simulation ? | **Sans objet** : la couche 3A ne décrit que des catégories d'agents, et `participates in` a été retiré (C1-14) |
