# Tests

Chaque test déclare le strict minimum et demande au raisonneur de classer. Les lignes `ATTENDU` de son en-tête disent ce que HermiT doit inférer tout seul.

| Fichier | Ce qu'il vérifie | Comment le lancer |
|---|---|---|
| `test_transmission_environnementale.ttl` | la schistosomiase est classée à médiation environnementale, la COVID-19 ne l'est pas | `tools/reason.py` (voir `tools/README.md`), ou Protégé |
| `test_forme_du_cours.ttl` | la grippe est classée à cours aigu, le diabète à cours chronique | Protégé |

Dans Protégé :

1. *File → Open*, puis choisir le test dans ce dossier.
2. *Reasoner → HermiT*, puis *Reasoner → Start reasoner*.
3. Regarder les types inférés, en jaune, dans l'onglet des individus.

Le fichier `catalog-v001.xml` dit à Protégé de lire les couches dans `src/ontology/`, au lieu de les chercher sur w3id.org. Les tests peuvent donc rester dans ce dossier, contrairement à ce que dit encore leur en-tête.
