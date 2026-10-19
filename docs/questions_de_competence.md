# OntoSim-Dis — Questions de compétence

**Brouillon à valider.** Ces questions sont les vôtres à deux titres : elles disent ce que
votre ontologie doit savoir faire, et elles serviront d'instrument de validation, exécutées en
SPARQL. Ce document est une proposition de départ, pas une liste arrêtée.

**Ce qu'il faut en faire.**
1. Les relire et **en supprimer celles qui ne vous servent pas**. Une question de compétence
   qu'on garde « au cas où » alourdit la validation sans rien prouver.
2. **En ajouter** : celles qui viennent de votre thèse et que je ne peux pas deviner.
3. Les faire **valider par Iván**, et si possible par un épidémiologiste. Des questions validées
   par des tiers ne sont plus vos suppositions.

**Colonne « état ».**
`OK` — l'ontologie actuelle y répond · `partiel` — elle y répond en partie, la note dit ce qui
manque · `fermeture` — le raisonneur ne peut pas répondre sans les axiomes de fermeture de la
limite L1, mais une requête SPARQL en monde fermé le peut · `3C` — attend le retour de la couche
des événements discrets, retirée le 9 octobre 2026 · `à construire` — il manque une relation ou
un test · `hors périmètre` — ne sera pas traitée, à dire explicitement.

**État au 19 octobre 2026.** Sur les 26 questions de départ : 16 `OK`, 3 `partiel`,
2 `fermeture`, 3 `à construire`, 2 `3C`. Depuis la version précédente, Q15 et Q17 sont passées
à `OK` (modules 4-Checks et 4-Context), et Q18 à `partiel` ; Q6 et Q20, notées `OK` à tort,
sont redescendues à `partiel` ; Q19 et Q21 sont `à construire`. Quatre questions sont
proposées en fin de document (Q27 à Q30).

---

## Groupe 1 — Décrire une maladie

| # | Question | État |
|---|---|---|
| Q1 | Quels états de santé une maladie donnée définit-elle ? | OK |
| Q2 | Par quelles transitions passe-t-on d'un état de santé à un autre, et dans quel sens ? | OK |
| Q3 | Qu'est-ce qui gouverne chaque transition : un déterminant couplé à la population ou un déterminant individuel ? | OK |
| Q4 | Quels états sont absorbants, c'est-à-dire qu'on ne peut plus en sortir ? | OK |
| Q5 | Quelle est la forme dynamique du cours de cette maladie : transitoire, chronique, progressive ou aiguë ? | OK |
| Q6 | Quels facteurs de risque augmentent la probabilité d'une transition donnée ? | partiel |

**Pourquoi ce groupe.** Il vérifie que la couche 4 décrit réellement une maladie, et pas
seulement une liste d'étiquettes. Si Q2 ou Q3 ne renvoient rien, la description est incomplète.

**Q6, ce qui manque.** Un facteur de risque est rattaché à la maladie (`hasRiskFactor`), pas à
une transition. Pour une transition, on ne peut passer que par son déterminant individuel et
les attributs qu'il lit (`dependsOnAttribute`), quand un attribut est aussi déclaré facteur de
risque. Soit on reformule la question au niveau de la maladie, soit on ajoute une relation.

---

## Groupe 2 — Le couplage, cœur de l'article

| # | Question | État |
|---|---|---|
| Q7 | Quelles maladies comportent au moins une transition dont le risque dépend de l'état de la population ? | OK |
| Q8 | Pour une transition couplée, de l'effectif de quel état de santé, ou de quel état de réservoir, dépend-elle ? | OK |
| Q9 | Quelles maladies ont **toutes** leurs transitions individuelles, donc des trajectoires indépendantes ? | fermeture |
| Q10 | Quel paramètre quantifie un déterminant donné, et dans quelle unité ? | OK |
| Q11 | Une même transition peut-elle être gouvernée à la fois par un déterminant couplé et par un déterminant individuel, et lesquelles le sont ? | OK |

**Pourquoi ce groupe.** C'est la contribution de l'article. Q7 est la question qui doit
fonctionner **sans** qu'on ait jamais déclaré qu'une maladie est infectieuse. Vérifié le
19 octobre 2026 : une maladie dont une transition est gouvernée par un déterminant couplé est
classée `CoupledDiseaseKnowledge`, une maladie à déterminants individuels ne l'est pas.

Q8 a été élargie : depuis que le couplage peut lire un état de réservoir (`CouplingSource`),
le risque d'une transition peut dépendre d'escargots infectés et non seulement d'humains.

