# Outils de vérification

Toutes les commandes se lancent dans Git Bash, à la racine du dépôt.

## Installer une seule fois

- Python 3 et deux bibliothèques : `pip install rdflib owlready2`
- Java, dont a besoin le raisonneur HermiT qu'utilise owlready2 : https://adoptium.net (version LTS)

Sous Windows, la commande Python s'appelle souvent `python` ou `py`, plutôt que `python3`.

## `audit_ontosim.py` : contrôler un module

Contrôles effectués sur un module :

1. chaque entité a un libellé, une langue et un commentaire ; les métadonnées (date, version) sont du texte simple ;
2. aucune référence vers une entité jamais déclarée ;
3. aucune propriété déclarée sans être utilisée ;
4. chaque terme importé de BFO, RO, IAO ou OGMS a le libellé et le parent de sa source officielle (fichiers de `ref/`) ;
5. HermiT trouve l'ensemble cohérent, sans classe insatisfiable.

**Les 8 modules d'un coup :**

    bash tools/audit_tout.sh

Le script audite chaque module avec ceux qu'il importe, puis compte les modules qui ont au moins une erreur. Pour aller plus vite sans HermiT : `bash tools/audit_tout.sh --no-reasoner`.

**Un seul module**, par exemple la couche 2 :

    python tools/audit_ontosim.py --focus src/ontology/layer2_modsim.ttl --load src/ontology/layer1_foundational.ttl src/ontology/layer2_modsim.ttl --ref tools/ref/ro.owl tools/ref/iao.owl tools/ref/bfo.owl tools/ref/ogms-edit.owl

- `--focus` : le module audité ;
- `--load` : ce module et tous ceux qu'il importe ;
- `--ref` : les fichiers officiels de référence.

| Module | Modules à donner à `--load` |
|---|---|
| couche 1 | couche 1 |
| couche 2 | couches 1, 2 |
| couche 3A | couches 1, 2, 3A |
| couche 3B | couches 1, 2, 3B |
| OGMS | couche 1, OGMS |
| 4-Core | couches 1, 2, OGMS, 4-Core |
| 4-Infectious | couches 1, 2, OGMS, 4-Core, 4-Infectious |
| 4-Context | couches 1, 2, 4-Context |

## `reason.py` : le test de transmission environnementale

    python tools/reason.py src/ontology/layer1_foundational.ttl src/ontology/layer2_modsim.ttl src/ontology/layer4-ogms.ttl src/ontology/layer4_core.ttl src/ontology/layer4_infectious.ttl tests/test_transmission_environnementale.ttl

Il fusionne les fichiers, lance HermiT, puis vérifie trois classements : les cercaires sont un état de réservoir, la schistosomiase est classée à médiation environnementale, la COVID-19 ne l'est pas. Résultat attendu : `3 verifications passees, 0 echouees`.

Ces trois vérifications sont écrites dans le script : il ne sert qu'à ce test.

## `ref/` : les fichiers de référence

Voir `ref/LISEZMOI.md`.
