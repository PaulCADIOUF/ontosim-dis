#!/usr/bin/env python3
"""
version.py : donne le même numéro de version à tout l'empilement d'OntoSim-Dis,
puis réécrit les deux catalogues.

À lancer depuis Git Bash, à la racine du dépôt :

    python tools/version.py                  état : le numéro de chaque fichier, et les contrôles
    python tools/version.py 1.1              simulation : ce qui changerait, sans rien écrire
    python tools/version.py 1.1 --appliquer  écrit les changements

Ce qui change :
  - dans chaque fichier de src/ontology : l'IRI de version, le numéro (owl:versionInfo)
    et les imports. Par exemple, <.../layer2/1.0> devient <.../layer2/1.1> ;
  - dans chaque fichier de tests : les imports seulement. Le numéro propre d'un test
    reste le sien ;
  - les deux catalogues, src/ontology/catalog-v001.xml et tests/catalog-v001.xml :
    ils sont réécrits à partir des en-têtes. Chaque module y figure deux fois, avec et
    sans numéro, et l'ombrelle aussi.

Avant d'écrire un fichier, le script vérifie avec rdflib que le fichier modifié contient
les mêmes triplets qu'avant, à ces changements près. Il finit par cinq contrôles :
  1. tous les fichiers de src/ontology portent le même numéro ;
  2. chaque IRI de version vaut l'IRI de l'ontologie, suivie de "/" et du numéro ;
  3. chaque import vise un fichier de src/ontology, à son IRI de version ;
  4. l'ombrelle, ontosim-dis.ttl, importe tous les modules ;
  5. chaque catalogue connaît toutes ces IRI, et chaque fichier qu'il cite existe.

Rappel : une version publiée ne change plus. Une correction prend un nouveau numéro.
"""
import glob
import os
import re
import sys
import xml.etree.ElementTree as ET

from rdflib import Graph, Literal, URIRef
from rdflib.compare import isomorphic
from rdflib.namespace import OWL, RDF

BASE = "https://w3id.org/ontosim-dis"
RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ONTO = os.path.join(RACINE, "src", "ontology")
TESTS = os.path.join(RACINE, "tests")
OMBRELLE = "ontosim-dis.ttl"

# Ordre des fichiers dans les catalogues : l'ombrelle, puis les couches
ORDRE = [OMBRELLE, "layer1_foundational.ttl", "layer2_modsim.ttl", "layer3a_mas.ttl",
         "layer3b_equations.ttl", "layer4-ogms.ttl", "layer4_core.ttl", "layer4_infectious.ttl",
         "layer4-context.ttl", "layer4-checks.ttl"]

NUMERO = re.compile(r"^[0-9]+\.[0-9]+(\.[0-9]+)?$")

ENTETE_SRC = ("<!-- Produit par tools/version.py. Dit a Protege et a ROBOT ou trouver chaque "
              "module sur le disque, au lieu de le chercher sur w3id.org. -->")
ENTETE_TESTS = ("<!-- Produit par tools/version.py. Dit a Protege ou trouver les couches sur le "
                "disque : dans ../src/ontology/, et non sur w3id.org. -->")


class Fichier:
    """Un fichier Turtle : son texte, ses triplets et son en-tete."""

    def __init__(self, chemin):
        self.chemin = chemin
        self.nom = os.path.basename(chemin)
        with open(chemin, encoding="utf-8", newline="") as f:
            self.texte = f.read()
        self.graphe = Graph().parse(data=self.texte, format="turtle")
        ontos = list(self.graphe.subjects(RDF.type, OWL.Ontology))
        if len(ontos) != 1:
            raise ValueError(f"{self.nom} : {len(ontos)} en-tetes owl:Ontology, il en faut un")
        self.onto = ontos[0]
        self.viri = self.graphe.value(self.onto, OWL.versionIRI)
        self.vinfo = self.graphe.value(self.onto, OWL.versionInfo)
        self.imports = sorted(self.graphe.objects(self.onto, OWL.imports), key=str)


def ordre(nom):
    return (ORDRE.index(nom), nom) if nom in ORDRE else (len(ORDRE), nom)


