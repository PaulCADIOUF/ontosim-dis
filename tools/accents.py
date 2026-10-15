#!/usr/bin/env python3
"""
accents.py : rétablit les accents dans les textes français (@fr) d'OntoSim-Dis.

À lancer depuis Git Bash, à la racine du dépôt :

    python tools/accents.py              simulation : écrit accents_rapport.txt, ne modifie rien
    python tools/accents.py --appliquer  corrige les fichiers de src/ontology

Le script ne touche que le contenu des textes marqués @fr. Les IRI, les noms des termes
et les textes anglais ou espagnols restent tels quels. Avant d'écrire un fichier, il vérifie
avec rdflib que le fichier corrigé contient les mêmes triplets, à ces textes près.

Le dictionnaire a été établi pour les textes actuels de l'ontologie, en lisant chaque mot
ambigu dans son contexte. Un texte écrit plus tard doit être accentué à la main.
"""
import glob
import os
import re
import sys
import unicodedata

# ---------------------------------------------------------------------------------------
# 1. Mots corrigés partout : forme sans accent -> forme correcte.
#    La majuscule et les capitales sont conservées : Etat -> État, DEFINIE -> DÉFINIE.
# ---------------------------------------------------------------------------------------
MOTS = {
    "age": "âge", "aleatoire": "aléatoire", "annees": "années", "appliquee": "appliquée",
    "appliquees": "appliquées", "appreciation": "appréciation", "apres": "après", "arrivee": "arrivée",
    "capacite": "capacité", "caracterisant": "caractérisant", "caracterisee": "caractérisée", "caracteristique": "caractéristique",
    "caracteristiques": "caractéristiques", "carre": "carré", "categorie": "catégorie", "categories": "catégories",
    "causee": "causée", "cholera": "choléra", "classee": "classée", "classifiee": "classifiée",
    "comorbidite": "comorbidité", "comptee": "comptée", "comptes": "comptés", "consequence": "conséquence",
    "contaminee": "contaminée", "contaminees": "contaminées", "contamines": "contaminés", "continument": "continûment",
    "controle": "contrôle", "cotes": "côtés", "couple": "couplé", "couplee": "couplée",
    "couts": "coûts", "creation": "création", "cree": "crée", "debut": "début",
    "deces": "décès", "decidee": "décidée", "decision": "décision", "declarant": "déclarant",
    "declarons": "déclarons", "declenche": "déclenche", "declenchee": "déclenchée", "decrire": "décrire",
    "decrit": "décrit", "decrite": "décrite", "decrites": "décrites", "decrivant": "décrivant",
    "dediee": "dédiée", "definie": "définie", "definit": "définit", "definition": "définition",
    "degres": "degrés", "deja": "déjà", "dela": "delà", "deliberement": "délibérément",
    "demographique": "démographique", "densite": "densité", "depart": "départ", "depend": "dépend",
    "dependant": "dépendant", "dependre": "dépendre", "depens": "dépens", "depistage": "dépistage",
    "deplacements": "déplacements", "deplacent": "déplacent", "depourvu": "dépourvu", "deroule": "déroule",
    "desordre": "désordre", "detail": "détail", "detecte": "détecté", "detection": "détection",
    "determinant": "déterminant", "determinantes": "déterminantes", "determinants": "déterminants", "deterministe": "déterministe",
    "deuxieme": "deuxième", "developpe": "développe", "deviation": "déviation", "differentielles": "différentielles",
    "documente": "documenté", "donnee": "donnée", "donnees": "données", "duree": "durée",
    "durees": "durées", "ecart": "écart", "ecarte": "écarte", "echange": "échange",
    "echouee": "échouée", "ecoule": "écoule", "element": "élément", "emerger": "émerger",
    "empecher": "empêcher", "employe": "employé", "employee": "employée", "enonce": "énonce",
    "entiere": "entière", "entierement": "entièrement", "entite": "entité", "entites": "entités",
    "entraine": "entraîne", "entree": "entrée", "entrees": "entrées", "epidemies": "épidémies",
    "epidemiologique": "épidémiologique", "epidemiologiques": "épidémiologiques", "equation": "équation", "equations": "équations",
    "equilibre": "équilibre", "esperance": "espérance", "etabli": "établi", "etablissements": "établissements",
    "etait": "était", "etape": "étape", "etat": "état", "etats": "états",
    "ete": "été", "etiquette": "étiquette", "etre": "être", "etudie": "étudie",
    "evaluation": "évaluation", "evenements": "événements", "evoluent": "évoluent", "evolution": "évolution",
    "execute": "exécuté", "executer": "exécuter", "execution": "exécution", "exposes": "exposés",
    "exquations": "équations", "facon": "façon", "fermee": "fermée", "frequents": "fréquents",
    "frontieres": "frontières", "generale": "générale", "generateur": "générateur", "generique": "générique",
    "geographique": "géographique", "geographiques": "géographiques", "gouvernee": "gouvernée", "gouvernes": "gouvernés",
    "gueri": "guéri", "guerison": "guérison", "herite": "hérite", "hierarchie": "hiérarchie",
    "homeostasie": "homéostasie", "homogenes": "homogènes", "hote": "hôte", "hotes": "hôtes",
    "humidite": "humidité", "hypothese": "hypothèse", "hypotheses": "hypothèses", "immunite": "immunité",
    "independamment": "indépendamment", "independant": "indépendant", "independante": "indépendante", "independantes": "indépendantes",
    "independants": "indépendants", "infecte": "infecté", "infectes": "infectés", "inferieure": "inférieure",
    "influencant": "influençant", "intensite": "intensité", "interieur": "intérieur", "intermediaire": "intermédiaire",
    "isole": "isolé", "kilometre": "kilomètre", "letale": "létale", "letalite": "létalité",
    "lineaire": "linéaire", "localite": "localité", "maniere": "manière", "marquees": "marquées",
    "materielles": "matérielles", "mathematique": "mathématique", "matieres": "matières", "median": "médian",
    "medicale": "médicale", "medicamenteux": "médicamenteux", "mediee": "médiée", "melangee": "mélangée",
    "melant": "mêlant", "meme": "même", "memes": "mêmes", "menage": "ménage",
    "menages": "ménages", "mere": "mère", "meteo": "météo", "methode": "méthode",
    "methodes": "méthodes", "modele": "modèle", "modeles": "modèles", "modelisable": "modélisable",
    "modelisation": "modélisation", "modelisees": "modélisées", "modeliser": "modéliser", "moderees": "modérées",
    "necessaire": "nécessaire", "neonatal": "néonatal", "nommee": "nommée", "numerique": "numérique",
    "observees": "observées", "ordonnee": "ordonnée", "parametre": "paramètre", "parametres": "paramètres",
    "pathogene": "pathogène", "periode": "période", "periodes": "périodes", "phenomene": "phénomène",
    "plutot": "plutôt", "portee": "portée", "possede": "possède", "precipitations": "précipitations",
    "premiere": "première", "present": "présent", "presentant": "présentant", "presentes": "présentes",
    "probabilite": "probabilité", "probabilites": "probabilités", "projetees": "projetées", "propriete": "propriété",
    "protege": "protégé", "proximite": "proximité", "quatrieme": "quatrième", "rapproches": "rapprochés",
    "realise": "réalise", "realisent": "réalisent", "realiste": "réaliste", "reduction": "réduction",
    "reduire": "réduire", "reelle": "réelle", "reelles": "réelles", "reference": "référence",
    "region": "région", "regions": "régions", "reglages": "réglages", "regle": "règle",
    "reglementation": "réglementation", "regles": "règles", "regroupes": "regroupés", "reguliere": "régulière",
    "repetee": "répétée", "repetition": "répétition", "repetitions": "répétitions", "replique": "réplique",
    "repond": "répond", "reponse": "réponse", "representable": "représentable", "representation": "représentation",
    "representent": "représentent", "reseau": "réseau", "reservoir": "réservoir", "resultats": "résultats",
    "reutilisee": "réutilisée", "reutilises": "réutilisés", "role": "rôle", "roles": "rôles",
    "sante": "santé", "scenario": "scénario", "scenarios": "scénarios", "senegal": "sénégal",
    "sensibilite": "sensibilité", "separant": "séparant", "separement": "séparément", "separer": "séparer",
    "simulee": "simulée", "situee": "située", "specialise": "spécialise", "specificite": "spécificité",
    "structuree": "structurée", "succes": "succès", "superieure": "supérieure", "supposee": "supposée",
    "symetrique": "symétrique", "symptomes": "symptômes", "systeme": "système", "temperature": "température",
    "temperatures": "températures", "terminee": "terminée", "theorie": "théorie", "tiree": "tirée",
    "traite": "traité", "transitivite": "transitivité", "unite": "unité", "utilisee": "utilisée",
    "visee": "visée", "zero": "zéro",
}

