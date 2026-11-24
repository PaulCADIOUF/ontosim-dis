# OntoSim-Dis — Couche 4-Transfer : changer un modèle de contexte

**Fichier :** `src/ontology/layer4-transfer.ttl`
**IRI :** `https://w3id.org/ontosim-dis/layer4-transfer` — version `https://w3id.org/ontosim-dis/layer4-transfer/1.3`
**Importe :** `https://w3id.org/ontosim-dis/layer4-context/1.3`
**Licence :** CC BY 4.0
**Statut :** version 1.3. Module ajouté en novembre 2026, dans la version 1.2 ; la 1.3 lui
ajoute une cinquième origine, « mesurée ». Voir *Versionnement*.

## Rôle

4-Context dit **où et pour qui** un modèle a été construit. 4-Transfer dit **ce qu'il faut
refaire** quand on reprend ce modèle ailleurs. Il répond à la question Q19 :

> Q19 — *Quels paramètres d'un modèle doivent être réestimés si on change de contexte
> géographique ?*

Le principe : on déclare deux choses pour chaque paramètre, et le raisonneur conclut.

1. **De quoi sa valeur dépend** : une région, une population, un climat ou une infrastructure
   de santé.
2. **D'où vient sa valeur** : reprise de la littérature, supposée, mesurée dans le contexte,
   estimée sur des données ou calculée.

Selon ces deux déclarations, le paramètre se garde, se remplace, se recalcule ou se réestime.


## Contenu

**5 classes, dont 4 définies, 3 propriétés d'objet, 1 propriété de données, 5 individus.**
169 triplets. L'index des termes en compte 14.

### Les 3 propriétés d'objet

| Propriété | Domaine → Portée | Caractéristique |
|---|---|---|
| `dependsOnContextElement` | ModelParameter → GeographicRegion, Population, Climate ou HealthInfrastructure | — |
| `hasValueOrigin` | ModelParameter → ValueOrigin | **fonctionnelle** |
| `isDerivedFrom` | ModelParameter → ModelParameter | — |

**`dependsOnContextElement` ne s'écrit pas pour un paramètre propre à la maladie.** Une durée
d'incubation ne dépend pas du pays : on ne lui déclare aucune dépendance, et le raisonneur ne
la range dans aucune des classes ci-dessous.

**`hasValueOrigin` est fonctionnelle** : une valeur a une origine et une seule.

### La propriété de données

| Propriété | Domaine → Type | Rôle |
|---|---|---|
| `parameterExpression` | ModelParameter → `xsd:string` | la formule d'un paramètre calculé, par exemple `beta / gamma` |

### L'origine d'une valeur : une liste fermée

`ValueOrigin` est une sous-classe de `SimulationKnowledgeArtifact`. Elle a cinq individus,
déclarés tous différents, et aucun autre n'est possible.

| Individu | Sens |
|---|---|
| `FROM_LITERATURE` | valeur reprise d'une étude publiée |
| `ASSUMED` | valeur posée par hypothèse, sans mesure ni estimation |
| `MEASURED` | valeur relevée dans le contexte du modèle, par un comptage ou une mesure : une population recensée, des cas ou des décès déclarés |
| `ESTIMATED_FROM_DATA` | valeur obtenue en ajustant le modèle à des données observées |
| `DERIVED` | valeur calculée par une formule à partir d'autres paramètres |

### Les 4 classes définies

Personne ne range un paramètre dans ces classes à la main : c'est le raisonneur qui le fait.

| Classe | Définition | Ce que demande un changement de contexte |
|---|---|---|
| `ContextDependentParameter` | un paramètre qui dépend d'au moins un élément de contexte | — |
| `ParameterToReestimate` | dépend du contexte, et sa valeur a été estimée sur des données | l'estimer de nouveau, sur des données du nouveau contexte |
| `ParameterToReplace` | dépend du contexte, et sa valeur a été supposée, reprise de la littérature ou mesurée dans le contexte | prendre la valeur du nouveau contexte |
| `ParameterToRecalculate` | calculé à partir d'au moins un paramètre qui dépend du contexte | refaire le calcul, sans nouvelles données |

Les trois dernières sont des sous-classes de `ContextDependentParameter`. Un paramètre à
recalculer dépend donc lui aussi du contexte, par le paramètre dont il est tiré.

**Un paramètre qui n'est dans aucune de ces classes se garde tel quel.**


## Exemple : le modèle d'Althaus (2014) pour la Guinée

