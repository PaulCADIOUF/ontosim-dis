# Cahier de conception — OntoSim-Dis, Couche 1 (fondations)

Version de la couche : 1.0 — cahier mis à jour le 19 octobre 2026
Auteur : Paul Cheikh Anta DIOUF

> **Comment utiliser ce cahier.** Chaque entrée consigne une décision : ce qui a été décidé,
> pourquoi, et quelle alternative a été écartée. Les justifications ci-dessous reprennent ce qui
> a été établi pendant la conception. **Relisez chaque entrée et réécrivez-la avec vos propres mots**
> avant de cocher la case. Règle : si vous ne pouvez pas défendre une entrée à l'oral en trente
> secondes, ne la cochez pas, et revenez sur la décision.

**Mise à jour du 19 octobre 2026.** Nouvel espace de noms w3id.org (C1-01) ; décision D1
tranchée (C1-03) ; sept relations de RO retirées (C1-06), ce qui clôt C1-08, C1-09 et C1-14
et réduit C1-10 et C1-12 ; règle des commentaires des termes importés (C1-16, nouvelle).

---

## C1-01 — Renommage OntoSim-Epi → OntoSim-Dis

**Décision.** L'ontologie change de nom et d'espace de noms. Les termes ont pour IRI
`https://w3id.org/ontosim-dis#…`, et chaque module a la sienne :
`https://w3id.org/ontosim-dis/layer1`, `https://w3id.org/ontosim-dis/layer2`, etc.

**Justification.** *(à confirmer par vous)* L'ontologie ne se limite plus aux maladies
infectieuses : la couche 4 devient un noyau commun à toutes les maladies, dont on dérive
ensuite les types. Le nom « Epi » ne décrit plus le périmètre.

w3id.org est un service d'identifiants permanents : l'adresse d'un terme reste la même si
l'ontologie change d'hébergement.

**Alternative écartée.** Garder OntoSim-Epi et changer seulement le contenu.