def charger(dossier):
    return sorted((Fichier(c) for c in glob.glob(os.path.join(dossier, "*.ttl"))),
                  key=lambda f: ordre(f.nom))


def renumeroter(f, nouveau, cible, avec_entete):
    """Rend (nouveau texte, changements, erreurs) pour le fichier f.
    cible : IRI d'ontologie ou de version d'un module -> son IRI d'ontologie.
    avec_entete : False pour un test, dont on ne change que les imports."""
    texte, changements, erreurs = f.texte, [], []
    attendu = Graph()
    for t in f.graphe:
        attendu.add(t)

    if avec_entete:
        ancien = f.viri
        neuf = URIRef(f"{f.onto}/{nouveau}")
        if ancien is None:
            erreurs.append(f"{f.nom} : pas d'IRI de version")
        elif ancien != neuf:
            n = texte.count(f"<{ancien}>")
            if n != 1:
                erreurs.append(f"{f.nom} : l'IRI de version <{ancien}> apparait {n} fois, 1 attendue")
            texte = texte.replace(f"<{ancien}>", f"<{neuf}>")
            attendu.remove((f.onto, OWL.versionIRI, ancien))
            attendu.add((f.onto, OWL.versionIRI, neuf))
            changements.append(f"version {ancien} -> {neuf}")
        if f.vinfo is None:
            erreurs.append(f"{f.nom} : pas de owl:versionInfo")
        elif str(f.vinfo) != nouveau:
            motif = re.compile(r'(owl:versionInfo\s+)"' + re.escape(str(f.vinfo)) + '"')
            texte, n = motif.subn(lambda m: m.group(1) + '"' + nouveau + '"', texte)
            if n != 1:
                erreurs.append(f'{f.nom} : owl:versionInfo "{f.vinfo}" trouve {n} fois, 1 attendue')
            attendu.remove((f.onto, OWL.versionInfo, f.vinfo))
            attendu.add((f.onto, OWL.versionInfo,
                         Literal(nouveau, datatype=f.vinfo.datatype, lang=f.vinfo.language)))
            changements.append(f'numero "{f.vinfo}" -> "{nouveau}"')

    for imp in f.imports:
        if not str(imp).startswith(BASE + "/"):
            continue  # un import hors d'OntoSim-Dis n'est pas touche
        if imp not in cible:
            erreurs.append(f"{f.nom} : import inconnu <{imp}>, aucun fichier de src/ontology ne le declare")
            continue
        neuf = URIRef(f"{cible[imp]}/{nouveau}")
        if neuf != imp:
            n = texte.count(f"<{imp}>")
            if n != 1:
                erreurs.append(f"{f.nom} : l'import <{imp}> apparait {n} fois, 1 attendue")
            texte = texte.replace(f"<{imp}>", f"<{neuf}>")
            attendu.remove((f.onto, OWL.imports, imp))
            attendu.add((f.onto, OWL.imports, neuf))
            changements.append(f"import {imp} -> {neuf}")

    # Le texte modifie doit donner exactement les triplets attendus, ni plus ni moins
    if changements and not erreurs:
        try:
            obtenu = Graph().parse(data=texte, format="turtle")
        except Exception as e:
            erreurs.append(f"{f.nom} : le texte modifie ne se lit plus ({e})")
        else:
            if not isomorphic(obtenu, attendu):
                erreurs.append(f"{f.nom} : d'autres triplets que l'en-tete changeraient ; fichier non touche")
    return texte, changements, erreurs


def catalogue(entrees, prefixe, entete, fin_de_ligne):
    lignes = ['<?xml version="1.0" encoding="UTF-8" standalone="no"?>', entete,
              '<catalog prefer="public" xmlns="urn:oasis:names:tc:entity:xmlns:xml:catalog">']
    for iri, nom in entrees:
        lignes.append(f'    <uri name="{iri}" uri="{prefixe}{nom}"/>')
    lignes.append("</catalog>")
    return fin_de_ligne.join(lignes) + fin_de_ligne


