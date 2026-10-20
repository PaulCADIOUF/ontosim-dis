# OntoSim-Dis — Couche 3B : paradigme compartimental

**Fichier :** `src/ontology/layer3b_equations.ttl`
**IRI :** `https://w3id.org/ontosim-dis/layer3b` — version `https://w3id.org/ontosim-dis/layer3b/1.1`
**Importe :** `https://w3id.org/ontosim-dis/layer2/1.1`
**Licence :** CC BY 4.0
**Statut :** version 1.1. Aucun axiome n'a changé depuis la 1.0 ; seuls l'en-tête et des
commentaires ont été revus (octobre 2026 : guillemets d'en-tête corrigés, sens de
`ConstantRate` précisé, accents rétablis). Voir *Versionnement*.

## Rôle

La couche 3B dit **comment** un modèle compartimental est construit : la population est divisée
en compartiments et des flux gouvernés par des taux font passer les individus de l'un à
l'autre.

**Elle ne dit jamais quelle maladie le modèle représente** (décision D9). `EpidemiologicalParameter`,
`TransmissionRate`, `RecoveryRate` et les modèles nommés SIR et SEIR ont quitté cette couche :
les premiers sont des connaissances sur la maladie (couche 4), les seconds combinent un
paradigme et des états de santé, donc relèvent de la couche 5 (décision D12).

**Conséquence chiffrée :** 3B est passée de 33 à 9 classes.

## Contenu

**9 classes, 7 propriétés d'objet, 5 propriétés de données, 2 classes définies, 8 restrictions,
1 disjonction, 0 alignement.** 181 triplets. L'index des termes en compte 21.

### Le modèle et ses pièces

| Classe | Parent (couche 2) | Ce qu'elle impose |
|---|---|---|
| `CompartmentalModel` | `SimulationModel` | au moins **2** compartiments ; au moins 1 flux |
| `Compartment` | `StateComponent` | — |
| `TransitionFlow` | `TransitionComponent` | exactement 1 taux ; hérite : exactement 1 compartiment de départ et 1 d'arrivée |
| `RateSpecification` | `ModelParameter` | — |
| `DifferentialEquation` | `ModelComponent` | au moins 1 flux ; gouverne exactement 1 compartiment |

**Le « au moins 2 compartiments » n'est pas décoratif.** Un modèle compartimental à un seul
compartiment n'est pas un modèle compartimental : il n'y a nulle part où aller. La contrainte
dit ce que le paradigme exige et un fichier qui ne la respecte pas est rejeté avant la requête.

`DifferentialEquation` gouverne **exactement un** compartiment, parce qu'une équation
différentielle dans un modèle compartimental donne la variation du contenu d'un compartiment et
d'un seul, comme bilan des flux qui y entrent et en sortent.

### Les deux sortes de taux -- le cœur de la couche

| Classe | Parent | Ce qu'elle impose |
|---|---|---|
| `ConstantRate` | `RateSpecification` | — |
| `CompartmentDependentRate` | `RateSpecification` | `dependsOnCompartment` au moins 1 `Compartment` |

Les deux sont **déclarées disjointes** : un taux ne peut pas être à la fois constant et
dépendant d'un compartiment.

Un taux de guérison γ est constant. Une force d'infection βI/N dépend du contenu du compartiment
des infectieux. **C'est là et nulle part ailleurs, que le couplage se voit dans ce paradigme.**

**Ce que « constant » veut dire.** `ConstantRate` veut dire indépendant des compartiments, et
non fixe dans le temps : un taux saisonnier qui ne lit aucun compartiment est aussi un
`ConstantRate`. Sa valeur s'écrit alors avec `rateExpression`, car `rateConstantValue` ne
donne qu'une valeur fixe. Le commentaire de la classe le dit depuis le 15 octobre 2026
(correction 10) ; le nom est gardé.

### Les deux classes définies

```
CoupledFlow             ≡ TransitionFlow and (hasRate some CompartmentDependentRate)
CoupledCompartmentalModel ≡ CompartmentalModel and (hasFlow some CoupledFlow)
```

**Deux niveaux et c'est voulu.** Le flux est couplé parce que son taux dépend d'un
compartiment ; le modèle est couplé parce qu'il a au moins un flux couplé. Le raisonneur
enchaîne les deux déductions tout seul : il suffit de déclarer qu'un taux dépend d'un
compartiment pour que le modèle entier soit reconnu couplé.

C'est le pendant exact de `CoupledAgentBasedModel` en 3A, qui passe par une transition
déclenchée par une interaction.

### Lien avec 4-Checks

3B n'importe pas la couche 4. C'est le module 4-Checks (correction 9, 15 octobre 2026) qui
importe 3A, 3B et 4-Core et qui se sert de `ConstantRate` :

```
StaticApproximationFlow ≡ TransitionFlow and (hasRate some ConstantRate)
                          and (representsStateTransition some CoupledTransition)
```

Pour un flux qui représente une transition couplée de la maladie, trois cas, vérifiés le
19 octobre 2026 avec HermiT :

| Taux du flux | Ce que le raisonneur conclut |
|---|---|
| `CompartmentDependentRate` | le flux est `CoupledFlow`, le modèle `CoupledCompartmentalModel` |
| `ConstantRate` | le flux est `StaticApproximationFlow`, le modèle `StaticApproximationModel` |
| sorte non déclarée (`RateSpecification` seulement) | rien |

