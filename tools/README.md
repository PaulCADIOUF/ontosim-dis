# Outils de vérification

Toutes les commandes se lancent dans Git Bash, à la racine du dépôt.

## Installer une seule fois

- Python 3 et deux bibliothèques : `pip install rdflib owlready2`
- Java, dont a besoin le raisonneur HermiT qu'utilise owlready2 : https://adoptium.net (version LTS)

Sous Windows, la commande Python s'appelle souvent `python` ou `py`, plutôt que `python3`.

Pour construire la documentation seulement (`construire.sh`), deux outils Java, à télécharger une fois dans `tools/lib/`, que git ignore :

    mkdir -p tools/lib
    curl -L -o tools/lib/robot.jar https://github.com/ontodev/robot/releases/download/v1.9.11/robot.jar
    curl -L -o tools/lib/widoco.jar https://github.com/dgarijo/Widoco/releases/download/v1.4.25/widoco-1.4.25-jar-with-dependencies_JDK-11.jar

ROBOT réunit les modules en un seul fichier ; WIDOCO écrit la documentation. Tous deux demandent Java 11 ou plus récent. Si `java -version` affiche une version plus ancienne (1.8 par exemple), installe Java 21 à côté, depuis https://adoptium.net ou avec `winget install EclipseAdoptium.Temurin.21.JDK` dans PowerShell : `construire.sh` la trouve seul, dans `JAVA_HOME` ou dans `C:\Program Files`, et affiche celle qu'il utilise. Pour en imposer une : `JAVA="/chemin/vers/java" bash tools/construire.sh`.

## `audit_ontosim.py` : contrôler un module

Contrôles effectués sur un module :

1. chaque entité a un libellé, une langue et un commentaire ; les métadonnées (date, version) sont du texte simple ;
2. aucune référence vers une entité jamais déclarée ;
3. aucune propriété déclarée sans être utilisée ;
4. chaque terme importé de BFO, RO, IAO ou OGMS a le libellé et le parent de sa source officielle (fichiers de `ref/`) ;
5. HermiT trouve l'ensemble cohérent, sans classe insatisfiable.

**Les 9 modules et l'ombrelle d'un coup :**

    bash tools/audit_tout.sh

Le script audite chaque module avec ceux qu'il importe, puis l'ombrelle avec les 9 modules, et compte les fichiers qui ont au moins une erreur. Pour aller plus vite sans HermiT : `bash tools/audit_tout.sh --no-reasoner`.

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
| 4-Checks | couches 1, 2, 3A, 3B, OGMS, 4-Core, 4-Checks |
| ombrelle | l'ombrelle et les 9 modules : HermiT vérifie alors toute l'ontologie |

## `reason.py` : le test de transmission environnementale

    python tools/reason.py src/ontology/layer1_foundational.ttl src/ontology/layer2_modsim.ttl src/ontology/layer4-ogms.ttl src/ontology/layer4_core.ttl src/ontology/layer4_infectious.ttl tests/test_transmission_environnementale.ttl

Il fusionne les fichiers, lance HermiT, puis vérifie trois classements : les cercaires sont un état de réservoir, la schistosomiase est classée à médiation environnementale, la COVID-19 ne l'est pas. Résultat attendu : `3 verifications passees, 0 echouees`.

Ces trois vérifications sont écrites dans le script : il ne sert qu'à ce test.
<!--
## `version.py` : changer le numéro de version de tout l'empilement

    python tools/version.py                  état : le numéro de chaque fichier, et cinq contrôles
    python tools/version.py 1.1              simulation : ce qui changerait, sans rien écrire
    python tools/version.py 1.1 --appliquer  écrit les changements

Un seul numéro pour tout : les neuf modules et l'ombrelle changent ensemble, et s'importent entre eux à ce numéro. Le script change l'IRI de version, le numéro et les imports dans chaque fichier de `src/ontology`, les imports des tests, et réécrit les deux catalogues. Avant d'écrire un fichier, il vérifie avec rdflib que seul l'en-tête change.

À lancer quand on prépare une nouvelle version, puis relire avec `git diff`. Une version publiée ne change plus : une correction prend un nouveau numéro.

## `construire.sh` : le fichier complet et la documentation

    bash tools/construire.sh

Trois étapes, en une quinzaine de secondes :

1. ROBOT suit les imports de `src/ontology/ontosim-dis.ttl` grâce au catalogue et réunit les neuf modules dans `build/ontosim-dis-full.ttl`, sans `owl:imports`, avec les métadonnées de l'ombrelle. C'est ce fichier que recevront les applications.
2. WIDOCO écrit la documentation de ce fichier dans `build/site/latest/` : `index-en.html` et `index-fr.html`, la visualisation WebVOWL, l'ontologie en Turtle, RDF/XML (`ontology.owl`), N-Triples et JSON-LD, et l'évaluation OOPS! si le service répond.
3. Le script copie `latest/` dans un dossier au numéro de la version, met le fichier de chaque module dans `build/site/<module>/latest/` et `build/site/<module>/<numéro>/`, et écrit la page d'accueil `build/site/index.html`.

Le dossier `build/` est effacé et refait à chaque lancement. Pour regarder la documentation comme sur le web :

    cd build/site && python -m http.server 8000

puis ouvrir http://localhost:8000/latest/index-fr.html, et Ctrl+C pour arrêter.

Si OOPS! ne répond pas, la documentation se construit quand même, sans évaluation : relancer plus tard, ou soumettre `build/ontosim-dis-full.ttl` sur https://oops.linkeddata.es.

## `index_termes.py` : régénérer l'index des termes

    python tools/index_termes.py

Il relit les fichiers de `src/ontology/` et réécrit `docs/index_termes.md` : chaque terme, avec son module, sa nature et sa définition française. À lancer après chaque modification de l'ontologie, puis enregistrer l'index dans le même commit. Un nouveau fichier `.ttl` est pris en compte sans rien changer au script ; pour lui donner un nom court dans l'index, l'ajouter à la liste `MODULES`, en tête du script.

Résultat au 19 octobre 2026 : 325 termes.

## `accents.py` : rétablir les accents, outil d'une seule fois

    python tools/accents.py              simulation : écrit accents_rapport.txt, ne modifie rien
    python tools/accents.py --appliquer  corrige les fichiers de src/ontology

Il a servi le 15 octobre 2026 (correction 11), pour remettre les accents dans les textes français de l'ontologie. Il ne touche que les textes marqués `@fr` et vérifie, avant d'écrire, que seuls ces textes changent.

Son dictionnaire ne connaît que les mots des textes de cette date : **un texte écrit plus tard s'accentue à la main.** Si on le relance, lire d'abord `accents_rapport.txt` (ignoré par git), puis seulement appliquer.
-->
## `ref/` : les fichiers de référence

Voir `ref/LISEZMOI.md`.