def entrees_catalogue(sources):
    entrees = []
    for f in sources:
        entrees.append((str(f.onto), f.nom))
        if f.viri is not None:
            entrees.append((str(f.viri), f.nom))
    return entrees


def fin_de_ligne(chemin):
    if os.path.exists(chemin):
        with open(chemin, "rb") as f:
            if b"\r\n" in f.read():
                return "\r\n"
    return "\n"


def lire_catalogue(texte):
    """Les correspondances IRI -> fichier d'un catalogue, quel que soit l'ordre des attributs."""
    if not texte.strip():
        return {}
    try:
        racine = ET.fromstring(texte.encode("utf-8"))
    except ET.ParseError:
        return {}
    return {e.get("name"): e.get("uri") for e in racine.iter()
            if e.tag.endswith("}uri") and e.get("name") and e.get("uri")}


def controles(sources, tests, catalogues):
    """Les cinq controles, sur des fichiers lus ou simules. Rend le nombre d'echecs."""
    echecs = 0

    def dire(ok, message):
        nonlocal echecs
        print(("  OK  " if ok else "  X   ") + message)
        if not ok:
            echecs += 1

    numeros = {str(f.vinfo) for f in sources}
    dire(len(numeros) == 1, f"1. un seul numero dans src/ontology : {', '.join(sorted(numeros))}")

    fausses = [f.nom for f in sources if str(f.viri) != f"{f.onto}/{f.vinfo}"]
    dire(not fausses, "2. chaque IRI de version = IRI de l'ontologie + '/' + numero"
         + (f" ; faux : {', '.join(fausses)}" if fausses else ""))

    versions = {f.viri for f in sources}
    perdus = [f"{f.nom} -> {imp}" for f in sources + tests for imp in f.imports
              if str(imp).startswith(BASE + "/") and imp not in versions]
    dire(not perdus, "3. chaque import vise un fichier de src/ontology, a son IRI de version"
         + (f" ; faux : {'; '.join(perdus)}" if perdus else ""))

    ombrelle = [f for f in sources if f.nom == OMBRELLE]
    if not ombrelle:
        dire(False, f"4. l'ombrelle {OMBRELLE} est absente de src/ontology")
    else:
        manquants = sorted(f.nom for f in sources
                           if f.nom != OMBRELLE and f.viri not in ombrelle[0].imports)
        dire(not manquants, f"4. l'ombrelle importe les {len(sources) - 1} modules"
             + (f" ; manquent : {', '.join(manquants)}" if manquants else ""))

    a_connaitre = {str(f.onto) for f in sources} | {str(f.viri) for f in sources}
    for nom, (dossier, texte) in catalogues.items():
        connus = lire_catalogue(texte)
        absentes = sorted(a_connaitre - set(connus))
        introuvables = sorted(u for u in set(connus.values())
                              if not os.path.exists(os.path.normpath(os.path.join(dossier, u))))
        dire(not absentes and not introuvables,
             f"5. {nom} : {len(connus)} IRI, chacune vers un fichier qui existe"
             + (f" ; IRI absentes : {', '.join(absentes)}" if absentes else "")
             + (f" ; fichiers introuvables : {', '.join(introuvables)}" if introuvables else ""))
    return echecs