Modèle SEIR de l'épidémie d'Ebola de 2014 (Althaus, *PLOS Currents Outbreaks*,
doi:10.1371/currents.outbreaks.91afb5e0f279e7f29e7056095255b288).

| Paramètre | Valeur | Dépend de | Origine | Le raisonneur conclut |
|---|---|---|---|---|
| durée d'incubation | 5,3 jours | — | littérature | rien : se garde |
| durée de contagiosité | 5,61 jours | — | littérature | rien : se garde |
| taux de transmission β | 0,27 | la Guinée | estimé | à réestimer |
| taux de létalité f | 0,74 | la Guinée | estimé | à réestimer |
| décroissance k | 0,0023 | la Guinée | estimé | à réestimer |
| taille de la population N | 1 000 000 | la population de Guinée | supposé | à remplacer |
| R0 = β / γ | 1,51 | — (tiré de β) | calculé | à recalculer |

Pour reprendre ce modèle dans un autre pays : deux paramètres se gardent, un se remplace,
trois demandent des données du nouveau pays, et le R0 se recalcule une fois β réestimé.

---

## Validation

### 1. Audit automatique

**Résultat au 24 novembre 2026, en 1.3 : 0 erreur, 0 avertissement.** 169 triplets. HermiT : aucune
classe insatisfiable.

Pour reproduire, depuis la racine du dépôt : `bash tools/audit_tout.sh`, ou pour 4-Transfer
seule :

```
python tools/audit_ontosim.py --focus src/ontology/layer4-transfer.ttl \
    --load src/ontology/layer1_foundational.ttl src/ontology/layer2_modsim.ttl src/ontology/layer4-context.ttl src/ontology/layer4-transfer.ttl \
    --ref tools/ref/ro.owl tools/ref/iao.owl tools/ref/bfo.owl tools/ref/ogms-edit.owl
```

### 2. Tests

`tests/test_changement_de_contexte.ttl` reprend l'exemple ci-dessus. Vérifié le 17 novembre
2026 avec HermiT dans Protégé : le taux de transmission est classé à réestimer, la taille de
la population à remplacer, le R0 à recalculer, et la durée d'incubation n'est classée dans
aucune des trois.

`tests/test_valeur_mesuree.ttl` vérifie la cinquième origine, avec des valeurs du modèle de
Roques et al. (2020) pour la France. Vérifié le 24 novembre 2026 avec HermiT dans Protégé : les
décès à l'hôpital au 31 mars 2020, une valeur mesurée, sont classés à remplacer ; le taux de
décès, qui dépend du pays et de ses hôpitaux, à réestimer ; le taux de guérison n'est classé dans
aucune des trois.

### 3. OOPS!

**Résultat sur la version 1.2** (novembre 2026). OOPS! a évalué le fichier complet, produit
par `tools/construire.sh` : aucun défaut critique, et aucun défaut nouveau par rapport à la
1.1. Pour ce module, un seul défaut, mineur : P13, inverse non déclaré, pour les 3 propriétés
d'objet, avec la même réponse qu'en couche 2. Le rapport accompagne la documentation : lien
« Evaluation » en tête de page.

---

## Limites

- **Si la dépendance n'est pas déclarée, le raisonneur ne conclut rien.** Un paramètre sans
  `dependsOnContextElement` est traité comme un paramètre qui se garde, même si on a
  seulement oublié de la déclarer.
- Le module dit **quoi** refaire, pas **comment**. Il ne donne ni la nouvelle valeur ni la
  méthode d'estimation.

---

## Décisions consignées

| Code | Décision |
|---|---|
| — | Un module à part de 4-Context : 4-Context décrit un contexte, 4-Transfer dit ce que coûte un changement de contexte. |
| — | La dépendance se déclare paramètre par paramètre, vers un élément précis du contexte, pas vers le contexte entier. |
| — | L'origine d'une valeur est une liste fermée de cinq individus. |
| — | Les classes de paramètres sont définies : c'est le raisonneur qui classe, pas le modélisateur. |
| — | Un paramètre à recalculer est une sorte de paramètre dépendant du contexte. |
| — | Une cinquième origine, « mesurée » : une valeur relevée dans le contexte du modèle se remplace, comme une valeur supposée ou reprise (24 novembre 2026, version 1.3). |

---

## Versionnement

Le numéro de version suit l'empilement entier, pas ce fichier seul. L'ajout de ce module a fait
passer l'ensemble de 1.1 à 1.2, en un seul geste ; l'ajout de l'origine « mesurée » l'a fait
passer en 1.3. Voir la fiche de la couche 2,
*Versionnement*.
