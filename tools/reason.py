import sys, os, tempfile, warnings
from rdflib import Graph, OWL
import owlready2
warnings.filterwarnings("ignore")

files = sys.argv[1:]
g = Graph()
for f in files:
    g.parse(f, format="turtle")
for t in list(g.triples((None, OWL.imports, None))):
    g.remove(t)
tmp = os.path.join(tempfile.mkdtemp(), "merged.owl")
g.serialize(tmp, format="xml")
onto = owlready2.get_ontology("file://" + tmp).load()
with onto:
    owlready2.sync_reasoner(infer_property_values=False, debug=0)

inc = [c.name for c in owlready2.default_world.inconsistent_classes() if hasattr(c,"name")]
print("=== HermiT : coherence ===")
print("classes insatisfiables :", inc or "AUCUNE")

attendus = {
 "tCercariae": (["FreeLivingStageState","ReservoirState","CouplingSource"], ["HealthState"]),
 "tSchisto":   (["DiseaseKnowledgeTemplate","InfectiousDiseaseKnowledge",
                 "EnvironmentallyMediatedDiseaseKnowledge"], []),
 "tCovid":     (["DiseaseKnowledgeTemplate","InfectiousDiseaseKnowledge"],
                ["EnvironmentallyMediatedDiseaseKnowledge"]),
}
ok = bad = 0
print("\n=== Test fonctionnel : classification inferee ===")
for name,(must,mustnot) in attendus.items():
    ind = owlready2.default_world.search_one(iri="*#"+name)
    if ind is None:
        print(f"  ?  {name} : individu introuvable"); bad += 1; continue
    anc = {c.name for c in ind.INDIRECT_is_a if hasattr(c,"name")}
    miss = [c for c in must    if c not in anc]
    extra= [c for c in mustnot if c in anc]
    if miss or extra:
        bad += 1
        print(f"  X  {name}")
        if miss:  print(f"       manque  : {miss}")
        if extra: print(f"       en trop : {extra}")
        print(f"       infere  : {sorted(anc)}")
    else:
        ok += 1
        print(f"  OK {name}  ->  {sorted(anc)}")
print(f"\n{ok} verifications passees, {bad} echouees")
sys.exit(1 if bad or inc else 0)
