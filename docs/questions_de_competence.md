# OntoSim-Dis, Questions de compétence

**Version du 19 octobre 2026.** 

**Ce qui a changé depuis le 9 octobre.** Q15 passe à `OK` : le module 4-Checks signale les
modèles non couplés qui représentent une transition couplée. Q6 et Q20 passent à `manque` :
il leur manque une relation, détaillée sous chaque groupe. Q21 passe aussi à `manque`, car
elle demande la même relation que Q20. Les chiffres d'alignement de Q24 sont à jour.

**Colonne « état ».**

| État | Sens |
|---|---|
| `OK` | l'ontologie actuelle y répond, par requête SPARQL |
| `fermeture` | demande les axiomes de fermeture de la limite L1  |
| `manque` | **un terme est absent de l'ontologie** : à ajouter ou à déclarer hors périmètre (je vais le gerer lors des prochaines mises à jours)|
| `reporté` | En attente |
| `à construire` | demande un jeu de données, pas un terme |

**Compte au 19 octobre : 30 questions, 21 `OK`, 2 `fermeture`, 4 `manque`, 2 `reporté`,
1 `à construire`.**

---

## Groupe 1 -- Décrire une maladie

| # | Question | État |
|---|---|---|
| Q1 | Quels états de santé une maladie donnée définit-elle ? | OK |
| Q2 | Par quelles transitions passe-t-on d'un état de santé à un autre et dans quel sens ? | OK |
| Q3 | Qu'est-ce qui gouverne chaque transition : un déterminant couplé à la population ou un déterminant individuel ? | OK |
| Q4 | Quels états sont absorbants, c'est-à-dire qu'on ne peut plus en sortir ? | OK |
| Q5 | Quelle est la forme dynamique du cours de cette maladie : transitoire, chronique, progressive ou aiguë ? | OK |
| Q6 | Quels facteurs de risque augmentent la probabilité d'une transition donnée ? | **manque** |

**Pourquoi ce groupe.** Il vérifie que la couche 4 décrit réellement une maladie et pas
seulement une liste d'étiquettes. Si Q2 ou Q3 ne renvoient rien, la description est incomplète.

**Ce sur quoi elles reposent.** `DiseaseKnowledgeTemplate` exige au moins deux états de santé
et au moins une transition ; `HealthStateTransition` exige un état de départ, un état d'arrivée
et au moins un déterminant. Une description qui ne répondrait pas à Q1 ou Q2 serait rejetée par
le raisonneur avant même la requête.

**Ce qui manque à Q6.** Un facteur de risque est rattaché à la maladie (`hasRiskFactor`), pas à
une transition. Pour une transition, on ne peut passer que par son déterminant individuel et
les attributs qu'il lit (`dependsOnAttribute`), quand un attribut est aussi déclaré facteur de
risque. Soit on reformule la question au niveau de la maladie, et elle redevient `OK`, soit on
ajoute une relation entre un facteur de risque et une transition.


---

## Groupe 2 -- Le couplage, cœur de l'article

| # | Question | État |
|---|---|---|
| Q7 | Quelles maladies comportent au moins une transition dont le risque dépend de l'effectif d'une source ? | OK |
| Q8 | Pour une transition couplée, de l'effectif de quelle source dépend-elle ? | OK |
| Q9 | Quelles maladies ont **toutes** leurs transitions individuelles, donc des trajectoires indépendantes ? | fermeture |
| Q10 | Quel paramètre quantifie un déterminant donné et dans quelle unité ? | OK |
| Q11 | Une même transition peut-elle être gouvernée à la fois par un déterminant couplé et par un déterminant individuel et lesquelles le sont ? | OK |

**Pourquoi ce groupe.** C'est la contribution. Q7 est la question qui doit fonctionner **sans**
qu'on ait jamais déclaré qu'une maladie est infectieuse : elle passe par
`CoupledDiseaseKnowledge`, une classe définie.


---

## Groupe 3 -- Le pont vers les paradigmes

| # | Question | État |
|---|---|---|
| Q12 | Quel état de santé un compartiment ou un état d'agent représente-t-il ? | OK |
| Q13 | Quels modèles représentent une maladie donnée et dans quel paradigme ? | OK |
| Q14 | Un modèle est-il couplé et par quel mécanisme propre à son paradigme : taux dépendant d'un compartiment ou transition déclenchée par une interaction ? | OK |
| Q15 | Existe-t-il des modèles **incohérents** avec la maladie qu'ils représentent, c'est-à-dire non couplés alors que le déterminant de la maladie l'est ? | OK |
| Q16 | Quels états de santé d'une maladie ne sont représentés par aucun composant d'un modèle donné ? | fermeture |

**Pourquoi ce groupe.** Il teste les trois ponts de la décision D14, donc la cohérence de toute
l'architecture. Q15 et Q16 sont des **détecteurs d'erreur** : elles ne servent pas à décrire,
mais à trouver ce qui cloche. Ce sont les plus utiles pour la validation.