# ---------------------------------------------------------------------------------------
# 2. Mots dont la forme dépend du contexte. Les règles ont été écrites en lisant chacune
#    de leurs occurrences dans les textes actuels.
#    mot, avant, apres : en minuscules et sans accents (avant et apres sont les mots voisins) ;
#    elision : le mot élidé juste avant (« n' », « d' », « l' »...) ; debut : le mot ouvre le texte.
# ---------------------------------------------------------------------------------------
AMBIGUS = {"a", "ou", "declare", "represente", "determine", "modelise", "infere", "donne",
           "passe", "valide", "exprime", "gouverne", "beta", "general", "medical"}


def selon_contexte(mot, avant, apres, elision, debut):
    if mot == "a":                       # « il a » (avoir) ou « à » (préposition)
        if elision == "n'" or avant in ("il", "elle", "on", "y", "individu"):
            return "a"
        return "à"
    if mot == "ou":                      # « ou » (ou bien) ou « où » (lieu, moment)
        if debut or elision == "d'":
            return "où"
        if avant in ("decrit", "territoire", "endroit", "moment", "hydrique"):
            return "où"
        if avant == "milieu" and apres == "l":
            return "où"
        return "ou"
    if mot == "declare":                 # « qu'on ait déclaré » / « Déclare quel... »
        return "déclaré" if avant == "ait" else "déclare"
    if mot == "represente":              # « est représenté par » / « qu'il représente »
        return "représenté" if avant in ("est", "pas") else "représente"
    if mot == "determine":               # « son taux est déterminé » / « qui détermine »
        return "déterminé" if avant == "est" else "détermine"
    if mot == "modelise":                # « le système modélisé » / « dont on modélise »
        return "modélise" if avant == "on" else "modélisé"
    if mot == "infere":                  # « Inféré par le raisonneur » / « le raisonneur l'infère »
        return "infère" if elision == "l'" else "inféré"
    if mot == "donne":                   # « à un instant donné » / « qui en donne »
        return "donné" if avant in ("instant", "etat") else "donne"
    if mot == "passe":                   # « le temps passé » / « elle passe par »
        return "passé" if avant == "temps" else "passe"
    if mot == "valide":                  # « il a été validé »
        return "validé" if avant == "ete" else "valide"
    if mot == "exprime":                 # « ils sont exprimés »
        return "exprimés" if avant == "sont" else "exprime"
    if mot == "gouverne":                # « gouverné par un taux » / « qui gouverne »
        return "gouverné" if apres == "par" else "gouverne"
    if mot == "beta":                    # « loi bêta », mais beta le paramètre : beta * I / N
        return "bêta" if avant == "loi" else "beta"
    if mot == "general":                 # nom anglais : Ontology for General Medical Science
        return "general" if apres == "medical" else "général"
    if mot == "medical":
        return "medical" if avant == "general" else "médical"
    return None


