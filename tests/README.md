# Tests

Chaque test déclare le strict minimum et demande au raisonneur de classer. Les lignes `ATTENDU` de son en-tête disent ce que HermiT doit inférer tout seul.

| Fichier | Ce qu'il vérifie | Comment le lancer |
|---|---|---|
| `test_transmission_environnementale.ttl` | la schistosomiase est classée à médiation environnementale, la COVID-19 ne l'est pas | `tools/reason.py` (voir `tools/README.md`), ou Protégé |
| `test_forme_du_cours.ttl` | la grippe est classée à cours aigu, le diabète à cours chronique | Protégé |
| `test_changement_de_contexte.ttl` | dans le modèle d'Althaus pour la Guinée, le taux de transmission est classé à réestimer, la taille de la population à remplacer, le R0 à recalculer, et la durée d'incubation n'est classée dans aucune des trois | Protégé |
| `test_valeur_mesuree.ttl` | dans le modèle de Roques et al. (2020) pour la France, les décès à l'hôpital au départ, une valeur mesurée, sont classés à remplacer, le taux de décès, qui dépend aussi des hôpitaux, à réestimer, et le taux de guérison n'est classé dans aucune des trois | Protégé |

Dans Protégé :

1. *File → Open*, puis choisir le test dans ce dossier.
2. *Reasoner → HermiT*, puis *Reasoner → Start reasoner*.
3. Regarder les types inférés, en jaune, dans l'onglet des individus.

Le fichier `catalog-v001.xml` dit à Protégé de lire les couches dans `src/ontology/`, au lieu de les chercher sur w3id.org. Les tests peuvent donc rester dans ce dossier, contrairement à ce que dit encore leur en-tête.
