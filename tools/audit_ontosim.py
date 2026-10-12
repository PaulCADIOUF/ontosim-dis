#!/usr/bin/env python3
"""
audit_ontosim.py — Verification d'une couche OntoSim-Epi.

Usage :
    python3 audit_ontosim.py --focus layer1-foundational.ttl \
        --load layer1-foundational.ttl \
        --ref ro.owl iao.owl bfo.owl ogms.owl

    --focus : la couche que l'on audite
    --load  : toutes les couches a charger ensemble (dependances comprises)
    --ref   : fichiers officiels de reference (RO, IAO, BFO, OGMS...) pour
              verifier les termes importes par MIREOT

Controles effectues :
    1. Chaque entite propre a un label, une etiquette de langue, un commentaire
    2. Aucune reference vers une entite jamais declaree (reference orpheline)
    3. Aucune propriete d'objet declaree sans etre utilisee dans un axiome
    4. Termes MIREOT : label et parent direct conformes a la source officielle
    5. Coherence logique et satisfiabilite des classes (raisonneur HermiT)

Dependances : pip install rdflib owlready2   (+ Java pour HermiT)
"""
import argparse, os, sys, tempfile, warnings
from rdflib import Graph, RDF, RDFS, OWL, URIRef, Literal

EPI = ("https://w3id.org/ontosim-dis#",            # IRIs actuelles (w3id) : espace de noms des TERMES
       "http://www.ontosim-epi.org/ontology#",     # ancien nom OntoSim-Epi
       "http://www.ontosim-dis.org/ontology")      # nom intermediaire, avant le passage a w3id
OBO = "http://purl.obolibrary.org/obo/"
STD = ("http://www.w3.org/", "http://purl.org/", "http://xmlns.com/")


def short(u):
    s = str(u)
    return s.split("#")[-1] if "#" in s else s.rsplit("/", 1)[-1]


def parse_functional(path, g):
    """Lit une source OWL en syntaxe fonctionnelle et ajoute a g les labels,
    definitions (IAO_0000115) et parents nommes. Renvoie le nombre de triplets
    ajoutes, 0 si le fichier n'est pas en syntaxe fonctionnelle."""
    import re
    try:
        txt = open(path, encoding="utf-8", errors="replace").read()
    except OSError:
        return 0
    if "AnnotationAssertion(" not in txt and "SubClassOf(" not in txt:
        return 0
    n = 0
    for pred, ann in ((RDFS.label, r"rdfs:label"),
                      (URIRef(OBO + "IAO_0000115"), r"obo:IAO_0000115")):
        for m in re.finditer(r'AnnotationAssertion\(\s*' + ann +
                             r'\s+obo:([A-Za-z]+_\d+)\s+"((?:[^"\\]|\\.)*)"', txt):
            g.add((URIRef(OBO + m.group(1)), pred,
                   Literal(m.group(2).replace('\\"', '"').replace("\\\\", "\\"))))
            n += 1
    for m in re.finditer(r'SubClassOf\(\s*obo:([A-Za-z]+_\d+)'
                         r'\s+obo:([A-Za-z]+_\d+)\s*\)', txt):
        g.add((URIRef(OBO + m.group(1)), RDFS.subClassOf, URIRef(OBO + m.group(2))))
        n += 1
    return n


def load(paths):
    g = Graph()
    for p in paths:
        g.parse(p, format="turtle" if p.endswith(".ttl") else None)
    return g