Q9 est la question qui révèle la limite L1 : en monde ouvert, prouver qu'il n'existe pas
d'autre transition demande des axiomes de fermeture. **À garder précisément pour cette raison** :
elle documente une limite réelle. Une requête SPARQL en monde fermé y répond, elle (voir la
dernière partie).

Q11 mérite votre attention : la vaccination d'une maladie transmissible mêle les deux — le
risque d'infection dépend des autres, l'effet du vaccin dépend de l'individu.

---

## Groupe 3 — Le pont vers les paradigmes

| # | Question | État |
|---|---|---|
| Q12 | Quel état de santé un compartiment ou un état d'agent représente-t-il ? | OK |
| Q13 | Quels modèles représentent une maladie donnée, et dans quel paradigme ? | OK |
| Q14 | Un modèle est-il couplé, et par quel mécanisme propre à son paradigme : taux dépendant d'un compartiment, ou interaction entre agents ? | OK |
| Q15 | Existe-t-il des modèles **incohérents** avec la maladie qu'ils représentent, c'est-à-dire non couplés alors que le déterminant de la maladie l'est ? | OK |
| Q16 | Quels états de santé d'une maladie ne sont représentés par aucun composant d'un modèle donné ? | fermeture |

**Pourquoi ce groupe.** Il teste les trois ponts de la décision D14, donc la cohérence de toute
l'architecture. Q15 et Q16 sont des **détecteurs d'erreur** : elles ne servent pas à décrire,
mais à trouver ce qui cloche. Ce sont les plus utiles pour la validation.

**Les changements.** Q12 et Q14 ne citent plus la couche 3C (étape de flux, variable partagée).
Q13 n'a pas de relation directe : la requête passe par les composants du modèle et les états
qu'ils représentent. Q15 est passée à `OK` avec le module 4-Checks : un modèle qui représente
une transition couplée avec un taux constant, ou avec une transition d'agent déclenchée par les
seuls attributs de l'agent, est classé `StaticApproximationModel`. Il est **signalé, pas
interdit** : ce n'est pas une incohérence logique, mais une approximation à justifier.
Vérifié le 19 octobre 2026 ; si la sorte du taux n'est pas déclarée, le raisonneur ne conclut
rien.

---

## Groupe 4 — Contexte et transférabilité

| # | Question | État |
|---|---|---|
| Q17 | Quelles populations, régions et infrastructures de santé un modèle donné suppose-t-il ? | OK |
| Q18 | Quels modèles ont été construits pour un contexte comparable à celui du Sénégal — climat, densité, infrastructure ? | partiel |
| Q19 | Quels paramètres d'un modèle doivent être réestimés si on change de contexte géographique ? | à construire |

**Pourquoi ce groupe.** C'est ce qui vous distingue le plus d'OSDi, dont la population est une
cohorte clinique sans géographie. Q18 et Q19 sont au cœur de votre thèse : réutiliser un modèle
ailleurs que là où il a été construit.

**Ce qui manque.** Q17 est passée à `OK` avec 4-Context (`hasContextKnowledge`, puis
population, région, infrastructure). Pour Q18, l'ontologie a les descripteurs (climat,
densité, infrastructure) mais pas la notion de « comparable » : les critères doivent être
fixés dans la requête. Pour Q19, aucune relation ne dit encore qu'un paramètre dépend du
contexte.

---

## Groupe 5 — Choix et génération d'un modèle

| # | Question | État |
|---|---|---|
| Q20 | Quelles familles de modèles conviennent à une maladie donnée, compte tenu de son déterminant et de la forme de son cours ? | partiel |
| Q21 | Quelles familles sont **exclues** pour cette maladie, et pourquoi ? | à construire |
| Q22 | De quels éléments a-t-on besoin pour générer un modèle à événements discrets à partir de cette description ? | 3C |
| Q23 | Quelles variables partagées faut-il créer, et quelles étapes doivent les mettre à jour ? | 3C |

**Pourquoi ce groupe.** C'est la chaîne qui mène à la génération. Q21 est celle qui donne sa
valeur au raisonnement : une ontologie qui ne sait qu'ajouter, sans jamais exclure, n'aide pas
à choisir.

**Ce qui manque.** Le raisonneur classe la maladie — couplée ou individuelle, et selon la forme
de son cours — mais le lien entre ces classes et les familles de modèles n'est écrit que dans
les définitions (« modélisable par microsimulation… »), pas dans des axiomes. Q20 est donc
`partiel`, et Q21 demande ce lien plus une fermeture. Q22 et Q23 attendent la décision sur la
couche 3C.

