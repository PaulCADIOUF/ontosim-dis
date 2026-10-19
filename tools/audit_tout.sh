#!/usr/bin/env bash
# Audite les 9 modules d'OntoSim-Dis, chacun avec les modules qu'il importe.
#
# A lancer depuis Git Bash, a la racine du depot :
#     bash tools/audit_tout.sh
#
# Le script cherche lui-meme la commande Python. Pour en imposer une :
#     PYTHON=py bash tools/audit_tout.sh

cd "$(dirname "$0")/.." || exit 1

# Une commande Python qui sait importer rdflib et owlready2
PY="$PYTHON"
if [ -z "$PY" ]; then
    for cand in python py python3; do
        if command -v "$cand" >/dev/null 2>&1 && "$cand" -c "import rdflib, owlready2" >/dev/null 2>&1; then
            PY="$cand"
            break
        fi
    done
fi
if [ -z "$PY" ]; then
    echo "Python introuvable, ou rdflib et owlready2 non installes."
    echo "Installe-les avec :  pip install rdflib owlready2"
    exit 1
fi

if ! command -v java >/dev/null 2>&1; then
    echo "Attention : Java introuvable. HermiT ne pourra pas tourner, et chaque audit"
    echo "le signalera comme une erreur [5]. Installe Java, ou relance avec --no-reasoner."
    echo
fi

O=src/ontology
L1=$O/layer1_foundational.ttl
L2=$O/layer2_modsim.ttl
A=$O/layer3a_mas.ttl
B=$O/layer3b_equations.ttl
G=$O/layer4-ogms.ttl
C=$O/layer4_core.ttl
I=$O/layer4_infectious.ttl
X=$O/layer4-context.ttl
K=$O/layer4-checks.ttl
REF="tools/ref/ro.owl tools/ref/iao.owl tools/ref/bfo.owl tools/ref/ogms-edit.owl"

# Options passees au script (par exemple --no-reasoner), transmises a chaque audit
OPTS="$*"

echecs=0
audit() {
    # $1 = le module audite ; la suite = ce module et tous ceux qu'il importe
    "$PY" tools/audit_ontosim.py --focus "$1" --load "${@:2}" --ref $REF $OPTS || echecs=$((echecs + 1))
    echo
}

audit "$L1" "$L1"
audit "$L2" "$L1" "$L2"
audit "$A"  "$L1" "$L2" "$A"
audit "$B"  "$L1" "$L2" "$B"
audit "$G"  "$L1" "$G"
audit "$C"  "$L1" "$L2" "$G" "$C"
audit "$I"  "$L1" "$L2" "$G" "$C" "$I"
audit "$X"  "$L1" "$L2" "$X"
audit "$K"  "$L1" "$L2" "$A" "$B" "$G" "$C" "$K"

echo "======================================================================"
echo "Modules avec au moins une erreur : $echecs sur 9"
[ "$echecs" -eq 0 ]
