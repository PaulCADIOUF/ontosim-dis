# Fichiers de référence

`audit_ontosim.py` compare chaque terme importé par MIREOT à sa source officielle. Ces fichiers sont ces sources, dans les versions contre lesquelles la couche 1 a été validée (`docs/cahier_conception_couche1.md`).

| Fichier | Ontologie | Version | Source | Licence |
|---|---|---|---|---|
| `bfo.owl` | Basic Formal Ontology | 2.0 | https://github.com/BFO-ontology/BFO, fichier `releases/2.0/bfo.owl` | CC BY 3.0 |
| `ro.owl` | Relation Ontology | 2026-09-04 | https://github.com/oborel/obo-relations, fichier `ro.owl` | CC0 1.0 |
| `iao.owl` | Information Artifact Ontology | 2026-03-30 | https://github.com/information-artifact-ontology/IAO, fichier `iao.owl` | CC BY 4.0 |
| `ogms-edit.owl` | Ontology for General Medical Science | fichier d'édition, sans numéro de version | https://github.com/OGMS/ogms, fichier `src/ontology/ogms-edit.owl` | CC BY 4.0 |

Ces fichiers appartiennent à leurs auteurs ; ils sont copiés ici, sans modification, pour que l'audit fonctionne sans connexion.

`ogms-edit.owl` est en syntaxe fonctionnelle OWL, que rdflib ne lit pas : l'audit en extrait lui-même libellés et parents. Le fichier `ogms.owl` servi à la racine du dépôt OGMS ne convient pas : il ne contient qu'une seule classe OGMS.