Le deuxième cas est une **approximation statique** : le modèle ignore le couplage, donc les
effets indirects d'une intervention. C'est un signalement, pas une erreur. Le troisième cas
rappelle le monde ouvert : tant que la sorte du taux n'est pas dite, le raisonneur ne
conclut rien.

### 7 propriétés d'objet

| Propriété | Domaine → Portée | Caractéristique |
|---|---|---|
| `hasCompartment` | CompartmentalModel → Compartment | — |
| `hasFlow` | CompartmentalModel → TransitionFlow | — |
| `hasRate` | TransitionFlow → RateSpecification | fonctionnelle |
| `dependsOnCompartment` | CompartmentDependentRate → Compartment | — |
| `hasEquation` | CompartmentalModel → DifferentialEquation | — |
| `involvesFlow` | DifferentialEquation → TransitionFlow | — |
| `governsCompartment` | DifferentialEquation → Compartment | fonctionnelle |

**Pas de `fromCompartment` ni de `toCompartment`** : ce seraient des doublons de `hasSourceState`
et `hasTargetState`, héritées de `TransitionComponent` en couche 2. Le même concept à deux
endroits finit par être rangé différemment selon le jour.

### 5 propriétés de données

| Propriété | Sur | Type |
|---|---|---|
| `compartmentSymbol` | Compartment | chaîne |
| `compartmentInitialSize` | Compartment | double |
| `rateExpression` | RateSpecification | chaîne |
| `rateConstantValue` | ConstantRate | double |
| `equationExpression` | DifferentialEquation | chaîne |

---

## Validation

### 1. Audit automatique

**Résultat au 19 octobre 2026 : 0 erreur, 1 avertissement.** 181 triplets. HermiT : aucune
classe insatisfiable. Les deux erreurs du 8 octobre (les guillemets d'en-tête) ont été
corrigées.

L'avertissement signale `hasEquation` comme déclarée sans apparaître dans un axiome. Conservée
sciemment, comme les trois propriétés décoratives de 3A.

Pour reproduire, depuis la racine du dépôt : `bash tools/audit_tout.sh`, ou pour 3B seule :

```
python tools/audit_ontosim.py --focus src/ontology/layer3b_equations.ttl \
    --load src/ontology/layer1_foundational.ttl src/ontology/layer2_modsim.ttl src/ontology/layer3b_equations.ttl \
    --ref tools/ref/ro.owl tools/ref/iao.owl tools/ref/bfo.owl tools/ref/ogms-edit.owl
```

### 2. Test de classification

Un modèle dont un flux porte un taux dépendant d'un compartiment doit être classé
`CoupledCompartmentalModel` et son flux `CoupledFlow`, **sans qu'on ait écrit ni l'un ni
l'autre**. Un modèle dont tous les taux sont constants ne doit l'être ni l'un ni l'autre.
**Vérifié le 19 octobre 2026** avec HermiT.

### 3. Test du garde-fou

Un taux déclaré à la fois `ConstantRate` et `CompartmentDependentRate` doit rendre l'ontologie
incohérente. **Vérifié le 19 octobre 2026.**

### 4. Le test qui a révélé la limite L3

En donnant **deux** états de départ au même flux, alors que `hasSourceState` est fonctionnelle,
l'ontologie reste cohérente : le raisonneur conclut que les deux compartiments sont le même,
plutôt que d'y voir une erreur. En déclarant les compartiments distincts par `owl:AllDifferent`,
HermiT détecte bien l'incohérence.

**Conséquence pratique à automatiser.** Toute description d'un modèle réel doit déclarer ses
compartiments mutuellement distincts. Une propriété fonctionnelle ne protège que si les
individus sont distincts et en OWL ils ne le sont pas par défaut.

### 5. OOPS!

**Résultat sur la version 1.1** (octobre 2026). OOPS! a évalué le fichier complet, produit
par `tools/construire.sh` : aucun défaut critique. Pour cette couche, un seul défaut, mineur : P13, inverse non déclaré,
pour les 7 propriétés d'objet, avec la même réponse qu'en couche 2. Le rapport accompagne la documentation : lien « Evaluation » en tête de page.

---

## Décisions consignées

| Code | Décision |
|---|---|
| D9 | La couche 3 ne décrit que des paradigmes. 33 classes → 9. |
| D12 | `SIR_Model` et `SEIR_Model` montent en couche 5 : ils combinent un paradigme et des états de santé. |
| — | Pas de `fromCompartment` ni `toCompartment` : doublons de la couche 2. |
| — | Disjonction `ConstantRate` ⊥ `CompartmentDependentRate` : garde-fou vérifié. |
| — | Parents explicites conservés sur les deux classes définies, de façon cohérente avec 3A. |
| — | `hasEquation` laissée sans axiome. |
| — | `ConstantRate` garde son nom ; son commentaire dit qu'il s'agit d'un taux indépendant des compartiments, pas d'un taux fixe (correction 10). |
| L3 | Les propriétés fonctionnelles ne protègent que si les individus sont déclarés distincts. Découvert ici. |

## Décisions ouvertes

| Question | À trancher lors de |
|---|---|
| `CompartmentalModel` a-t-il un équivalent dans OSDi ? | Avant soumission |
| Sort de `hasEquation` | Revue finale |

---

## Versionnement

Le numéro de version suit l'empilement entier, pas ce fichier seul. Même sans changement
d'axiome, la couche est passée en 1.1 avec les autres, en un seul geste, et son import de la
couche 2 a suivi. Voir la fiche de la couche 2, *Versionnement*.

<br>

<p align="center">
  🦋<br>
  <i>Fais avec amour et pour l'Amour.</i>
</p>