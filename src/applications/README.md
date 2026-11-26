# Applications

La couche 5 d'OntoSim-Dis : un fichier par cas étudié. Chaque application décrit un modèle publié avec le vocabulaire des couches 1 à 4 : la maladie, le contexte, la structure du modèle et ses paramètres. Elle ne crée aucun terme. Chaque valeur reprise d'une publication porte sa source, avec `dcterms:source`.

| Fichier | Le cas | Source |
|---|---|---|
| `althaus-2014-ebola.ttl` | le modèle SEIR de l'épidémie d'Ebola de 2014, ajusté à la Guinée, à la Sierra Leone et au Libéria : trois modèles qui partagent la description de la maladie et la structure | Althaus (2014), *PLOS Currents Outbreaks*, doi:10.1371/currents.outbreaks.91afb5e0f279e7f29e7056095255b288 |
| `roques-2020-covid19.ttl` | le modèle SIRD du COVID-19 en France pendant le confinement du printemps 2020, ajusté aux tests positifs et aux décès à l'hôpital | Roques et al. (2020), *Frontiers in Medicine*, doi:10.3389/fmed.2020.00274 |
| `hunter-2018-measles.ttl` | le modèle multi-agents de la rougeole dans la ville irlandaise de Schull, construit sur des données ouvertes et comparé à l'épidémie de 2012 | Hunter et al. (2018), *PLOS ONE*, doi:10.1371/journal.pone.0208775 |

Dans Protégé :

1. *File → Open*, puis choisir l'application dans ce dossier.
2. *Reasoner → HermiT*, puis *Reasoner → Start reasoner*.
3. Regarder les types inférés, en jaune, dans l'onglet des individus. La fin de chaque fichier dit ce que HermiT doit trouver tout seul.

Le fichier `catalog-v001.xml` dit à Protégé de lire l'ontologie dans `src/ontology/`, au lieu de la chercher sur w3id.org. Il est produit par `tools/version.py`, qui met aussi à jour l'import de chaque application quand le numéro de l'ontologie change.

Chaque application est aussi vérifiée par `bash tools/audit_tout.sh`, avec toute l'ontologie.