# ---------------------------------------------------------------------------------------
# 3. Cinq phrases reformulées en entier, parce qu'elles contenaient aussi des fautes :
#    texte d'origine exact -> nouveau texte. Une phrase déjà modifiée n'est pas trouvée,
#    et le rapport le signale.
# ---------------------------------------------------------------------------------------
PHRASES = {
    "Couche 2 :Cette couche repond à la question comment modeliser ?\n"
    "Nous yi avons les concepts generique de simulation, ces concepts sont communs a tous "
    "les paradigmes de modelisation et independants de tout domaine medical.":
    "Couche 2 : cette couche répond à la question « comment modéliser ? ».\n"
    "Elle rassemble les concepts génériques de simulation, communs à tous les paradigmes "
    "de modélisation et indépendants de tout domaine médical.",

    "Les caracteristiques principales du systeme multi-agents est qu'il n'y a pas d'ordre "
    "centralisé ce qui fait que chaque agent prend des décisions et agit seul. Les agents "
    "aussi communiquent et réagissent aux actions des autres et de leur environnement.\n"
    "D'ou la possibilité de voir emerger un comportement collectif inattendu.\n"
    "Cette couche est générale donc ne contient aucun contenu medical.":
    "La caractéristique principale d'un système multi-agents est l'absence de contrôle "
    "centralisé : chaque agent prend ses décisions et agit seul. Les agents communiquent "
    "aussi entre eux, et réagissent aux actions des autres et à leur environnement.\n"
    "D'où la possibilité de voir émerger un comportement collectif inattendu.\n"
    "Cette couche est générale : elle ne contient aucun contenu médical.",

    "Pour ce type de modele, nous divisons la population en compartiments et les flux "
    "entre ces compartiments sont gouvernes par des taux.\n"
    "Pour la plupart du temps ils sont exprime en exquations differentielles.\n"
    "Rappel : Cette couche ne contient aucun contenu medical":
    "Pour ce type de modèle, nous divisons la population en compartiments, et les flux "
    "entre ces compartiments sont gouvernés par des taux.\n"
    "La plupart du temps, ils sont exprimés en équations différentielles.\n"
    "Rappel : cette couche ne contient aucun contenu médical.",

    "Couche 1 de l'ontologie OntoSim-Dis. les concepts fondateurs indépendants de tout "
    "domaine applicatif. Les termes nécessaires de BFO, RO et IAO ont été extraits selon "
    "une approche MIREOT.":
    "Couche 1 de l'ontologie OntoSim-Dis : les concepts fondateurs, indépendants de tout "
    "domaine applicatif. Les termes nécessaires de BFO, RO et IAO ont été extraits selon "
    "la méthode MIREOT.",

    "Lie une maladie au desordre qui en est la base physique. OGMS enonce cette relation "
    "dans la definition textuelle de la maladie mais ne la formalise pas. IDO la formalise "
    "sous son propre IRI. nous la declarons ici pour ne pas dependre d'IDO.":
    "Lie une maladie au désordre qui en est la base physique. OGMS énonce cette relation "
    "dans la définition textuelle de la maladie, mais ne la formalise pas. IDO la formalise "
    "sous son propre IRI ; nous la déclarons ici pour ne pas dépendre d'IDO.",
}