def declared(g):
    out = set()
    for t in (OWL.Class, OWL.ObjectProperty, OWL.DatatypeProperty,
              OWL.AnnotationProperty, OWL.NamedIndividual):
        out |= {x for x in g.subjects(RDF.type, t) if isinstance(x, URIRef)}
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--focus", required=True)
    ap.add_argument("--load", nargs="+", required=True)
    ap.add_argument("--ref", nargs="*", default=[])
    ap.add_argument("--no-reasoner", action="store_true")
    a = ap.parse_args()

    focus, allg = load([a.focus]), load(a.load)
    err, warn = [], []

    print("=" * 70)
    print("AUDIT :", os.path.basename(a.focus))
    print("=" * 70)
    print(f"triplets={len(focus)}  "
          f"classes={len(set(focus.subjects(RDF.type, OWL.Class)))}  "
          f"prop.objet={len(set(focus.subjects(RDF.type, OWL.ObjectProperty)))}  "
          f"prop.donnees={len(set(focus.subjects(RDF.type, OWL.DatatypeProperty)))}")

    # 1. label / langue / commentaire
    own = [x for x in declared(focus) if str(x).startswith(EPI + (OBO,))]
    for x in own:
        labels = list(focus.objects(x, RDFS.label))
        if not labels:
            err.append(f"[1] sans label : {short(x)}")
        for l in labels:
            if isinstance(l, URIRef):
                err.append(f"[1] label dont la valeur est une IRI (champ d'annotation errone ?) : "
                           f"{short(x)} = {l}")
            elif isinstance(l, Literal) and l.language is None:
                warn.append(f"[1] label sans etiquette de langue : {short(x)} = {l!r}")
        if str(x).startswith(EPI) and not list(focus.objects(x, RDFS.comment)):
            warn.append(f"[1] sans commentaire : {short(x)}")

    # 1b. valeur d'annotation contenant ses propres guillemets
    #     (on a tape "2026" dans un champ Protege qui ajoute deja les siens)
    for s, p, o in focus:
        if isinstance(o, Literal):
            v = str(o)
            if len(v) > 1 and v.startswith('"') and v.endswith('"'):
                err.append(f"[1b] valeur entre guillemets dans la valeur : "
                           f"{short(s)} {short(p)} = {v}")

    # 1c. en-tete d'ontologie : versionInfo, created et les autres annotations de
    #     texte doivent etre des chaines. Un nombre nu devient un xsd:decimal ou
    #     un xsd:integer, ce qui n'est pas ce que l'on veut dire.
    TEXT_ANN = (OWL.versionInfo,
                URIRef("http://purl.org/dc/terms/created"),
                URIRef("http://purl.org/dc/terms/creator"),
                URIRef("http://purl.org/dc/terms/source"),
                URIRef("http://purl.org/dc/elements/1.1/description"))
    for p in TEXT_ANN:
        for s, _, o in focus.triples((None, p, None)):
            if isinstance(o, Literal) and o.datatype is not None \
               and str(o.datatype) != "http://www.w3.org/2001/XMLSchema#string":
                err.append(f"[1c] annotation de texte typee : {short(s)} {short(p)} = "
                           f"{o} (type {short(o.datatype)}), attendu une chaine")

    # 2. references orphelines
    #    Seules comptent les references en POSITION D'AXIOME. Une valeur
    #    d'annotation (skos:exactMatch, seeAlso...) peut pointer vers n'importe
    #    quelle IRI exterieure : c'est tout l'objet d'un alignement.
    decl = declared(allg)
    decl |= set(allg.subjects(RDF.type, OWL.Ontology))
    decl |= set(allg.objects(None, OWL.imports)) | set(allg.objects(None, OWL.versionIRI))
    ann_props = set(allg.subjects(RDF.type, OWL.AnnotationProperty)) | {
        RDFS.label, RDFS.comment, RDFS.seeAlso, RDFS.isDefinedBy, OWL.versionInfo}
    refs = set()
    for s, p, o in focus:
        refs.add(s)
        refs.add(p)
        if p not in ann_props:
            refs.add(o)
    refs = {x for x in refs if isinstance(x, URIRef)}
    for x in sorted(refs - decl, key=str):
        s = str(x)
        if s.startswith(STD) or "/ontology/layer" in s or "OSDi" in s:
            continue
        if s.startswith(EPI + (OBO,)):
            err.append(f"[2] reference orpheline : {short(x)}")

    # 3. proprietes decoratives
    used = {o for s, p, o in allg.triples((None, OWL.onProperty, None))}
    used |= {p for s, p, o in allg if isinstance(p, URIRef)}
    for p in focus.subjects(RDF.type, OWL.ObjectProperty):
        if str(p).startswith(EPI) and p not in {o for s, pp, o in allg.triples((None, OWL.onProperty, None))}:
            if not any(True for _ in allg.triples((None, p, None))):
                warn.append(f"[3] propriete jamais utilisee : {short(p)}")

    # 3b. nos propres proprietes doivent declarer domaine ET portee.
    # Une propriete sans l'un des deux ne dit pas ce qu'elle relie : le raisonneur
    # n'en tire rien et OOPS! la signale (P11). Le controle 4b ne couvrait que les
    # proprietes importees — celles d'ici passaient en silence.
    for t in (OWL.ObjectProperty, OWL.DatatypeProperty):
        for p in sorted(focus.subjects(RDF.type, t), key=short):
            if not str(p).startswith(EPI):
                continue
            manque = [n for n, pred in (("domaine", RDFS.domain), ("portee", RDFS.range))
                      if not list(focus.objects(p, pred))]
            if manque:
                err.append(f"[3b] {short(p)} : {' et '.join(manque)} absent"
                           f"{'s' if len(manque) > 1 else ''}")

    # 4. conformite MIREOT
    if a.ref:
        ref = Graph()
        for r in a.ref:
            try:
                ref.parse(r)
            except Exception as e:
                # certaines sources OBO ne sont publiees qu'en syntaxe fonctionnelle
                # OWL, que rdflib ne sait pas lire. On en extrait labels, definitions
                # et parents nommes, ce qui suffit au controle MIREOT.
                n = parse_functional(r, ref)
                if n == 0:
                    warn.append(f"[4] reference illisible {r} : {e}")
        rlab = {s: str(o) for s, p, o in ref.triples((None, RDFS.label, None))}

        # 4a-bis. aucune reference ne couvre ce terme : on ne peut RIEN affirmer.
        # Sans cet avertissement, un fichier de reference vide ou incomplet fait
        # passer le controle en silence (c'etait le cas avec ogms.owl, qui ne
        # contient aucune definition OGMS : seulement ses imports).
        unver = sorted({str(x).split("/")[-1].split("_")[0]
                        for x in own
                        if str(x).startswith(OBO) and x not in rlab})
        if unver:
            n = len([x for x in own if str(x).startswith(OBO) and x not in rlab])
            warn.append(f"[4?] {n} terme(s) importe(s) non verifiables, aucune "
                        f"reference ne les couvre : {', '.join(unver)}")

        for x in own:
            if not str(x).startswith(OBO) or x not in rlab:
                continue
            mine = [str(l) for l in focus.objects(x, RDFS.label)]
            if mine and rlab[x] not in mine:
                err.append(f"[4] label divergent : {short(x)} = {mine[0]!r}, officiel = {rlab[x]!r}")
            p_mine = {o for o in focus.objects(x, RDFS.subClassOf) if isinstance(o, URIRef)}
            p_ref = {o for o in ref.objects(x, RDFS.subClassOf) if isinstance(o, URIRef)}
            if p_mine and p_ref and not (p_mine & p_ref):
                err.append(f"[4] parent divergent : {short(x)} -> "
                           f"{[short(p) for p in p_mine]}, officiel -> {[short(p) for p in p_ref]}")

        # 4b. proprietes importees : hierarchie, domaine, portee, caracteristiques, inverse
        CHAR = [OWL.FunctionalProperty, OWL.InverseFunctionalProperty,
                OWL.TransitiveProperty, OWL.SymmetricProperty,
                OWL.AsymmetricProperty, OWL.ReflexiveProperty, OWL.IrreflexiveProperty]
        focus_props = set(focus.subjects(RDF.type, OWL.ObjectProperty))
        for p in focus_props:
            if not str(p).startswith(OBO) or p not in rlab:
                continue
            for nm, pred in (("sous-propriete", RDFS.subPropertyOf),
                             ("domaine", RDFS.domain), ("portee", RDFS.range)):
                sm = {o for o in focus.objects(p, pred) if isinstance(o, URIRef)}
                sr = {o for o in ref.objects(p, pred) if isinstance(o, URIRef)}
                if sr and not sm:
                    warn.append(f"[4b] {short(p)} ({rlab[p]}) : {nm} absent, officiel = {[short(x) for x in sr]}")
                elif sm and sr and sm != sr:
                    err.append(f"[4b] {short(p)} ({rlab[p]}) : {nm} = {[short(x) for x in sm]}, officiel = {[short(x) for x in sr]}")
            cm = {c for c in CHAR if (p, RDF.type, c) in focus}
            cr = {c for c in CHAR if (p, RDF.type, c) in ref}
            for c in cr - cm:
                warn.append(f"[4b] {short(p)} ({rlab[p]}) : caracteristique manquante {short(c)}")
            for c in cm - cr:
                err.append(f"[4b] {short(p)} ({rlab[p]}) : caracteristique {short(c)} absente de la source officielle")
            # inverse : seulement si les deux proprietes sont presentes dans la couche
            inv_ref = set(ref.objects(p, OWL.inverseOf)) | set(ref.subjects(OWL.inverseOf, p))
            inv_mine = set(focus.objects(p, OWL.inverseOf)) | set(focus.subjects(OWL.inverseOf, p))
            for q in inv_ref & focus_props:
                if q not in inv_mine and str(p) < str(q):
                    err.append(f"[4b] {short(p)} et {short(q)} presentes toutes deux mais non declarees inverses")
    else:
        warn.append("[4] aucune --ref fournie : conformite MIREOT non verifiee")

    # 5. raisonneur
    if not a.no_reasoner:
        try:
            import owlready2
            warnings.filterwarnings("ignore")
            g = load(a.load)
            for t in list(g.triples((None, OWL.imports, None))):
                g.remove(t)
            tmp = os.path.join(tempfile.mkdtemp(), "merged.owl")
            g.serialize(tmp, format="xml")
            onto = owlready2.get_ontology("file://" + tmp).load()
            with onto:
                owlready2.sync_reasoner(infer_property_values=False, debug=0)
            inc = list(owlready2.default_world.inconsistent_classes())
            if inc:
                err.append(f"[5] classes insatisfiables : {[c.name for c in inc]}")
            else:
                print("\n[5] HermiT : ontologie COHERENTE, aucune classe insatisfiable")
        except ImportError:
            warn.append("[5] owlready2 absent : raisonneur non execute")
        except Exception as e:
            err.append(f"[5] HermiT : INCOHERENCE ou echec — {e}")

    print(f"\n--- ERREURS ({len(err)}) ---")
    print("\n".join("  X " + e for e in err) or "  aucune")
    print(f"\n--- AVERTISSEMENTS ({len(warn)}) ---")
    print("\n".join("  ! " + w for w in warn) or "  aucun")
    sys.exit(1 if err else 0)


if __name__ == "__main__":
    main()
