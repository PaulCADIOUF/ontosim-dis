# OntoSim-Dis - Layer 1 - Couche 1 - foundational 

Fichier : layer1_foundational.ttl  
IRI : http://www.ontosim-dis.org/ontology/layer1   
version 1.0  
Licence : CC BY 4.0  
Statut : ferméé à la version 1.0. Toute modification donne une nouvelle version.  

## Rôle

la couche 1 contient les concepts fondateurs, notez qu'elle est independante de tout domaine applicatif.
Elle fournit aux autres couches les categories les plus genérale et les relations qui les lient. Il est important de souligner que cette couche ne contient aucun terme medical.

## Sources et version
Basic Formal Ontology
Relation Ontology
Information Artefact Ontology 

Notée que toute ces sources nous ont été utiles. Et la méthode utilisé pour prendre ceux qui nous intéressés etait MIREOT.

## Contenu : Nos 13 Classes

BFO_0000001  
BFO_0000002  
BFO_0000003  
BFO_0000004  
BFO_0000015  
BFO_0000016  
BFO_0000017  
BFO_0000019  
BFO_0000020  
BFO_0000031  
BFO_0000040  
BFO_0000141  
BFO_0000030  

## Contenu : Nos 16 propriétés d'objet

BFO_0000050  
BFO_0000054  
BFO_0000055  
IAO_0000136  
RO_0000052  
RO_0000053  
RO_0000056  
RO_0000057  
RO_0000091  
RO_0001025  
RO_0002131  
RO_0002233  
RO_0002234  
RO_0002314  
RO_0002323  
RO_0002502  

## Disjonctions 
continuant ⊥ occurrent  
independent ⊥ specifically dependent ⊥ generically dependent continuant  
material ⊥ immaterial entity  
realizable entity ⊥ quality   

## Validation

### 1. Audit automatique
Test réalisé le 22/09/2026 : 0 erreurs, 0 avertissements.  
Ce qui prouve que l'ontologie est cohérente selon HermiT.  

A noter que l'outil actuellement utilisé vérifie la forme(libellés, références, hiérarchies, caractéristiques, cohérence), il ne verifie pas reellement le sens, chose qui sera faite sur le cahier de conception.

### 2. OOPS!
 Vérification que l'on va faire apres la création des 4 couches

## Décisions mineures/majeures
Où placer OGMS? lors de la création de la couche 4

has input / has output : retirer ou remplacer par has specified input/output d'OBI ? Décision à prendre plus tard.

Un agent participe-t-il directement à la simulation ? Décision à prendre lors de la création de la couche 3.
