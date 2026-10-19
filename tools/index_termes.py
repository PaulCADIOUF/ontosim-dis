#!/usr/bin/env python3
"""
index_termes.py : régénère docs/index_termes.md à partir des fichiers de src/ontology.

À lancer depuis Git Bash, à la racine du dépôt, après chaque modification de l'ontologie :

    python tools/index_termes.py

Pour chaque terme : le module où il est déclaré, sa nature et sa définition française
(l'anglaise à défaut). Une classe est dite « définie » quand elle a une équivalence
(« Equivalent To » dans Protégé) : le raisonneur sait alors la reconnaître seul.

Un nouveau fichier .ttl placé dans src/ontology est pris en compte sans rien changer ici :
il apparaît sous son nom de fichier. Pour lui donner un nom court, l'ajouter à MODULES.
"""
import datetime
import glob
import os
import sys

from rdflib import Graph, OWL, RDF, RDFS, URIRef

# Les modules connus, dans l'ordre des couches, avec le nom court employé dans l'index
MODULES = [
    ("layer1_foundational.ttl", "Couche 1"),
    ("layer2_modsim.ttl", "Couche 2"),
    ("layer3a_mas.ttl", "Couche 3A"),
    ("layer3b_equations.ttl", "Couche 3B"),
    ("layer4-ogms.ttl", "4-OGMS"),
    ("layer4_core.ttl", "4-Core"),
    ("layer4_infectious.ttl", "4-Infectious"),
    ("layer4-context.ttl", "4-Context"),
    ("layer4-checks.ttl", "4-Checks"),
]
LOCAL = "https://w3id.org/ontosim-dis#"
OBO = "http://purl.obolibrary.org/obo/"
LONGUEUR = 160          # au-delà, la définition est coupée et finit par « … »
MOIS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août",
        "septembre", "octobre", "novembre", "décembre"]


def nom_court(iri):
    s = str(iri)
    return s.split("#")[-1] if s.startswith(LOCAL) else s.rsplit("/", 1)[-1]


def texte(g, terme, propriete):
    """Le texte français de la propriété, l'anglais à défaut, sinon une chaîne vide."""
    valeurs = list(g.objects(terme, propriete))
    for langue in ("fr", "en", None):
        for v in valeurs:
            if getattr(v, "language", None) == langue:
                return " ".join(str(v).split())
    return " ".join(str(valeurs[0]).split()) if valeurs else ""


def couper(t):
    t = t.replace("|", "\\|")
    if len(t) > LONGUEUR:
        t = t[:LONGUEUR].rsplit(" ", 1)[0] + "…"
    return t


def main():
    try:
        sys.stdout.reconfigure(errors="replace")   # console Windows
    except AttributeError:
        pass
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    # Les modules connus d'abord, puis tout autre fichier .ttl, sous son nom de fichier
    connus = dict(MODULES)
    presents = sorted(os.path.basename(f) for f in glob.glob(os.path.join("src", "ontology", "*.ttl")))
    a_lire = [(f, m) for f, m in MODULES if f in presents]
    a_lire += [(f, f[:-4]) for f in presents if f not in connus]
    absents = [f for f, _ in MODULES if f not in presents]

    termes = {}                                   # nom court -> (module, nature, définition)
    sortes = [(OWL.Class, "classe"), (OWL.ObjectProperty, "relation"),
              (OWL.DatatypeProperty, "donnée"), (OWL.NamedIndividual, "valeur")]
    for fichier, module in a_lire:
        g = Graph().parse(os.path.join("src", "ontology", fichier), format="turtle")
        for type_owl, nature in sortes:
            for terme in g.subjects(RDF.type, type_owl):
                if not isinstance(terme, URIRef):
                    continue
                iri = str(terme)
                if iri.startswith(OBO):
                    nature_terme = "importé"
                    definition = f"*{texte(g, terme, RDFS.label)}* — {texte(g, terme, RDFS.comment)}"
                elif iri.startswith(LOCAL):
                    nature_terme = nature
                    if nature == "classe" and (terme, OWL.equivalentClass, None) in g:
                        nature_terme = "**classe définie**"
                    definition = texte(g, terme, RDFS.comment)
                else:
                    continue                      # skos, dcterms... : pas des termes de l'ontologie
                nom = nom_court(terme)
                if nom not in termes:             # un terme compte une fois, dans le premier module qui le déclare
                    termes[nom] = (module, nature_terme, couper(definition))

    par_module = {}
    for module, _, _ in termes.values():
        par_module[module] = par_module.get(module, 0) + 1
    aujourd_hui = datetime.date.today()
    date = f"{aujourd_hui.day} {MOIS[aujourd_hui.month - 1]} {aujourd_hui.year}"

    lignes = [
        "# OntoSim-Dis — Index alphabétique des termes",
        "",
        f"**{len(termes)} termes**, régénéré le {date} à partir des {len(a_lire)} fichiers de "
        "`src/ontology`, par `tools/index_termes.py`. Ne pas modifier à la main : relancer le script.",
        "",
        "Pour chaque terme : le module où il se trouve, sa nature, et sa définition française "
        "(l'anglaise à défaut). Les **classes définies** sont celles que le raisonneur sait "
        "reconnaître seul ; les termes `importé` viennent de BFO, RO, IAO ou OGMS par MIREOT "
        "et portent leur libellé officiel en italique.",
        "",
        "| Module | Termes |",
        "|---|---|",
    ]
    for _, module in a_lire:
        if module in par_module:
            lignes.append(f"| {module} | {par_module[module]} |")
    lignes += ["", "| Terme | Module | Nature | Définition |", "|---|---|---|---|"]
    for nom in sorted(termes, key=str.lower):
        module, nature, definition = termes[nom]
        lignes.append(f"| `{nom}` | {module} | {nature} | {definition} |")

    os.makedirs("docs", exist_ok=True)
    with open(os.path.join("docs", "index_termes.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lignes) + "\n")

    print(f"docs/index_termes.md : {len(termes)} termes, lus dans {len(a_lire)} fichiers.")
    for _, module in a_lire:
        if module in par_module:
            print(f"   {module:13} {par_module[module]}")
    for fichier in absents:
        print(f"   (fichier absent : {fichier})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