# ---------------------------------------------------------------------------------------
# Lecture des textes d'un fichier Turtle
# ---------------------------------------------------------------------------------------
LITTERAL = re.compile(r'("""(?:[^"\\]|\\.|"(?!""))*"""|"(?:[^"\\\n]|\\.)*")(@[A-Za-z-]+|\^\^\S+)?', re.S)
MOT = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿŒœ]+")


def litteraux(texte):
    """Renvoie (début, fin, contenu, étiquette) pour chaque texte entre guillemets du fichier."""
    i, n, trouves = 0, len(texte), []
    while i < n:
        c = texte[i]
        if c == "#":                                  # commentaire jusqu'à la fin de la ligne
            j = texte.find("\n", i)
            i = n if j < 0 else j + 1
        elif c == "<":                                # IRI
            i = texte.find(">", i) + 1
        elif c == '"':
            m = LITTERAL.match(texte, i)
            brut, etiquette = m.group(1), m.group(2) or ""
            q = 3 if brut.startswith('"""') else 1
            trouves.append((m.start(1) + q, m.end(1) - q, brut[q:-q], etiquette))
            i = m.end()
        else:
            i += 1
    return trouves


def sans_accents(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def meme_casse(source, cible):
    if len(source) > 1 and source.isupper():
        return cible.upper()
    if source[0].isupper():
        return cible[0].upper() + cible[1:]
    return cible


def est_identifiant(contenu, m):
    """Vrai pour un morceau de nom de terme : dsim:Truc, camelCase, 3A, OBI_0000278."""
    a = contenu[m.start() - 1] if m.start() > 0 else " "
    b = contenu[m.end()] if m.end() < len(contenu) else " "
    if a.isdigit() or b.isdigit() or a in "_:" or b in "_:":
        return True
    return re.search(r"[a-z][A-Z]", m.group(0)) is not None


def corriger(contenu):
    """Corrige un texte @fr. Renvoie (nouveau texte, liste des corrections)."""
    normalise = contenu.replace("\r\n", "\n")
    if normalise in PHRASES:
        nouveau = PHRASES[normalise]
        if "\r\n" in contenu:
            nouveau = nouveau.replace("\n", "\r\n")
        return nouveau, [("phrase", contenu, nouveau, "")]
    mots = [m for m in MOT.finditer(contenu) if not est_identifiant(contenu, m)]
    simples = [sans_accents(m.group(0)).lower() for m in mots]
    corrections, morceaux, dernier = [], [], 0
    for k, m in enumerate(mots):
        w = m.group(0)
        if not w.isascii():
            continue
        lw = simples[k]
        nouveau = None
        if lw in AMBIGUS:
            avant = simples[k - 1] if k > 0 else ""
            apres = simples[k + 1] if k + 1 < len(mots) else ""
            elision = ""
            if m.start() >= 2 and contenu[m.start() - 1] in "'’":
                elision = sans_accents(mots[k - 1].group(0)).lower() + "'" if k > 0 else ""
            debut = contenu[:m.start()].strip() == ""
            nouveau = selon_contexte(lw, avant, apres, elision, debut)
            genre = "contexte"
        elif lw in MOTS:
            nouveau = MOTS[lw]
            genre = "mot"
        if nouveau is None:
            continue
        nouveau = meme_casse(w, nouveau)
        extrait = (contenu[max(0, m.start() - 40):m.start()] + "[" + nouveau + "]"
                   + contenu[m.end():m.end() + 40]).replace("\r", "").replace("\n", " / ")
        if nouveau != w or lw == "a":
            corrections.append((genre, w, nouveau, extrait))
        if nouveau != w:
            morceaux.append(contenu[dernier:m.start()])
            morceaux.append(nouveau)
            dernier = m.end()
    morceaux.append(contenu[dernier:])
    return "".join(morceaux), corrections


def meme_graphe(ancien, nouveau, chemin):
    """Vérifie avec rdflib que seuls des textes @fr ont changé. Renvoie un message d'erreur, ou ''."""
    try:
        from rdflib import Graph, Literal
        from rdflib.compare import isomorphic
    except ImportError:
        return ""
    graphes = []
    for texte in (ancien, nouveau):
        g = Graph().parse(data=texte, format="turtle")
        h = Graph()
        for s, p, o in g:
            if isinstance(o, Literal) and o.language == "fr":
                o = Literal("texte français", lang="fr")
            h.add((s, p, o))
        graphes.append((len(g), h))
    if graphes[0][0] != graphes[1][0] or not isomorphic(graphes[0][1], graphes[1][1]):
        return "le fichier corrigé ne contient pas les mêmes triplets"
    return ""


def main():
    appliquer = "--appliquer" in sys.argv[1:]
    try:
        sys.stdout.reconfigure(errors="replace")
    except AttributeError:
        pass
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    fichiers = sorted(glob.glob("src/ontology/*.ttl"))
    if not fichiers:
        print("Aucun fichier dans src/ontology : lance le script depuis la racine du dépôt.")
        return 1

    par_mot, contexte, phrases, resume = {}, [], [], []
    a_ecrire, erreurs = {}, []
    total_textes = textes_sans_accent = 0
    for chemin in fichiers:
        with open(chemin, encoding="utf-8", newline="") as f:
            ancien = f.read()
        morceaux, dernier, n = [], 0, 0
        for debut, fin, contenu, etiquette in litteraux(ancien):
            if etiquette.lower() != "@fr":
                continue
            total_textes += 1
            if not re.search(r"[À-ÿ]", contenu):
                textes_sans_accent += 1
            nouveau, corrections = corriger(contenu)
            for genre, avant, apres, extrait in corrections:
                nom = os.path.basename(chemin)
                if genre == "mot":
                    cle = (avant.lower(), apres.lower())
                    par_mot[cle] = par_mot.get(cle, 0) + 1
                elif genre == "contexte":
                    contexte.append((nom, avant, apres, extrait))
                else:
                    phrases.append((nom, avant, apres))
                if avant != apres:
                    n += 1
            morceaux.append(ancien[dernier:debut])
            morceaux.append(nouveau)
            dernier = fin
        morceaux.append(ancien[dernier:])
        nouveau_fichier = "".join(morceaux)
        resume.append((os.path.basename(chemin), n))
        if nouveau_fichier != ancien:
            probleme = meme_graphe(ancien, nouveau_fichier, os.path.abspath(chemin))
            if probleme:
                erreurs.append(f"{chemin} : {probleme}")
            else:
                a_ecrire[chemin] = nouveau_fichier

    phrases_attendues = len(PHRASES)
    with open("accents_rapport.txt", "w", encoding="utf-8") as r:
        r.write("Rapport de accents.py : les corrections proposées dans les textes français (@fr).\n\n")
        r.write("1. MOTS CORRIGÉS PARTOUT (forme d'origine -> forme corrigée, nombre)\n\n")
        for (avant, apres), nb in sorted(par_mot.items()):
            r.write(f"   {avant} -> {apres}   ({nb})\n")
        r.write("\n2. MOTS CORRIGÉS SELON LE CONTEXTE (le mot décidé est entre crochets)\n")
        r.write("   Chaque « a » est listé, qu'il devienne « à » ou reste le verbe avoir.\n\n")
        for nom, avant, apres, extrait in sorted(contexte, key=lambda x: (sans_accents(x[1]).lower(), x[0])):
            etat = "gardé" if avant == apres else f"{avant} -> {apres}"
            r.write(f"   {nom:24} {etat:22} ...{extrait}...\n")
        r.write(f"\n3. PHRASES REFORMULÉES ({len(phrases)} sur {phrases_attendues})\n\n")
        for nom, avant, apres in phrases:
            avant = avant.replace("\r", "").replace("\n", "\n           ")
            apres = apres.replace("\r", "").replace("\n", "\n           ")
            r.write(f"   {nom}\n   AVANT : {avant}\n   APRÈS : {apres}\n\n")
        if len(phrases) < phrases_attendues:
            r.write("   Une phrase n'a pas été trouvée telle quelle : elle a peut-être déjà été modifiée.\n")

    nb_mots = sum(par_mot.values())
    nb_contexte = sum(1 for c in contexte if c[1] != c[2])
    print(f"Textes français lus : {total_textes}, dont {textes_sans_accent} sans aucun accent")
    print(f"Corrections : {nb_mots + nb_contexte} mots ({nb_mots} partout, {nb_contexte} selon le contexte), "
          f"et {len(phrases)} phrases reformulées sur {phrases_attendues}")
    for nom, n in resume:
        print(f"   {nom:26} {n} mots")
    for e in erreurs:
        print("ERREUR, fichier non modifié :", e)
    print("Détail de chaque correction : accents_rapport.txt")
    if not appliquer:
        print("Simulation : aucun fichier n'a été modifié. Pour appliquer : python tools/accents.py --appliquer")
        return 1 if erreurs else 0
    for chemin, texte in a_ecrire.items():
        with open(chemin, "w", encoding="utf-8", newline="") as f:
            f.write(texte)
    print(f"Fichiers corrigés : {len(a_ecrire)}. Vérifie chaque changement avec : git diff --word-diff src/ontology")
    return 1 if erreurs else 0


if __name__ == "__main__":
    sys.exit(main())