**Q15 et le module 4-Checks.** Un modèle qui représente une transition couplée avec un taux
constant, ou avec une transition d'agent déclenchée par les seuls attributs de l'agent, est
classé `StaticApproximationModel`. Il est **signalé, pas interdit** : ce n'est pas une
incohérence logique, mais une approximation à justifier. Vérifié le 19 octobre 2026. Si la
sorte du taux n'est pas déclarée, le raisonneur ne conclut rien.


---

## Groupe 4 -- Contexte et transférabilité

| # | Question | État |
|---|---|---|
| Q17 | Quelles populations, régions et infrastructures de santé un modèle donné suppose-t-il ? | OK |
| Q18 | Quels modèles ont été construits pour un contexte comparable à celui du Sénégal, climat, densité, infrastructure ? | OK |
| Q19 | Quels paramètres d'un modèle doivent être réestimés si on change de contexte géographique ? | **manque** |


---

## Groupe 5, Choix et génération d'un modèle

| # | Question | État |
|---|---|---|
| Q20 | Quelles familles de modèles conviennent à une maladie donnée, compte tenu de son déterminant et de la forme de son cours ? | **manque** |
| Q21 | Quelles familles sont **exclues** pour cette maladie et pourquoi ? | **manque** |
| Q22 | De quels éléments a-t-on besoin pour générer un modèle à événements discrets à partir de cette description ? | reporté |
| Q23 | Quelles variables partagées faut-il créer et quelles étapes doivent les mettre à jour ? | reporté |

**Pourquoi ce groupe.** C'est la chaîne qui mène à la génération. 

**Ce qui manque à Q20 et Q21.** Le raisonneur classe la maladie, couplée ou à progression
individuelle, et selon la forme de son cours, mais le lien entre ces classes et les familles
de modèles n'est écrit que dans les définitions (« modélisable par microsimulation… »), pas
dans des axiomes. Une requête ne peut donc pas le suivre. Q21 demande en plus une fermeture.


---

## Groupe 6, Mapping vers OSDi et non-régression

| # | Question | État |
|---|---|---|
| Q24 | Quels éléments de cette description ont un équivalent dans OSDi et lesquels n'en ont pas ? | OK |
| Q25 | Les maladies déjà décrites dans OSDi sont-elles classées de la même façon après l'extension ? | à construire |
| Q26 | Quels éléments d'OSDi n'ont aucun équivalent chez nous ? | OK |


**Chiffres utiles pour Q24 (au 19 octobre) :** **36 alignements** posés au total,
21 `exactMatch`, 13 `closeMatch`, 2 `relatedMatch`. **34 visent OSDi** ; ce sont 34 des 35
cibles vérifiées existantes dans `OSDi.ttl` le 9 octobre. Les 2 autres visent des termes OBO
(`RiskFactor` → `OGMS_0000030`, `Population` → `OGMS_0000084`).

Répartition par module : 19 en 4-Core (18 OSDi + 1 OBO), 13 en couche 2, 2 en 4-Context
(1 + 1), 1 en 3A, 1 en 4-Infectious, **0 en 3B**.

L'alignement retiré est le `relatedMatch` de `TransitionDeterminant` vers
`osdi:hasRiskCharacterization` : il reliait une classe à une propriété. Une note de l'éditeur
dit maintenant que `TransitionDeterminant` n'a pas d'équivalent dans OSDi.


---

## Groupe 7, La transmission environnementale


| # | Question | État |
|---|---|---|
| Q27 | Quelles maladies se transmettent par un réservoir environnemental plutôt que de personne à personne ? | OK |
| Q28 | Pour une maladie à transmission environnementale, quel est le réservoir et de quel rôle épidémiologique est-il l'état ? | OK |
| Q29 | Un déterminant couplé l'est-il directement, par un effectif humain ou indirectement, par un effectif non humain ? | OK |
| Q30 | Quelles maladies partagent à la fois la même forme de cours et le même type de déterminant ? | OK |


---

## Les questions `fermeture` et SPARQL

Le raisonneur, en monde ouvert, ne peut pas répondre à Q9 ni à Q16 sans axiomes de fermeture :
c'est la limite L1, et c'est un résultat à publier, pas un échec. Une requête SPARQL, elle, peut
y répondre en monde fermé : `FILTER NOT EXISTS` traite l'absence d'une information comme
l'absence de la chose. Pour Q9 :

```sparql
PREFIX dsim: <https://w3id.org/ontosim-dis#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?maladie WHERE {
  ?maladie a dsim:DiseaseKnowledgeTemplate .
  FILTER NOT EXISTS {
    ?maladie dsim:hasStateTransition/dsim:isGovernedBy ?d .
    ?d a/rdfs:subClassOf* dsim:PopulationCoupledDeterminant
  }
}
```

Essayée le 19 octobre 2026 sur deux maladies, l'une couplée et l'autre non : elle renvoie
seulement la seconde. La même méthode répond à Q16. C'est un choix à écrire dans l'article :
la réponse n'est juste que si la description est complète.


---



<br>

<p align="center">
  🦋<br>
  <i>Fais avec amour et pour l'Amour.</i>
</p>