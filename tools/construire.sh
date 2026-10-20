#!/usr/bin/env bash
# Construit le fichier complet et le site de documentation d'OntoSim-Dis.
#
# A lancer depuis Git Bash, a la racine du depot :
#     bash tools/construire.sh
#
# Il faut Java 11 ou plus recent, et deux outils telecharges une fois dans tools/lib/
# (voir tools/README.md) :
#     tools/lib/robot.jar     ROBOT, qui reunit les modules en un seul fichier
#     tools/lib/widoco.jar    WIDOCO, qui ecrit la documentation
#
# Le script cherche lui-meme une Java assez recente, meme si la commande java est plus
# ancienne : dans JAVA_HOME, puis dans les dossiers d'installation habituels de Windows.
# Pour en imposer une :
#     JAVA="/c/Program Files/Eclipse Adoptium/jdk-21.../bin/java" bash tools/construire.sh
#
# Tout ce qui est produit va dans build/, que git ignore :
#     build/ontosim-dis-full.ttl             toute l'ontologie en un fichier, sans owl:imports
#     build/site/latest/                     la documentation, et l'ontologie en 4 formats
#     build/site/<numero>/                   la meme chose, pour la version figee
#     build/site/<module>/latest/ et build/site/<module>/<numero>/   le fichier de chaque module
#     build/site/index.html                  l'accueil du site, qui renvoie vers la documentation
#
# Le dossier build/ est efface et refait a chaque lancement.

cd "$(dirname "$0")/.." || exit 1

O=src/ontology
ROBOT=tools/lib/robot.jar
WIDOCO=tools/lib/widoco.jar
LANGUE=en   # langue de la page d'accueil du site : en ou fr

# Chaque module : son chemin dans l'IRI, puis son fichier
MODULES="layer1:layer1_foundational.ttl layer2:layer2_modsim.ttl layer3a:layer3a_mas.ttl
layer3b:layer3b_equations.ttl layer4-ogms:layer4-ogms.ttl layer4-core:layer4_core.ttl
layer4-infectious:layer4_infectious.ttl layer4-context:layer4-context.ttl
layer4-checks:layer4-checks.ttl"

# 1. Les outils

# Numero majeur d'une Java : 8 pour "1.8.0_31", 21 pour "21.0.5"
version_java() {
    "$1" -version 2>&1 | grep -m 1 'version "' \
        | sed -n 's/.*version "\([0-9]*\)\.\{0,1\}\([0-9]*\).*/\1 \2/p' \
        | awk '{ if ($1 == 1) print $2; else print $1 }'
}

if [ -z "$JAVA" ]; then
    candidats=()
    command -v java >/dev/null 2>&1 && candidats+=("$(command -v java)")
    if [ -n "$JAVA_HOME" ]; then
        jh="$JAVA_HOME"
        command -v cygpath >/dev/null 2>&1 && jh=$(cygpath -u "$JAVA_HOME")
        candidats+=("$jh/bin/java")
    fi
    for j in "/c/Program Files/Eclipse Adoptium"/*/bin/java.exe \
             "/c/Program Files/Java"/*/bin/java.exe \
             "/c/Program Files/Microsoft"/jdk*/bin/java.exe \
             "/c/Program Files/Zulu"/*/bin/java.exe; do
        [ -f "$j" ] && candidats+=("$j")
    done
    meilleure=0
    for j in "${candidats[@]}"; do
        v=$(version_java "$j" 2>/dev/null)
        if [ -n "$v" ] && [ "$v" -gt "$meilleure" ]; then
            meilleure=$v
            JAVA="$j"
        fi
    done
fi
if [ -z "$JAVA" ]; then
    echo "Java introuvable. Installe Java 21 : https://adoptium.net (version LTS)."
    exit 1
fi
VJ=$(version_java "$JAVA")
if [ -z "$VJ" ] || [ "$VJ" -lt 11 ]; then
    echo "La Java trouvee est trop ancienne ($JAVA, version ${VJ:-inconnue})."
    echo "ROBOT et WIDOCO demandent Java 11 ou plus recent. Installe Java 21 : https://adoptium.net"
    exit 1
fi
echo "Java $VJ : $JAVA"

for jar in "$ROBOT" "$WIDOCO"; do
    if [ ! -f "$jar" ]; then
        echo "Il manque $jar. Les commandes pour le telecharger sont dans tools/README.md."
        exit 1
    fi
done

PY="$PYTHON"
if [ -z "$PY" ]; then
    for cand in python py python3; do
        if command -v "$cand" >/dev/null 2>&1 && "$cand" -c "import rdflib" >/dev/null 2>&1; then
            PY="$cand"
            break
        fi
    done
fi
if [ -z "$PY" ]; then
    echo "Python introuvable, ou rdflib non installe : pip install rdflib"
    exit 1
fi

# 2. Les numeros de version doivent etre coherents
if ! "$PY" tools/version.py >/dev/null; then
    echo "Les numeros de version ne sont pas coherents. Lance : python tools/version.py"
    exit 1
fi
VERSION=$(sed -n 's/.*owl:versionInfo "\([^"]*\)".*/\1/p' "$O/ontosim-dis.ttl" | head -n 1)
echo "=== OntoSim-Dis $VERSION ==="