---

## Groupe 6 — Mapping vers OSDi et non-régression

| # | Question | État |
|---|---|---|
| Q24 | Quels éléments de cette description ont un équivalent dans OSDi, et lesquels n'en ont pas ? | OK |
| Q25 | Les maladies déjà décrites dans OSDi sont-elles classées de la même façon après l'extension ? | à construire |
| Q26 | Quels éléments d'OSDi n'ont aucun équivalent chez nous ? | OK |

**Pourquoi ce groupe.** Q24 produit directement le tableau de la contribution de l'article :
l'ontologie compte 34 alignements vers OSDi (21 `exactMatch`, 12 `closeMatch`,
1 `relatedMatch`), et des notes disent quand un terme n'a pas d'équivalent. Q25 est le test de
non-régression, qui devient la pièce maîtresse dès lors que JaDES est modifié. Q26 est
l'honnêteté symétrique : OSDi couvre les coûts, les utilités et les stratégies, que vous ne
couvrez pas. Elle demande de charger le fichier d'OSDi à côté du vôtre.

---

## Questions proposées le 19 octobre 2026

Ces quatre questions répondent à deux des points ci-dessous (la schistosomiase et la
réutilisation). Elles sont proposées : à garder, reformuler ou supprimer.

| # | Question | État |
|---|---|---|
| Q27 | Quelles maladies se transmettent par un réservoir — un milieu ou un hôte non humain — et non seulement d'une personne à l'autre ? | OK |
| Q28 | Pour une transition couplée, le risque dépend-il d'humains, d'un réservoir, ou des deux ? | OK |
| Q29 | Comment évolue l'effectif d'un réservoir, par exemple celui des escargots infectés ? | à construire |
| Q30 | Quels modèles existants pourraient servir dans une situation donnée : même sorte de maladie, même objectif, portée générale, contexte comparable ? | partiel |

Q27 est le test `tests/test_transmission_environnementale.ttl` : la schistosomiase est classée
`EnvironmentallyMediatedDiseaseKnowledge`, la COVID-19 ne l'est pas. Q28 repose sur
`DirectlyCoupledDeterminant` et `IndirectlyCoupledDeterminant`, qui ne sont pas disjoints :
le cycle complet de la schistosomiase lit les deux. Q29 attend le cycle de l'escargot, à
ajouter à l'ontologie. Q30 s'appuie sur les trois listes qui classent un modèle (`ModelNature`,
`ModelScope`, `ModelPurpose`) et sur le contexte ; comme pour Q18, les critères de
ressemblance doivent être fixés dans la requête.

---

## Quatre questions à ne pas oublier d'ajouter

Ce sont celles que je ne peux pas formuler à votre place, parce qu'elles viennent de votre
thèse et de votre terrain.

1. **La schistosomiase.** Sa transmission passe par l'eau et par les escargots, donc par un
   réservoir environnemental et non d'une personne à l'autre. Quelle question de compétence
   doit vérifier que votre ontologie sait l'exprimer ? *Proposition faite : Q27 à Q29.*
2. **La recomposition.** Quand elle reviendra, quelle question dira qu'une recomposition est
   valide ou non ?
3. **La réutilisation d'un modèle existant.** Votre thèse promet de retrouver un modèle
   pertinent pour une situation donnée. Quelle question formule cette recherche ?
   *Proposition faite : Q30.*
4. **Ce que vous refusez de traiter.** Une bonne liste dit aussi ce qu'elle ne couvre pas :
   le coût économique, la décision de santé publique, la qualité des données. Écrivez-le.

---

## Comment s'en servir pour la validation

1. **Traduire chaque question en SPARQL** — celles marquées `OK` d'abord.
2. **Les exécuter** sur la description d'une maladie réelle.
3. **Compter** : combien renvoient un résultat juste, combien échouent, et pourquoi.
4. **Publier le compte tel quel**, échecs compris. C'est ce que fait l'article FRMO avec ses
   défauts OOPS!, et c'est ce qui rend une validation crédible.

**Les questions `fermeture`.** Le raisonneur, en monde ouvert, ne peut pas y répondre tant que
les axiomes de fermeture ne sont pas générés. **C'est un résultat, pas un échec** : il documente
la limite L1, et il justifie que l'outil de description les génère automatiquement.

Une requête SPARQL, elle, peut y répondre en monde fermé : `FILTER NOT EXISTS` traite
l'absence d'une information comme l'absence de la chose. Par exemple, pour Q9 :

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
