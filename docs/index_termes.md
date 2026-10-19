# OntoSim-Dis — Index alphabétique des termes

**325 termes**, régénéré le 19 octobre 2026 à partir des 9 fichiers de `src/ontology`, par `tools/index_termes.py`. Ne pas modifier à la main : relancer le script.

Pour chaque terme : le module où il se trouve, sa nature, et sa définition française (l'anglaise à défaut). Les **classes définies** sont celles que le raisonneur sait reconnaître seul ; les termes `importé` viennent de BFO, RO, IAO ou OGMS par MIREOT et portent leur libellé officiel en italique.

| Module | Termes |
|---|---|
| Couche 1 | 22 |
| Couche 2 | 105 |
| Couche 3A | 22 |
| Couche 3B | 21 |
| 4-OGMS | 10 |
| 4-Core | 59 |
| 4-Infectious | 49 |
| 4-Context | 34 |
| 4-Checks | 3 |

| Terme | Module | Nature | Définition |
|---|---|---|---|
| `AcuteCourseDiseaseKnowledge` | 4-Core | **classe définie** | Maladie à début brutal. Quatrième forme de cours reconnue par OGMS, aux côtés des formes chronique, progressive et transitoire. Contraint peu la structure du… |
| `ADEQUACY` | Couche 2 | valeur | Évaluation qualitative de la logique et des hypothèses du modèle. |
| `AdministrativeRegion` | 4-Context | classe | Division administrative d'un pays. Le Sénégal en compte quatorze. |
| `AgentBasedModel` | Couche 3A | classe | Modèle dans lequel des agents autonomes, suivant chacun son comportement, interagissent et produisent le comportement du système. |
| `AgentState` | Couche 3A | classe | État qu'un agent peut occuper. Forme multi-agents d'un composant d'état. |
| `AgentTransition` | Couche 3A | classe | Changement d'état d'un agent. Hérite de la transition de couche 2 ses états de départ et d'arrivée. |
| `AgentType` | Couche 3A | classe | Catégorie d'entités autonomes du modèle. L'agent individuel n'est pas modélisé car il n'existe qu'à l'exécution. |
| `agentTypeName` | Couche 3A | donnée | Nom de la catégorie d'agents. |
| `AIRBORNE` | 4-Infectious | valeur | Par des particules fines restant en suspension dans l'air. |
| `alphaParameter` | Couche 2 | donnée | Paramètre de forme d'une loi bêta ou gamma. |
| `appliesExecutionKnowledge` | Couche 2 | relation | Lie un processus d'exécution à la configuration qu'il réalise. Fonctionnelle : une exécution applique une configuration et une seule. |
| `AridClimate` | 4-Context | classe | Climat sec à faibles précipitations. |
| `AttributeDrivenTransition` | Couche 3A | classe | Transition déclenchée par les seuls attributs de l'agent : son âge, le temps passé dans son état courant. Déterminant individuel. |
| `averageHouseholdSize` | 4-Context | donnée | Nombre moyen de personnes par ménage. Gouverne l'intensité des contacts domestiques. |
| `avgHumidity` | 4-Context | donnée | Humidité relative moyenne en pourcentage. |
| `avgTemperature` | 4-Context | donnée | Température moyenne annuelle, en degrés Celsius. |
| `Bacterium` | 4-Infectious | classe | Agent pathogène unicellulaire dépourvu de noyau. |
| `basicReproductionNumber` | 4-Infectious | donnée | Nombre moyen de cas secondaires produits par un cas dans une population entièrement susceptible. |
| `Behavior` | Couche 3A | classe | Règle disant ce que fait un agent selon son état et ce qui l'entoure. |
| `behaviorExpression` | Couche 3A | donnée | Expression textuelle de la règle de comportement. |
| `BernoulliDistribution` | Couche 2 | classe | Loi d'un tirage unique à deux issues de probabilité donnée. |
| `BetaDistribution` | Couche 2 | classe | Loi sur l'intervalle de zéro à un, employée pour les proportions et les probabilités. |
| `betaParameter` | Couche 2 | donnée | Second paramètre de forme d'une loi bêta. |
| `BFO_0000001` | Couche 1 | importé | *entity* — An entity is anything that exists or has existed or will exist. |
| `BFO_0000002` | Couche 1 | importé | *continuant* — A continuant is an entity that persists, endures, or continues to exist through time while maintaining its identity. |
| `BFO_0000003` | Couche 1 | importé | *occurrent* — An occurrent is an entity that unfolds itself in time or it is the instantaneous boundary of such an entity (for example a beginning or an… |
| `BFO_0000004` | Couche 1 | importé | *independent continuant* — b is an independent continuant = Def. b is a continuant which is such that there is no c and no t such that b s-depends_on c at t. |
| `BFO_0000015` | Couche 1 | importé | *process* — An occurrent that has temporal proper parts and for some time t, p s-depends_on some material entity at t. |
| `BFO_0000016` | Couche 1 | importé | *disposition* — Dire que « b est une disposition » signifie que : b est une entité réalisable ; le porteur de b est une entité matérielle ; b est telle que, si… |
| `BFO_0000017` | Couche 1 | importé | *realizable entity* — Dire que b est une entité réalisable revient à dire que b est un continuant spécifiquement dépendant qui inhère dans un continuant… |
| `BFO_0000019` | Couche 1 | importé | *quality* — a quality is a specifically dependent continuant that, in contrast to roles and dispositions, does not require any further process in order to be… |
| `BFO_0000020` | Couche 1 | importé | *specifically dependent continuant* — b is a specifically dependent continuant = Def. b is a continuant & there is some independent continuant c which is not a… |
| `BFO_0000031` | Couche 1 | importé | *generically dependent continuant* — b is a generically dependent continuant = Def. b is a continuant that g-depends_on one or more other entities. |
| `BFO_0000040` | Couche 1 | importé | *material entity* — A material entity is an independent continuant that has some portion of matter as proper or improper continuant part. |
| `BFO_0000050` | Couche 1 | importé | *part of* — a core relation that holds between a part and its whole |
| `BFO_0000054` | Couche 1 | importé | *realized in* — Paraphrase of elucidation: a relation between a realizable entity and a process, where there is some material entity that is bearer of the… |
| `BFO_0000055` | Couche 1 | importé | *realizes* — Paraphrase of elucidation: a relation between a process and a realizable entity, where there is some material entity that is bearer of the… |
| `BFO_0000141` | Couche 1 | importé | *immaterial entity* —  |
| `BLOODBORNE` | 4-Infectious | valeur | Par le sang ou des produits sanguins. |
| `caseFatalityRate` | 4-Core | donnée | Fraction des cas symptomatiques se terminant par un décès, entre 0 et 1. Générique : vaut pour toute maladie létale. |
| `ChronicCourseDiseaseKnowledge` | 4-Core | **classe définie** | Maladie dont le cours ne revient pas à l'homéostasie normale. Impose au moins un état absorbant. |
| `City` | 4-Context | classe | Localité urbaine. |
| `Climate` | 4-Context | classe | Conditions climatiques influençant la transmission des maladies. Déterminantes pour les maladies à vecteur et à transmission hydrique, où température et… |
| `Compartment` | Couche 3B | classe | Groupe d'individus partageant la même situation, comptés ensemble. Forme compartimentale d'un composant d'état. |
| `CompartmentalModel` | Couche 3B | classe | Modèle divisant la population en compartiments, entre lesquels des flux font passer les individus à certains taux. |
| `CompartmentDependentRate` | Couche 3B | classe | Taux dont la valeur dépend du contenu courant d'un ou plusieurs compartiments, ce qui rend le système non linéaire et couplé. Forme compartimentale du couplage… |
| `compartmentInitialSize` | Couche 3B | donnée | Nombre d'individus dans le compartiment au début de la simulation. |
| `compartmentSymbol` | Couche 3B | donnée | Symbole du compartiment dans les équations, par exemple S ou I. |
| `ConstantRate` | Couche 3B | classe | Taux qui ne dépend du contenu courant d'aucun compartiment. Déterminant individuel. « Constant » veut dire ici indépendant des compartiments, et non fixe dans… |
| `contactRatePerDay` | Couche 3A | donnée | Nombre moyen d'interactions de cette sorte par agent et par jour. |
| `ContextKnowledge` | 4-Context | classe | Deuxième composant du Quadruplet de recomposition (CK). Décrit où, pour qui et dans quelles conditions un modèle s'applique. |
| `CONTINUOUS` | Couche 2 | valeur | Le temps s'écoule continûment, exemple les équations différentielles. |
| `Country` | 4-Context | classe | Niveau administratif le plus haut. |
| `CoupledAgentBasedModel` | Couche 3A | **classe définie** | Modèle multi-agents comportant au moins une transition déclenchée par une interaction. Inféré par le raisonneur sans que personne ait déclaré le modèle… |
| `CoupledCompartmentalModel` | Couche 3B | **classe définie** | Modèle compartimental comportant au moins un flux couplé. Inféré par le raisonneur sans que personne ait déclaré le modèle infectieux. |
| `CoupledDiseaseKnowledge` | 4-Core | **classe définie** | Connaissance de maladie comportant au moins une transition couplée. Le raisonneur classe ici toute maladie dont une transition dépend de l'état de la… |
| `CoupledFlow` | Couche 3B | **classe définie** | Flux dont le taux dépend du contenu d'un compartiment. |
| `CoupledTransition` | 4-Core | **classe définie** | Transition d'état de santé gouvernée par au moins un déterminant couplé à la population. |
| `CouplingSource` | 4-Core | classe | Catégorie dont on peut lire l'effectif courant et dont la lecture peut faire varier un risque. Classe abstraite : on n'en crée jamais d'instance directe,… |
| `coverageRate` | 4-Core | donnée | Fraction de la population visée effectivement atteinte par l'intervention, entre 0 et 1. Pour une vaccination, c'est le taux de vaccination. |
| `creationDate` | Couche 2 | donnée | Date de création du modèle. |
| `CROSS_MODEL` | Couche 2 | valeur | Comparaison avec un modèle établi du même phénomène. |
| `defaultValue` | Couche 2 | donnée | Valeur utilisée lorsqu'aucune n'est fournie. |
| `dependsOnAttribute` | 4-Core | relation | Lie un déterminant aux attributs individuels qu'il lit. |
| `dependsOnCompartment` | Couche 3B | relation | Lie un taux aux compartiments dont il lit le contenu courant. Signature du couplage populationnel dans le paradigme compartimental. |
| `dependsOnCountIn` | 4-Core | relation | Lie un déterminant aux catégories dont il lit l'effectif courant. Signature du couplage populationnel. La catégorie lue est un état de santé lorsque le risque… |
| `DetectionIntervention` | 4-Core | classe | Intervention dont le but est de savoir si un individu a la maladie, et non de la soigner. Elle modifie un déterminant par l'intermédiaire de ce qu'elle… |
| `detects` | 4-Core | relation | Lie une intervention de détection à la connaissance de maladie qu'elle recherche. |
| `determinantExpression` | 4-Core | donnée | Expression textuelle du déterminant, par exemple beta * I / N. |
| `DETERMINISTIC` | Couche 2 | valeur | Les mêmes entrées donnent toujours les mêmes sorties. |
| `DiagnosisIntervention` | 4-Core | classe | Détection appliquée à un individu présentant déjà des signes de la maladie. C'est ce que fait la pratique clinique en l'absence de dépistage. |
| `DifferentialEquation` | Couche 3B | classe | Équation donnant la variation dans le temps du contenu d'un compartiment, comme bilan des flux qui y entrent et en sortent. |
| `DIRECT_CONTACT` | 4-Infectious | valeur | Par contact physique entre deux hôtes. |
| `DirectlyCoupledDeterminant` | 4-Infectious | **classe définie** | Classe DÉFINIE : déterminant dont la valeur se lit sur un effectif d'humains. Signature de la transmission interhumaine directe. Le raisonneur y classe la… |
| `DISCRETE` | Couche 2 | valeur | Le temps avance par pas ou par événements. |
| `DiseaseKnowledgeTemplate` | 4-Core | classe | Premier composant du Quadruplet de recomposition (DK). Connaissance structurée sur une maladie, indépendante de son type, du paradigme de modélisation et du… |
| `diseaseName` | 4-Core | donnée | Nom officiel de la maladie. |
| `District` | 4-Context | classe | Division administrative d'une région. |
| `DROPLET` | 4-Infectious | valeur | Par des gouttelettes respiratoires projetées à courte distance. |
| `DynamicParameter` | Couche 2 | classe | Paramètre dont la valeur varie dans le temps, par exemple un taux de transmission dépendant du temps. |
| `DYNAMICS_RESEARCH` | Couche 2 | valeur | Explorer les mecanismes de propagation des maladies, leurs dynamiques et les facteurs qui les influencent. Objectif de comprehension. |
| `EMPIRICAL` | Couche 2 | valeur | Modèle dit à boite noire, qui décrit les reponses du système par des équations ajustees sur des données experimentales, sans integrer de principe scientifique… |
| `endDate` | Couche 2 | donnée | Date de fin du scénario. |
| `EnvironmentallyMediatedDiseaseKnowledge` | 4-Infectious | **classe définie** | Classe DÉFINIE : maladie infectieuse dont la transmission passe par un effectif non humain. Le raisonneur l'infère à partir de la structure du modèle, SANS que… |
| `EnvironmentComponent` | Couche 2 | classe | Facteur externe ou contextuel influençant le système modélisé : météo, relief, infrastructure. |
| `EnvironmentModel` | Couche 3A | classe | Milieu dans lequel les agents se déplacent et se rencontrent. Sa nature spatiale est donnée par le type d'espace de la structure de modèle, en couche 2 et… |
| `EPIDEMIC_PLANNING` | Couche 2 | valeur | Anticiper et gerer des épidémies potentielles en testant des interventions et des strategies, comme les fermetures d'ecoles ou les campagnes de vaccination.… |
| `EpidemiologicalRole` | 4-Infectious | classe | Part qu'un organisme prend dans la transmission d'une maladie. |
| `equationExpression` | Couche 3B | donnée | Expression textuelle de l'équation, par exemple dS/dt = -beta * S * I / N. |
| `executesModel` | Couche 2 | relation | Lie une exécution au modèle qu'elle fait tourner. |
| `ExecutionKnowledge` | Couche 2 | classe | Comment exécuter le modèle : quel simulateur, combien de répétitions, avec quelle graine aléatoire. Quatrième composant du Quadruplet, à cote de la… |
| `executionStatus` | Couche 2 | donnée | État de l'exécution : en attente, en cours, terminée, échouée. |
| `ExponentialDistribution` | Couche 2 | classe | Loi du temps séparant deux événements survenant à taux constant. |
| `FECAL_ORAL` | 4-Infectious | valeur | Par ingestion de matières contaminées par des selles. |
| `FOODBORNE` | 4-Infectious | valeur | Par des aliments contaminés. |
| `FreeLivingStageState` | 4-Infectious | classe | Effectif d'un stade libre de l'agent pathogène présent dans un milieu, hors de tout hôte. Les cercaires dans l'eau, les miracidies. Sous l'hypothèse de… |
| `Fungus` | 4-Infectious | classe | Champignon pathogène. |
| `GammaDistribution` | Couche 2 | classe | Loi sur les valeurs positives, employée pour les coûts et les durées. |
| `GENERAL` | Couche 2 | valeur | Modèle employant des dynamiques generiques et des paramètres ajustables, qui permet de simuler un large eventail de maladies partageant des mecanismes… |
| `GeographicRegion` | 4-Context | classe | Territoire auquel un modèle s'applique. Quatre niveaux administratifs : pays, région, district, ville. |
| `GIS` | Couche 2 | valeur | L'espace est représenté par des données géographiques réelles. |
| `governsCompartment` | Couche 3B | relation | Lie une équation au compartiment dont elle donne la variation. |
| `GranularityLevel` | Couche 2 | **classe définie** | Niveau de détail auquel les entités modélisées sont décrites. Liste fermée. |
| `GREY_BOX` | Couche 2 | valeur | Modèle mêlant une part mecaniste et une part empirique : certains sous-systemes sont decrits par leurs mecanismes, d'autres par des relations ajustees sur les… |
| `GRID` | Couche 2 | valeur | L'espace est représenté par une grille régulière de cellules. |
| `GROUP` | Couche 2 | valeur | Les individus sont regroupés en groupes homogènes. |
| `hasAgentState` | Couche 3A | relation | Lie une catégorie d'agents aux états que ses agents peuvent occuper. |
| `hasAgentTransition` | Couche 3A | relation | Lie un modèle aux changements d'état que ses agents peuvent subir. |
| `hasAgentType` | Couche 3A | relation | Lie un modèle aux catégories d'agents qu'il contient. |
| `hasAuthor` | Couche 2 | donnée | Le nom de l'auteur du modèle est sous forme de texte et non en classe. |
| `hasBehavior` | Couche 3A | relation | Lie un modèle aux règles de comportement de ses agents. |
| `hasClimate` | 4-Context | relation | Lie un contexte à ses conditions climatiques. |
| `hasCompartment` | Couche 3B | relation | Lie un modèle compartimental à ses compartiments. |
| `hasComponent` | Couche 2 | relation | Lie une structure de modèle aux composants qu'elle contient. |
| `hasContextKnowledge` | 4-Context | relation | Lie un modèle au contexte pour lequel il a été construit. |
| `hasDiseaseCourseShape` | 4-Core | relation | Lie une connaissance de maladie à la forme dynamique de son cours, telle que classifiée par OGMS. Cette forme contraint la structure du modèle indépendamment… |
| `hasEndAge` | 4-Core | relation | Lie un état de santé au paramètre donnant l'âge au-delà duquel un individu n'y est plus. |
| `hasEnvironmentModel` | Couche 3A | relation | Lie un modèle au milieu dans lequel ses agents évoluent. |
| `hasEpidemiologicalRole` | 4-Infectious | relation | Lie une connaissance de maladie aux rôles intervenant dans son cycle de transmission. |
| `hasEquation` | Couche 3B | relation | Lie un modèle compartimental à ses équations différentielles. |
| `hasExecutionKnowledge` | Couche 2 | relation | Lie un modèle aux configurations d'exécution definies pour lui. Non fonctionnelle : un même modèle peut être exécuté sous plusieurs configurations, simulateurs… |
| `hasFlow` | Couche 3B | relation | Lie un modèle compartimental à ses flux. |
| `hasGeographicRegion` | 4-Context | relation | Lie un contexte aux territoires qu'il couvre. |
| `hasGranularityLevel` | Couche 2 | relation | Lie une structure de modèle à son niveau de détail. |
| `hasHealthInfrastructure` | 4-Context | relation | Lie un contexte aux structures de santé disponibles. |
| `hasHealthState` | 4-Core | relation | Lie une connaissance de maladie aux états de santé qu'elle définit. |
| `hasMaterialBasisIn` | 4-Core | relation | Lie une maladie au désordre qui en est la base physique. OGMS énonce cette relation dans la définition textuelle de la maladie, mais ne la formalise pas. IDO… |
| `hasModelNature` | Couche 2 | relation | Dit si le modèle est mecaniste, empirique ou mixte. Fonctionnelle. |
| `hasModelPurpose` | Couche 2 | relation | Lie un modèle aux objectifs pour lesquels il a été construit. Non fonctionnelle, délibérément : un même modèle peut servir à plusieurs choses, par exemple à… |
| `hasModelScope` | Couche 2 | relation | Dit si le modèle est général ou specifique. Fonctionnelle : un modèle est l'un ou l'autre, pas les deux. |
| `hasOnsetAge` | 4-Core | relation | Lie un état de santé au paramètre donnant l'âge à partir duquel un individu peut y entrer. |
| `hasParadigm` | Couche 2 | relation | Lie une structure de modèle à sa nature déterministe ou stochastique. |
| `hasParameter` | Couche 2 | relation | Lie un modèle à ses paramètres. |
| `hasPathogen` | 4-Infectious | relation | Lie une connaissance de maladie à l'agent pathogène qui la cause. |
| `hasPermanentImmunity` | 4-Infectious | donnée | Vrai lorsque l'immunité acquise après guérison dure toute la vie. |
| `hasPopulation` | 4-Context | relation | Lie un contexte aux populations qu'il concerne. |
| `hasRate` | Couche 3B | relation | Lie un flux à la façon dont son taux est déterminé. |
| `hasRefToDO` | 4-Core | donnée | Identifiant Disease Ontology. Rattache la taxonomie médicale, délibérément tenue HORS de la structure de l'ontologie. |
| `hasRefToICD` | 4-Core | donnée | Code CIM de la maladie. Reprend la convention d'OSDi pour faciliter l'alignement. |
| `hasRefToNCBITaxon` | 4-Infectious | donnée | Identifiant NCBI Taxonomy de l'agent pathogène. Rattache la taxonomie biologique, délibérément tenue hors de la structure de l'ontologie. |
| `hasRefToSNOMED` | 4-Core | donnée | Identifiant SNOMED CT de la maladie. Reprend la convention d'OSDi. |
| `hasReservoirState` | 4-Infectious | relation | Lie une connaissance de maladie aux états de réservoir qui interviennent dans sa transmission. Une maladie qui en déclare au moins un est classée transmission… |
| `hasRiskFactor` | 4-Core | relation | Lie une connaissance de maladie à ses facteurs de risque. |
| `hasSensitivity` | 4-Core | relation | Lie une intervention de détection au paramètre qui en donne la sensibilité : la part des individus atteints que le test trouve effectivement. Passer par un… |
| `hasSourceHealthState` | 4-Core | relation | État de santé de départ d'une transition. Distincte de hasSourceState de la couche 2, qui relie des composants de modèle et non des connaissances. |
| `hasSourceState` | Couche 2 | relation | État de départ d'une transition. |
| `hasSpatialType` | Couche 2 | relation | Lie une structure de modèle à son traitement de l'espace. |
| `hasSpecificity` | 4-Core | relation | Lie une intervention de détection au paramètre qui en donne la spécificité : la part des individus indemnes que le test écarte correctement. |
| `hasStateTransition` | 4-Core | relation | Lie une connaissance de maladie aux transitions qu'elle autorise. |
| `hasStructureKnowledge` | Couche 2 | relation | Lie un modèle à la connaissance décrivant sa structure interne. |
| `hasTargetHealthState` | 4-Core | relation | État de santé d'arrivée d'une transition. |
| `hasTargetState` | Couche 2 | relation | État d'arrivée d'une transition. |
| `hasTemporalType` | Couche 2 | relation | Lie une structure de modèle à son traitement du temps. |
| `hasTransmissionRoute` | 4-Infectious | relation | Lie une connaissance de maladie aux voies par lesquelles elle se transmet. |
| `hasUncertaintyDistribution` | Couche 2 | relation | Lie un paramètre à la loi de probabilité qui décrit l'incertitude sur sa valeur. C'est ce qui rend possible l'analyse de sensibilité probabiliste : au lieu… |
| `hasValidationMethod` | Couche 2 | relation | Lie un modèle aux méthodes par lesquelles il a été validé. |
| `HealthCentre` | 4-Context | classe | Structure de proximité assurant les soins primaires. |
| `HealthInfrastructure` | 4-Context | classe | Structures de santé disponibles dans le contexte. Détermine la capacité de réponse, et le seuil de saturation au-delà duquel la létalité augmente. |
| `HealthState` | 4-Core | classe | État qu'un individu peut occuper vis-à-vis d'une maladie. C'est une connaissance sur une phase du cours de la maladie et NON un composant de modèle : un… |
| `healthStateName` | 4-Core | donnée | Nom de l'état de santé. |
| `HealthStateTransition` | 4-Core | classe | Passage d'un individu d'un état de santé à un autre. Classe pivot du noyau : c'est le seul endroit où la structure du modèle est décidée, parce que c'est le… |
| `HISTORICAL_DATA` | Couche 2 | valeur | Comparaison des résultats avec des données réelles observées. |
| `Hospital` | 4-Context | classe | Structure disposant de lits, capable d'accueillir les cas graves. |
| `hospitalCapacity` | 4-Context | donnée | Nombre de lits disponibles. Fixe le seuil de saturation. |
| `HostRole` | 4-Infectious | classe | Organisme dans lequel l'agent pathogène se développe et qui subit la maladie. |
| `IAO_0000030` | Couche 1 | importé | *information content entity* — A generically dependent continuant that is about some thing. |
| `IAO_0000136` | Couche 1 | importé | *is about* — A (currently) primitive relation that relates an information artifact to an entity. |
| `incubationPeriodDays` | 4-Infectious | donnée | Durée moyenne entre l'infection et les premiers symptômes, en jours. |
| `IndirectlyCoupledDeterminant` | 4-Infectious | **classe définie** | Classe DÉFINIE : déterminant dont la valeur se lit sur un effectif non humain. Signature de la transmission médiée par un réservoir ou un milieu. Le raisonneur… |
| `INDIVIDUAL` | Couche 2 | valeur | Chaque individu est représenté séparément. |
| `IndividualAttribute` | 4-Core | classe | Caractéristique clinique ou démographique d'un individu dont la valeur peut modifier l'évolution de la maladie : âge, sexe, comorbidité, biomarqueur, statut… |
| `IndividualDeterminant` | 4-Core | classe | Déterminant dont la valeur ne dépend pas des autres individus. Il peut lire des attributs de l'individu concerné (âge, sexe, comorbidité, biomarqueur), ou… |
| `IndividualProgressionDiseaseKnowledge` | 4-Core | **classe définie** | Connaissance de maladie dont toutes les transitions sont individuelles. Modélisable par microsimulation, modèle multi-états ou arbre de décision. |
| `InfectiousDiseaseKnowledge` | 4-Infectious | **classe définie** | Connaissance d'une maladie causée par un agent pathogène. Classe DÉFINIE : toute connaissance de maladie déclarant un agent pathogène est classée ici par le… |
| `infectiousPeriodDays` | 4-Infectious | donnée | Durée moyenne pendant laquelle un hôte peut transmettre, en jours. |
| `initialAgentCount` | Couche 3A | donnée | Nombre d'agents de cette catégorie au début de la simulation. |
| `InitialCondition` | Couche 2 | classe | Paramètre donnant la valeur d'une grandeur au début de la simulation. |
| `interactionProbability` | Couche 3A | donnée | Probabilité que l'interaction entraîne la transition qu'elle déclenche. |
| `InteractionTriggeredTransition` | Couche 3A | **classe définie** | Transition déclenchée par une interaction avec d'autres agents, donc dépendant de leur état. Forme multi-agents du couplage populationnel. Classe définie : le… |
| `InteractionType` | Couche 3A | classe | Sorte de rencontre ou d'échange entre agents. |
| `IntermediateHostRole` | 4-Infectious | classe | Organisme dans lequel l'agent pathogène accomplit une étape de son cycle de vie avant d'atteindre son hôte final. L'escargot dans la schistosomiase. |
| `Intervention` | 4-Core | classe | Mesure de contrôle appliquée pendant la simulation, qui modifie le cours de la maladie en agissant sur au moins un déterminant. |
| `interventionEndDate` | 4-Core | donnée | Date de fin de l'intervention, ce qui permet de modéliser les interventions intermittentes. |
| `interventionIntensity` | 4-Core | donnée | Intensité de l'intervention, entre 0 et 1. 0 signifie aucun effet, 1 un effet maximal. |
| `InterventionScenario` | Couche 2 | classe | Scénario dans lequel une ou plusieurs interventions sont appliquées : vaccination, traitement, mesure de contrôle. |
| `interventionStartDate` | 4-Core | donnée | Date de début d'application de l'intervention. |
| `involvesAgentType` | Couche 3A | relation | Lie une sorte d'interaction aux catégories d'agents qui y participent. |
| `involvesFlow` | Couche 3B | relation | Lie une équation aux flux qui y figurent. |
| `isAbsorbingState` | 4-Core | donnée | Vrai lorsqu'aucune transition ne quitte cet état, par exemple le décès. |
| `isGovernedBy` | 4-Core | relation | Lie une transition aux déterminants qui en fixent le taux ou la probabilité. |
| `isLocatedInRegion` | 4-Context | relation | Lie une population au territoire où elle vit. |
| `Isolation` | 4-Infectious | classe | Mise à l'écart d'individus dont on sait qu'ils sont infectieux. |
| `isStateOfRole` | 4-Infectious | relation | Lie un état de réservoir au rôle épidémiologique dont il quantifie l'effectif : le rôle d'hôte intermédiaire pour les escargots infectés, le rôle de réservoir… |
| `isSubRegionOf` | 4-Context | relation | Lie un territoire au territoire plus large qui le contient. Transitive : un district dans une région dans un pays est dans ce pays. RO:located in n'est… |
| `lambdaParameter` | Couche 2 | donnée | Paramètre de taux d'une loi exponentielle, gamma ou de Poisson. |
| `latentPeriodDays` | 4-Infectious | donnée | Durée moyenne entre l'infection et le moment où l'hôte devient infectieux, en jours. Distincte de la période d'incubation : on peut transmettre avant d'avoir… |
| `lowerLimitParameter` | Couche 2 | donnée | Borne inférieure d'une loi uniforme. |
| `MaskWearing` | 4-Infectious | classe | Réduction de la probabilité de transmission lors d'un contact. |
| `meanParameter` | Couche 2 | donnée | Moyenne d'une loi normale. |
| `MECHANISTIC` | Couche 2 | valeur | Modèle dit à boite blanche, construit sur la connaissance du fonctionnement du système, de ses elements et de leurs interactions. Fournit des explications… |
| `medianAge` | 4-Context | donnée | Âge médian de la population, en années. |
| `METHODOLOGICAL_RESEARCH` | Couche 2 | valeur | Ameliorer les approches de modélisation elles-mêmes, pour les rendre plus efficaces, plus rapides ou plus robustes. Objectif de comprehension. |
| `MixedPopulation` | 4-Context | classe | Population mêlant zones urbaines et rurales au sein d'un même territoire. |
| `ModelComponent` | Couche 2 | classe | Partie constitutive de la structure d'un modèle. |
| `modelDescription` | Couche 2 | donnée | Description libre du modèle. |
| `modelName` | Couche 2 | donnée | Nom du modèle |
| `ModelNature` | Couche 2 | **classe définie** | Dit si le modèle explique les mecanismes ou se contente de reproduire les observations. Liste fermée. Ce critere decide de ce qui est recomposable : on ne… |
| `ModelParameter` | Couche 2 | classe | Grandeur nommée dont la valeur fixe une partie du comportement du modèle. Fusionne les anciennes classes ParameterComponent et ModelParameter. |
| `ModelPurpose` | Couche 2 | **classe définie** | Objectif pour lequel le modèle a été construit. Liste fermée. Connaitre l'objectif permet de juger si un modèle convient à une situation donnée, et… |
| `ModelScope` | Couche 2 | **classe définie** | Dit si le modèle est reglable pour plusieurs maladies ou construit pour une seule. Liste fermée. C'est le critere qui decide si un modèle est reutilisable… |
| `ModelStructureKnowledge` | Couche 2 | classe | Connaissance décrivant la structure interne d'un modèle : ses composants, et ses choix de traitement du hasard (déterministe ou stochastique), de temps,… |
| `modelVersion` | Couche 2 | donnée | Version du modèle. |
| `modifiesDeterminant` | 4-Core | relation | Lie une intervention aux déterminants dont elle modifie la valeur. C'est ce qui donne un sens formel à une intervention : sans cela, c'est une étiquette. |
| `MovementRestriction` | 4-Infectious | classe | Limitation des déplacements : confinement, couvre-feu, fermeture des frontières. |
| `MULTISCALE` | Couche 2 | valeur | Plusieurs niveaux de détail coexistent dans le même modèle. |
| `NETWORK` | Couche 2 | valeur | L'espace est représenté par un réseau de contacts ou de connexions. |
| `NON_SPATIAL` | Couche 2 | valeur | L'espace n'est pas représenté, la population est supposée bien mélangée. |
| `NonHumanHostState` | 4-Infectious | classe | Effectif d'organismes non humains se trouvant dans un état donné du cycle de l'agent pathogène. Les escargots infectés de la schistosomiase, les moustiques… |
| `NonPharmaceuticalIntervention` | 4-Core | classe | Intervention agissant sur le comportement ou la réglementation sans produit médical. |
| `NormalDistribution` | Couche 2 | classe | Loi symétrique caractérisée par une moyenne et un écart type. |
| `numberOfRuns` | Couche 2 | donnée | Nombre de répétitions de l'exécution, utile pour les modèles stochastiques. |
| `numberOfZones` | 4-Context | donnée | Nombre de sous-zones administratives. |
| `OGMS_0000030` | 4-OGMS | importé | *predisposition to disease of type X* — Une prédisposition chez un organisme qui constitue un risque accru pour cet organisme de développer ultérieurement la… |
| `OGMS_0000031` | 4-OGMS | importé | *disease* — Une prédisposition (i) à subir des processus pathologiques qui (ii) existe chez un organisme en raison d'un ou plusieurs troubles affectant cet… |
| `OGMS_0000045` | 4-OGMS | importé | *disorder* — Une entité matérielle cliniquement anormale et faisant partie d'un organisme étendu. Les troubles constituent le fondement physique de la maladie. |
| `OGMS_0000063` | 4-OGMS | importé | *disease course* — The totality of all processes through which a given disease instance is realized. |
| `OGMS_0000064` | 4-OGMS | importé | *chronic disease course* — A disease course that (a) does not terminate in a return to normal homeostasis and (b) would, absent intervention, fall within… |
| `OGMS_0000065` | 4-OGMS | importé | *progressive disease course* — A disease course that (a) does not terminate in a return to normal homeostasis and (b) would, absent intervention, involve an… |
| `OGMS_0000066` | 4-OGMS | importé | *transient disease course* — A disease course that terminates in a return to normal homeostasis. |
| `OGMS_0000084` | 4-OGMS | importé | *organism population* — Un regroupement d'organismes du même type. |
| `OGMS_0000087` | 4-OGMS | importé | *extended organism* — Un agrégat d'objets constitué d'un organisme et de toutes les entités matérielles situées à l'intérieur de l'organisme, chevauchant… |
| `OGMS_0000094` | 4-OGMS | importé | *acute disease course* — A disease course with an acute onset. |
| `ParadigmType` | Couche 2 | **classe définie** | Nature du traitement du hasard par le modèle : déterministe ou stochastique. Liste fermée. Malgré son nom, cette classe ne désigne pas le paradigme de… |
| `parameterName` | Couche 2 | donnée | Nom du paramètre, par exemple beta. |
| `parameterUnit` | Couche 2 | donnée | Unité du paramètre, par exemple jour^-1. |
| `parameterValue` | Couche 2 | donnée | Valeur numérique du paramètre. |
| `Parasite` | 4-Infectious | classe | Organisme vivant aux dépens d'un hôte, souvent avec un cycle de vie passant par plusieurs hôtes. |
| `Pathogen` | 4-Infectious | classe | Agent infectieux responsable de la maladie. |
| `pathogenName` | 4-Infectious | donnée | Nom scientifique de l'agent pathogène. |
| `PharmaceuticalIntervention` | 4-Core | classe | Intervention reposant sur un produit médical : vaccin, antiviral, antibiotique. |
| `PoissonDistribution` | Couche 2 | classe | Loi du nombre d'événements survenant dans un intervalle fixe. |
| `Population` | 4-Context | classe | Groupe d'individus dans un contexte géographique. Alignement partiel avec osdi:Population, qui décrit une cohorte clinique par âge, sexe, espérance de vie et… |
| `PopulationCoupledDeterminant` | 4-Core | classe | Déterminant dont la valeur dépend du nombre d'individus se trouvant actuellement dans une catégorie donnée, humaine ou non. Exemple canonique : la force… |
| `populationDensity` | 4-Context | donnée | Densité en habitants par kilomètre carré. |
| `populationSize` | 4-Context | donnée | Effectif de la population. |
| `ProbabilityDistribution` | Couche 2 | classe | Loi de probabilité caractérisant l'incertitude d'un paramètre, ou le tirage aléatoire d'une valeur. |
| `probabilityParameter` | Couche 2 | donnée | Probabilité de succès d'une loi de Bernoulli, entre 0 et 1. |
| `producesResult` | Couche 2 | relation | Lie une exécution aux données qu'elle produit. |
| `ProgressiveCourseDiseaseKnowledge` | 4-Core | **classe définie** | Maladie à déviation croissante. Impose une progression ordonnée par stades, sans retour. |
| `quantifiedBy` | 4-Core | relation | Lie un déterminant au paramètre qui lui donne sa valeur : beta, gamma, un rapport de risque. |
| `Quarantine` | 4-Infectious | classe | Mise à l'écart d'individus possiblement exposés, pour les empêcher de transmettre. |
| `randomSeed` | Couche 2 | donnée | Graine du générateur aléatoire, nécessaire pour reproduire une exécution stochastique. |
| `rateConstantValue` | Couche 3B | donnée | Valeur d'un taux constant, par jour. |
| `rateExpression` | Couche 3B | donnée | Expression textuelle du taux, par exemple beta * I / N. |
| `RateSpecification` | Couche 3B | classe | Façon dont le taux d'un flux est déterminé. |
| `realisesDeterminant` | 4-Core | relation | Déclare quel déterminant un composant de modèle réalise : un taux dépendant d'un compartiment [3B] ou une transition déclenchée par une interaction [3A]… |
| `REGIONAL` | Couche 2 | valeur | L'unité décrite est un territoire. |
| `regionName` | 4-Context | donnée | Nom officiel du territoire. |
| `reinfectionPossible` | 4-Infectious | donnée | Vrai lorsqu'un hôte guéri peut être infecté à nouveau. |
| `representsDisease` | 4-Core | relation | Lie un artefact de connaissance de maladie à la maladie réelle dont il parle, c'est-à-dire une disposition portée par un organisme. Unique point de contact… |
| `representsHealthState` | 4-Core | relation | Déclare quel état de santé un composant d'état de modèle représente. Un compartiment S et un état d'agent susceptible utilisent tous deux cette même propriété. |
| `representsPhaseOf` | 4-Core | relation | Lie un état de santé à la phase du cours de maladie qu'il représente. Un état de santé n'est pas une phase réelle : c'est une abstraction de modélisation qui… |
| `representsStateTransition` | 4-Core | relation | Déclare quelle transition d'état de santé un composant de transition de modèle représente. |
| `ReservoirRole` | 4-Infectious | classe | Organisme ou milieu où l'agent pathogène persiste entre deux épidémies. |
| `ReservoirState` | 4-Infectious | classe | Catégorie non humaine dont l'effectif courant peut faire varier un risque : escargots infectés, cercaires présentes dans un point d'eau, moustiques infectieux.… |
| `RETROSPECTIVE_ANALYSIS` | Couche 2 | valeur | Etudier une epidemie passee pour evaluer l'efficacite des reponses et preparer les interventions futures. Objectif de prediction. |
| `RiskFactor` | 4-Core | classe | Élément augmentant la probabilité d'une transition. Peut être un attribut individuel, un élément de contexte ou une exposition. |
| `RO_0000057` | Couche 1 | importé | *has participant* — a relation between a process and a continuant, in which the continuant is somehow involved in the process. |
| `RO_0002131` | Couche 1 | importé | *overlaps* — A overlaps B if they share some part in common. x overlaps y if and only if there exists some z such that x has part z and z part of y |
| `RO_0002233` | Couche 1 | importé | *has input* — p has input c iff: p is a process, c is a material entity, c is a participant in p, c is present at the start of p, and the state of c is… |
| `RO_0002234` | Couche 1 | importé | *has output* — p has output c iff c is a participant in p, c is present at the end of p, and c is not present in the same state at the beginning of p. |
| `RO_0002323` | Couche 1 | importé | *mereotopologically related to* — A mereological relationship or a topological relationship |
| `RuleComponent` | Couche 2 | classe | Règle gouvernant le comportement du modèle : règle de décision, de comportement, d'interaction. |
| `RuralPopulation` | 4-Context | classe | Population vivant majoritairement en zone rurale, à faible densité et à contacts moins fréquents. |
| `scenarioDurationInDays` | Couche 2 | donnée | Durée couverte par le scénario en jours |
| `SchoolClosure` | 4-Infectious | classe | Fermeture des établissements scolaires. |
| `ScreeningIntervention` | 4-Core | classe | Détection appliquée à une population entière, y compris aux individus ne présentant aucun signe de la maladie. Le dépistage néonatal en est le cas type. |
| `SEXUAL` | 4-Infectious | valeur | Par contact sexuel. |
| `simulationDurationInDays` | Couche 2 | donnée | Durée totale simulée en jours |
| `SimulationExecution` | Couche 2 | classe | Ceci représente le processus d'exécution d'un modèle de simulation sur un simulateur. Ce n'est pas un artefact d'information mais un processus car il se… |
| `SimulationKnowledgeArtifact` | Couche 2 | classe | Artefact d'information portant une connaissance utilisée pour construire, décrire ou exécuter un modèle de simulation. |
| `SimulationModel` | Couche 2 | classe | Représentation d'un système dont on étudie le comportement par simulation, indépendamment du paradigme employé. |
| `SimulationObservation` | Couche 2 | classe | Données réelles observées, servant à valider un modèle par comparaison avec ses résultats. |
| `SimulationResult` | Couche 2 | classe | Données produites par une exécution de simulation. |
| `SimulationScenario` | Couche 2 | classe | Ensemble d'hypothèses et de réglages sous lesquels un modèle est exécuté. |
| `simulatorName` | Couche 2 | donnée | Nom du simulateur employé, par exemple JaDES, GAMA, NetLogo. |
| `simulatorVersion` | Couche 2 | donnée | Version du simulateur employé. |
| `SocialDistancing` | 4-Infectious | classe | Réduction des contacts rapprochés dans l'ensemble de la population. |
| `SpatialType` | Couche 2 | **classe définie** | Façon dont l'espace est représenté dans le modèle. Liste fermée. |
| `SPECIFIC` | Couche 2 | valeur | Modèle integrant les mecanismes de transmission et les facteurs propres à une maladie precise, souvent dans un contexte donne. Demande des données precises et… |
| `standardDeviationParameter` | Couche 2 | donnée | Écart type d'une loi normale |
| `startDate` | Couche 2 | donnée | Date de début du scénario. |
| `StateComponent` | Couche 2 | classe | État qu'une entité du modèle peut occuper à un instant donné. Se spécialise en compartiment pour les modèles compartimentaux [C3B] et en état d'agent pour les… |
| `StaticApproximationAgentTransition` | 4-Checks | **classe définie** | Transition d'agent qui représente une transition couplée, mais qui est déclenchée par les seuls attributs de l'agent, et non par une interaction. Forme… |
| `StaticApproximationFlow` | 4-Checks | **classe définie** | Flux qui représente une transition couplée, mais dont le taux est constant : il ne lit pas l'effectif dont dépend le risque. Forme compartimentale de… |
| `StaticApproximationModel` | 4-Checks | **classe définie** | Modèle comportant au moins une approximation statique : il représente une transition couplée sans en réaliser le couplage. Il ignore donc les effets indirects… |
| `StaticParameter` | Couche 2 | classe | Paramètre dont la valeur ne change pas au cours de la simulation. |
| `STATISTICAL` | Couche 2 | valeur | Test statistique de l'accord entre les résultats et des données de référence. |
| `STOCHASTIC` | Couche 2 | valeur | Le hasard intervient et les résultats varient d'une exécution à l'autre. |
| `supersedesHealthState` | 4-Core | relation | Ordre de progression entre états de santé, lorsqu'il en existe un. |
| `TemperateClimate` | 4-Context | classe | Climat à saisons marquées et températures modérées. |
| `TemporalType` | Couche 2 | **classe définie** | Nature du temps dans le modèle. Liste fermée. |
| `timeStepInDays` | Couche 2 | donnée | Durée d'un pas de simulation en jours |
| `TransientCourseDiseaseKnowledge` | 4-Core | **classe définie** | Maladie dont le cours peut se terminer par un retour à l'homéostasie normale. Autorise une transition de retour vers un état sain. |
| `TransitionComponent` | Couche 2 | classe | Passage d'un état à un autre. Possède exactement un état de départ et un état d'arrivée, quel que soit le paradigme. Une transition vers plusieurs états se… |
| `TransitionDeterminant` | 4-Core | **classe définie** | Ce qui gouverne le taux ou la probabilité d'une transition. La distinction entre ses deux sous-classes N'EST PAS médicale mais structurelle : elle dit si le… |
| `TransitionFlow` | Couche 3B | classe | Passage d'individus d'un compartiment à un autre, gouverné par un taux. Hérite de la transition de couche 2 ses états de départ et d'arrivée. |
| `TransmissionReducingIntervention` | 4-Infectious | **classe définie** | Classe DÉFINIE : intervention agissant sur un déterminant couplé à la population. N'a de sens que pour une maladie transmissible, puisque réduire les contacts… |
| `TransmissionRoute` | 4-Infectious | **classe définie** | Voie biologique par laquelle une maladie transmissible passe d'un hôte à un autre. Liste fermée. |
| `transmittedThroughRole` | 4-Infectious | relation | Lie une voie de transmission au rôle par lequel elle passe, lorsqu'elle passe par un organisme vivant ou un milieu. |
| `Treatment` | 4-Core | classe | Traitement médicamenteux des individus atteints. Agit en général sur un déterminant individuel : il modifie la guérison ou la progression de l'individu traité. |
| `triggeredBy` | Couche 3A | relation | Lie une transition à la sorte d'interaction qui la déclenche. Signature du couplage populationnel dans le paradigme multi-agents. |
| `TropicalClimate` | 4-Context | classe | Climat chaud et humide, favorable à de nombreux vecteurs. |
| `UniformDistribution` | Couche 2 | classe | Loi donnant le même poids à toutes les valeurs entre deux bornes. |
| `upperLimitParameter` | Couche 2 | donnée | Borne supérieure d'une loi uniforme. |
| `UrbanPopulation` | 4-Context | classe | Population vivant majoritairement en ville, à forte densité et à contacts fréquents. |
| `usesScenario` | Couche 2 | relation | Lie un modèle aux scénarios sous lesquels il est exécuté. |
| `Vaccination` | 4-Core | classe | Campagne faisant passer des individus d'un état susceptible à un état protégé. |
| `VaccinationCentre` | 4-Context | classe | Structure dédiée à l'administration des vaccins. |
| `ValidationMethod` | Couche 2 | **classe définie** | Méthode par laquelle on montre que le modèle convient à son objectif. Liste fermée. |
| `VECTOR_BORNE` | 4-Infectious | valeur | Par un vecteur vivant, le plus souvent un arthropode. Voie du paludisme et de la dengue. |
| `VectorRole` | 4-Infectious | classe | Organisme transportant l'agent pathogène d'un hôte à un autre sans subir la maladie. |
| `VERTICAL` | 4-Infectious | valeur | De la mère à l'enfant, pendant la grossesse, l'accouchement ou l'allaitement. |
| `Virus` | 4-Infectious | classe | Agent pathogène acellulaire, qui ne se réplique qu'à l'intérieur d'une cellule hôte. |
| `WATERBORNE` | 4-Infectious | valeur | Par de l'eau contaminée. Voie de la schistosomiase et du choléra. |