**Conséquence.** Tous les modules utilisent maintenant cet espace de noms (au 22 septembre,
c'était encore `http://www.ontosim-dis.org/`). Pour que les adresses mènent vraiment au
dépôt, l'espace de noms devra être enregistré auprès de w3id.org au moment de publier.

- [ ] Relu et reformulé

---

## C1-02 — Extraction par MIREOT plutôt qu'import complet

**Décision.** Les termes de BFO, RO et IAO sont recopiés un par un (MIREOT), au lieu
d'importer ces ontologies entières par `owl:imports`.

**Justification.** On ne charge que ce qui sert. Un import complet ferait entrer des milliers
de termes inutiles, alourdirait le raisonnement et rendrait l'ontologie plus difficile à lire.
C'est la pratique de l'OBO Foundry pour les ontologies de domaine.

**Alternative écartée.** `owl:imports` de BFO, RO et IAO complets.

**Contrepartie assumée.** Les termes recopiés doivent être tenus à jour à la main : d'où
l'entrée C1-04 sur les versions.

- [ ] Relu et reformulé

---

## C1-03 — OGMS n'est pas dans la couche 1

**Décision.** Les termes d'OGMS (maladie, désordre, cours de maladie) ne sont pas placés
dans la couche 1.

**Justification.** La couche 1 est définie comme contenant « les concepts fondateurs
indépendants de tout domaine applicatif ». OGMS est une ontologie médicale : la mettre ici
contredirait la définition même de la couche.

**Alternatives.** (a) mettre OGMS dans la couche 1 — écarté, pour la raison ci-dessus ;
(b) le recopier directement dans la couche 4 ; (c) le placer dans un module d'import séparé,
chargé par la couche 4.

**Décision D1, tranchée : (c).** Les dix termes d'OGMS sont dans `layer4-ogms.ttl`, que
4-Core importe. C'est la pratique de l'OBO Foundry, et on voit d'un coup d'œil ce qui est
repris d'OGMS.

- [ ] Relu et reformulé

---

## C1-04 — Versions de référence des sources

**Décision.** La couche est validée contre : BFO 2.0 ; RO 2026-09-04 ; IAO 2026-03-30.
Les fichiers de ces versions sont dans `tools/ref/`.

**Justification.** Les sources évoluent, et les copies qui circulent sont parfois périmées.
Deux cas rencontrés pendant la conception :
- RO a renommé `RO_0000052` : l'ancien libellé « inheres in », encore utilisé par IDO,
  est devenu « characteristic of » ;
- OGMS a redéfini `symptom` en 2020, alors qu'IDO garde l'ancienne définition.

Sans version consignée, on ne saurait plus contre quoi la couche a été vérifiée.

**Alternative écartée.** Citer les sources sans version.

- [ ] Relu et reformulé

---

## C1-05 — Libellés alignés sur les sources officielles

**Décision.** Chaque libellé reprend exactement celui de la source officielle :
`has participant` (et non `has_participant`), `disposition` (et non `Disposition`),
`is about` (et non `isAbout`).

**Justification.** Un outil qui croise plusieurs ontologies compare les libellés. Un écart
d'une majuscule ou d'un tiret bas suffit à faire croire à deux termes différents.

- [ ] Relu et reformulé

---

## C1-06 — Termes retirés

**Décision.** Dix termes ont été retirés, en deux fois.

Le 22 septembre 2026 : `has quality` (RO_0000086), `temporal region` (BFO_0000008),
`process boundary` (BFO_0000035).

En octobre 2026, sept relations de RO : `characteristic of` (RO_0000052),
`has characteristic` (RO_0000053), `characteristic of part of` (RO_0002314),
`depends on` (RO_0002502), `has disposition` (RO_0000091), `participates in` (RO_0000056),
`located in` (RO_0001025).

**Justification.**
- Aucun module ne les utilise (principe MIREOT : on n'importe que ce qui sert).
- `has quality` servait en outre à rattacher les paramètres épidémiologiques au modèle,
  ce qui était une erreur de catégorie : dans la couche 2, les paramètres sont des
  `ModelParameter`, donc des artefacts d'information. Un nombre écrit dans un modèle
  n'est pas une qualité d'une chose.
- `located in` relie des entités matérielles réelles. Les régions de 4-Context sont des
  descriptions de territoires : elles utilisent leur propre relation, `isSubRegionOf`.
- `has disposition` et `participates in` étaient anticipés pour les couches 4 et 3A, qui
  ont finalement pris un autre chemin : voir C1-09 et C1-14.

**Alternative écartée.** Les garder « au cas où ».

- [ ] Relu et reformulé

---

## C1-07 — `immaterial entity` est gardé bien qu'aucune couche ne l'utilise

**Décision.** `immaterial entity` (BFO_0000141) est conservé.

**Justification.** Il est nécessaire comme second terme de la disjonction
`material entity ⊥ immaterial entity` (voir C1-11). Sans lui, cette disjonction ne peut pas
être écrite.

- [ ] Relu et reformulé

---

## C1-08 — `has characteristic` (entrée close)

**Décision d'origine.** `has characteristic` (RO_0000053) était conservé comme inverse de
`characteristic of` et parent de `has disposition` dans RO.

**Close en octobre 2026.** Les trois termes ont été retirés ensemble (C1-06) : aucun module
ne les utilisait, et il ne reste plus de hiérarchie à préserver.

- [ ] Relu et reformulé

---

## C1-09 — `has disposition` (entrée close)

**Décision d'origine.** `has disposition` (RO_0000091) était anticipé pour la couche 4 :
dans le patron OGMS, un organisme **porte** une maladie, qui est une disposition. Il
devait être retiré si la couche 4 terminée ne l'utilisait pas.

**Close en octobre 2026.** La couche 4 ne l'utilise pas. Elle ne décrit pas l'organisme
malade, mais la connaissance qu'on a de la maladie : le lien vers la maladie réelle passe
par `representsDisease`, une sorte de `is about`. Le terme a donc été retiré, comme prévu
(C1-06).

- [ ] Relu et reformulé

---

## C1-10 — Parents de propriétés conservés

**Décision.** Sont conservés, bien qu'aucune couche ne les utilise directement :
`overlaps` et `mereotopologically related to`.

**Justification.** Ce sont les ancêtres de `part of`, qui est utilisée
(`part of ⊑ overlaps ⊑ mereotopologically related to`). Les garder préserve la hiérarchie
de RO, et donc les déductions que le raisonneur fait par héritage de propriétés.

**Alternative écartée.** Ne garder que les propriétés utilisées, sans leurs parents :
on perdrait la cohérence avec RO.

**Mise à jour d'octobre 2026.** `characteristic of part of` et `depends on`, qui figuraient
ici, sont partis avec les relations qu'ils coiffaient (C1-06).

- [ ] Relu et reformulé

---

## C1-11 — Les six disjonctions

**Décision.** Six paires de catégories sont déclarées disjointes. Chacune attrape un type
d'erreur précis :

| Disjonction | Erreur qu'elle attrape |
|---|---|
| continuant ⊥ occurrent | Confondre une chose et un processus, par exemple un modèle (`SimulationModel`) avec son exécution (`SimulationExecution`) |
| independent continuant ⊥ specifically dependent continuant | Traiter une qualité ou une disposition comme un objet autonome |
| independent continuant ⊥ generically dependent continuant | Ranger un artefact d'information (un modèle, un paramètre) sous une chose physique |
| specifically dependent continuant ⊥ generically dependent continuant | Confondre une maladie réelle (une disposition) avec la connaissance qu'on en a (un artefact d'information) — protège la distinction entre `OGMS:disease` et `DiseaseKnowledgeTemplate` |
| material entity ⊥ immaterial entity | Confondre un objet et un lieu ou une frontière |
| realizable entity ⊥ quality | Confondre une maladie (disposition, réalisable) avec une qualité comme la sévérité |

**Justification.** Sans disjonctions, le raisonneur accepte ces erreurs en silence.

- [ ] Relu et reformulé

---

## C1-12 — Caractéristiques des propriétés

**Décision.** Les caractéristiques sont reprises de RO et de BFO :

| Propriété | Caractéristique | Ce qu'elle permet |
|---|---|---|
| part of | transitive | Une partie d'une partie est une partie du tout |
| overlaps | symétrique | Si A chevauche B, B chevauche A |
| realized in / realizes | inverses | « Cette maladie se réalise dans ce cours » ⇔ « ce cours réalise cette maladie » |

**Mise à jour d'octobre 2026.** `located in` (transitive), `characteristic of`
(fonctionnelle) et `has characteristic` (inverse-fonctionnelle) ont été retirés (C1-06).

- [ ] Relu et reformulé

---

## C1-13 — Décision D2 en suspens : `has input` / `has output`

**Situation.** Ces relations sont conservées pour la recomposition, avec une note de
l'éditeur qui signale le problème.

**Le problème.** RO réserve `has input` aux entrées matérielles. Or les composants du
Quadruplet (DK, CK, MSK, EK) sont des artefacts d'information.

**Pourquoi c'est en suspens.** La recomposition n'est pas encore conçue : la décision se
prendra avec elle.

**Options pour plus tard.** (a) retirer ces relations ; (b) les remplacer par
`has specified input` / `has specified output` d'OBI, qui acceptent les artefacts
d'information, à condition de déclarer la recomposition comme processus planifié
(`COB_0000035`).

- [ ] Relu et reformulé

---

## C1-14 — Un agent participe-t-il à la simulation ? (entrée close)

**Question d'origine (décision D4).** `participates in` (RO_0000056) était conservé sans
utilisation. En BFO, une information n'agit pas : c'est sa réalisation concrète (le
programme qui tourne) qui participe à un processus. Si `Agent` est la description d'un
agent, il ne peut pas « participer » directement.

**Close en octobre 2026.** La couche 3A a tranché : elle décrit des catégories d'agents
(`AgentType`), qui sont des descriptions ; l'agent individuel n'existe qu'à l'exécution et
n'est pas modélisé. `participates in` n'avait donc pas d'usage, et a été retiré (C1-06).

- [ ] Relu et reformulé

---

## C1-15 — Licence

**Décision.** Licence Creative Commons Attribution 4.0 (CC BY 4.0).

**Justification.** Permet la réutilisation avec attribution. C'est aussi la licence d'OGMS
et de BFO. Enfin, l'absence de licence est un défaut « important » pour OOPS! : c'est
exactement celui que l'article FRMO a dû corriger.

- [ ] Relu et reformulé

---

## C1-16 — Commentaires des termes importés : la source d'un côté, nos notes de l'autre

**Décision (octobre 2026).** Pour chaque terme recopié, `rdfs:comment` contient la
définition officielle de la source, et rien d'autre. Ce qu'OntoSim-Dis ajoute (pourquoi
le terme est là, à quoi il sert) va dans une note de l'éditeur (`editor note`,
IAO_0000116). Les décisions en suspens sont signalées de la même façon, par une note
écrite pour un lecteur extérieur (« Décision en suspens : … »), jamais par une note
personnelle.

**Justification.** Un lecteur, ou un outil, doit pouvoir distinguer ce que dit BFO de ce
que nous en disons. Mettre nos explications dans `rdfs:comment` attribuerait à BFO des
phrases qui ne sont pas les siennes.

**Alternative écartée.** Garder nos explications dans `rdfs:comment`, à côté ou à la place
de la définition officielle.

- [ ] Relu et reformulé
