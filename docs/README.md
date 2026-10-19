# Documents de conception

Ce dossier rassemble les documents qui expliquent OntoSim-Dis. Les fichiers de l'ontologie
sont dans `src/ontology/`, les outils dans `tools/`, les tests dans `tests/`.

## Par où commencer

| Document | À quoi il sert |
|---|---|
| `guide_ontologie.md` | Où se trouve quoi : les neuf fichiers, les pièges, le Quadruplet. À lire en premier. |
| `index_termes.md` | Tous les termes par ordre alphabétique, avec leur module et leur définition. Produit par `tools/index_termes.py` : ne pas le modifier à la main. |
| `questions_de_competence.md` | Les 30 questions auxquelles l'ontologie doit répondre, et l'état de chacune. |

## Les fiches, une par module

Chaque fiche donne le contenu du module, les raisons des choix, les résultats de l'audit et
des tests, et les décisions qui le touchent. **C'est la référence à jour.**

| Fiche | Module |
|---|---|
| `couche1.md` | `layer1_foundational.ttl` : termes repris de BFO, RO et IAO |
| `couche2.md` | `layer2_modsim.ttl` : modélisation et simulation |
| `couche3a.md` | `layer3a_mas.ttl` : modèles multi-agents |
| `couche3b.md` | `layer3b_equations.ttl` : modèles à compartiments |
| `couche4-core.md` | `layer4_core.ttl` : la maladie |
| `couche4-context.md` | `layer4-context.ttl` : le contexte |

Trois modules n'ont pas encore de fiche :

- `layer4-ogms.ttl`, décrit pour l'instant dans `specification_couche4_core.md` ;
- `layer4_infectious.ttl`, décrit dans le guide et l'index ;
- `layer4-checks.ttl`, décrit dans le guide, l'index et les fiches 3A et 3B.

## Registre et histoire

Ces documents gardent la trace de la construction. Ils ne décrivent pas toujours l'état
actuel : en cas d'écart, la fiche fait foi.

| Document | Ce qu'il garde |
|---|---|
| `cahier_conception_couche1.md` | Les décisions de la couche 1 (C1-01 à C1-16), avec leurs raisons et les choix écartés. |
| `specification_couche2_coeur.md` | Le plan de construction de la couche 2, avec les corrections signalées à leur place. |
| `specification_couche4_core.md` | Le plan de construction du module OGMS et de 4-Core, mis à jour le 19 octobre 2026. |

## Après une modification de l'ontologie

1. Lancer l'audit, à la racine du dépôt : `bash tools/audit_tout.sh`.
2. Régénérer l'index : `python tools/index_termes.py`.
3. Mettre à jour la fiche du module : chiffres, résultat de l'audit, décisions.
4. Enregistrer l'ontologie, l'index et la fiche dans le même commit.

<br>

<p align="center">
  🦋<br>
  <i>Fais avec amour et pour l'Amour.</i>
</p>