def main():
    args = sys.argv[1:]
    appliquer = "--appliquer" in args
    args = [a for a in args if a != "--appliquer"]
    if len(args) > 1 or (args and not NUMERO.match(args[0])):
        print("Usage : python tools/version.py [NUMERO [--appliquer]]   (NUMERO comme 1.1 ou 1.1.2)")
        return 2

    sources, tests = charger(ONTO), charger(TESTS)
    cat_src = os.path.join(ONTO, "catalog-v001.xml")
    cat_tests = os.path.join(TESTS, "catalog-v001.xml")

    print("=== Etat actuel ===")
    for f in sources:
        print(f"  {f.nom:28s} {str(f.vinfo):6s} {f.viri}")
    for f in tests:
        print(f"  tests/{f.nom:22s} importe {', '.join(str(i) for i in f.imports)}")

    if not args:
        print("\n=== Controles ===")
        catalogues = {}
        for chemin, dossier in ((cat_src, ONTO), (cat_tests, TESTS)):
            texte = open(chemin, encoding="utf-8").read() if os.path.exists(chemin) else ""
            catalogues[os.path.relpath(chemin, RACINE).replace(os.sep, "/")] = (dossier, texte)
        echecs = controles(sources, tests, catalogues)
        print(f"\n{echecs} controle(s) en echec." if echecs else "\nTout est coherent.")
        return 1 if echecs else 0

    nouveau = args[0]
    cible = {}
    for f in sources:
        cible[f.onto] = f.onto
        if f.viri is not None:
            cible[f.viri] = f.onto

    print(f"\n=== Passage a la version {nouveau} "
          f"({'les fichiers seront modifies' if appliquer else 'simulation, rien n est ecrit'}) ===")
    resultats, erreurs = [], []
    for f, avec_entete in [(s, True) for s in sources] + [(t, False) for t in tests]:
        texte, changements, err = renumeroter(f, nouveau, cible, avec_entete)
        erreurs += err
        prefixe = "" if avec_entete else "tests/"
        if changements:
            print(f"  {prefixe}{f.nom} : {len(changements)} changement(s)")
            for c in changements:
                print(f"      {c}")
        else:
            print(f"  {prefixe}{f.nom} : rien a changer")
        resultats.append((f, texte, changements))

    if erreurs:
        print("\n=== Erreurs : rien n'a ete ecrit ===")
        for e in erreurs:
            print("  X   " + e)
        return 1

    # Les fichiers tels qu'ils seront, pour les catalogues et les controles
    simules = []
    for f, texte, changements in resultats:
        g = Fichier.__new__(Fichier)
        g.chemin, g.nom, g.texte = f.chemin, f.nom, texte
        g.graphe = Graph().parse(data=texte, format="turtle") if changements else f.graphe
        g.onto = f.onto
        g.viri = g.graphe.value(g.onto, OWL.versionIRI)
        g.vinfo = g.graphe.value(g.onto, OWL.versionInfo)
        g.imports = sorted(g.graphe.objects(g.onto, OWL.imports), key=str)
        simules.append(g)
    sources_neuves, tests_neufs = simules[:len(sources)], simules[len(sources):]

    entrees = entrees_catalogue(sources_neuves)
    textes_cat = {
        cat_src: catalogue(entrees, "", ENTETE_SRC, fin_de_ligne(cat_src)),
        cat_tests: catalogue(entrees, "../src/ontology/", ENTETE_TESTS, fin_de_ligne(cat_tests)),
    }
    for chemin, texte in textes_cat.items():
        avant = open(chemin, encoding="utf-8", newline="").read() if os.path.exists(chemin) else ""
        nom = os.path.relpath(chemin, RACINE).replace(os.sep, "/")
        print(f"  {nom} : {'rien a changer' if avant == texte else 'reecrit, ' + str(len(entrees)) + ' IRI'}")

    print("\n=== Controles sur le resultat ===")
    catalogues = {os.path.relpath(c, RACINE).replace(os.sep, "/"): (os.path.dirname(c), t)
                  for c, t in textes_cat.items()}
    echecs = controles(sources_neuves, tests_neufs, catalogues)
    if echecs:
        print(f"\n{echecs} controle(s) en echec : rien n'a ete ecrit.")
        return 1

    if not appliquer:
        print("\nSimulation : rien n'a ete ecrit. Pour appliquer :")
        print(f"    python tools/version.py {nouveau} --appliquer")
        return 0

    ecrits = 0
    for f, texte, changements in resultats:
        if changements:
            with open(f.chemin, "w", encoding="utf-8", newline="") as sortie:
                sortie.write(texte)
            ecrits += 1
    for chemin, texte in textes_cat.items():
        avant = open(chemin, encoding="utf-8", newline="").read() if os.path.exists(chemin) else ""
        if avant != texte:
            with open(chemin, "w", encoding="utf-8", newline="") as sortie:
                sortie.write(texte)
            ecrits += 1
    print(f"\n{ecrits} fichier(s) ecrit(s). Relis les changements avec :  git diff")
    return 0


if __name__ == "__main__":
    sys.exit(main())