rm -rf build
mkdir -p build/site

# 3. Le fichier complet : ROBOT suit les imports grace au catalogue, puis les retire
echo
echo "=== 1/3 Fichier complet (ROBOT) ==="
if ! "$JAVA" -jar "$ROBOT" merge --catalog "$O/catalog-v001.xml" \
        --input "$O/ontosim-dis.ttl" --output build/ontosim-dis-full.ttl; then
    echo "ROBOT a echoue : rien n'a ete construit."
    exit 1
fi
echo "build/ontosim-dis-full.ttl"

# 4. La documentation, en anglais et en francais, avec WebVOWL et l'evaluation OOPS!
echo
echo "=== 2/3 Documentation (WIDOCO) ==="
if ! "$JAVA" -jar "$WIDOCO" -ontFile build/ontosim-dis-full.ttl -outFolder build/site/latest \
        -getOntologyMetadata -lang en-fr -webVowl -uniteSections -noPlaceHolderText -oops \
        -rewriteAll > build/widoco.log 2>&1; then
    echo "WIDOCO a echoue. Le detail est dans build/widoco.log"
    exit 1
fi
for f in index-en.html index-fr.html ontology.ttl ontology.owl ontology.nt ontology.jsonld; do
    if [ ! -f "build/site/latest/$f" ]; then
        echo "WIDOCO n'a pas produit $f. Le detail est dans build/widoco.log"
        exit 1
    fi
done
echo "build/site/latest/ : index-en.html, index-fr.html et l'ontologie en ttl, owl, nt, jsonld"
if [ -f build/site/latest/OOPSevaluation/oopsEval.html ]; then
    echo "Evaluation OOPS! : build/site/latest/OOPSevaluation/oopsEval.html"
else
    echo "Attention : OOPS! n'a pas repondu, la page n'aura pas d'evaluation."
    echo "Relance plus tard, ou soumets build/ontosim-dis-full.ttl sur https://oops.linkeddata.es"
fi

# 5. La version figee, les modules et l'accueil
echo
echo "=== 3/3 Version $VERSION, modules, accueil ==="
cp -r build/site/latest "build/site/$VERSION"
for paire in $MODULES; do
    m=${paire%%:*}
    f=${paire#*:}
    mkdir -p "build/site/$m/latest" "build/site/$m/$VERSION"
    cp "$O/$f" "build/site/$m/latest/ontology.ttl"
    cp "$O/$f" "build/site/$m/$VERSION/ontology.ttl"
done
cat > build/site/index.html <<FIN
<!DOCTYPE html>
<html lang="$LANGUE">
<head>
<meta charset="utf-8">
<title>OntoSim-Dis</title>
<meta http-equiv="refresh" content="0; url=latest/index-$LANGUE.html">
</head>
<body><p><a href="latest/index-$LANGUE.html">OntoSim-Dis</a></p></body>
</html>
FIN
echo "build/site/$VERSION/, un dossier par module, build/site/index.html"

echo
echo "Fini. Pour regarder la documentation :"
echo "    cd build/site && $PY -m http.server 8000"
echo "puis ouvre http://localhost:8000/latest/index-fr.html dans ton navigateur (Ctrl+C pour arreter)."
