# pip install pyshacl

from pyshacl import Validator
from rdflib import Graph

g = Graph()

# A turtl file from 'https://github.com/pipauwel/IFCtoRDF/blob/master/src/test/resources/showfiles/nested/20160414office_model_CV2_fordesign.ttl'
# Only a few triples are selected and modified for this example

data_graph = """
@prefix ifc: <http://ifc-ld.org/schemas/ifc2x3#> .
@prefix inst: <http://linkedbuildingdata.net/ifc/resources20170627_103921/> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

inst:IfcSite_63 rdf:type ifc:ifcsite .
inst:IfcRelAggregates_86
    rdf:type  ifc:ifcrelaggregates ;
    ifc:globalId      inst:IfcGloballyUniqueId_42629 ;
    ifc:ownerHistory  inst:IfcOwnerHistory_15 ;
    ifc:relatingobject  inst:IfcSite_63 ;
    ifc:relatedobjects  inst:IfcBuilding_84 .
"""

# Shape graph from an examples in 'https://ifc-ld.org/releases/0.1/spec.html'
# The goal of this shape is to construct a BOT triple 'aSite bot:hasBuilding aBuilding' based on IFC triples

sh = Graph()
shapes_graph = '''
@prefix ifc: <http://ifc-ld.org/schemas/ifc2x3#> .
@prefix mod: <http://ifc-ld.org/profiles/bot/ifc2x3#> .
@prefix bot: <https://w3id.org/bot#> .
@prefix sh: <http://www.w3.org/ns/shacl#> . 
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> . 
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> . 

bot:
	sh:declare [
		sh:prefix "bot" ;
		sh:namespace "https://w3id.org/bot#"^^xsd:anyURI ;
	] .

mod:BotHasBuildingRule
	a sh:NodeShape ;
	sh:targetClass ifc:ifcsite ;
	sh:rule [
		a sh:SPARQLRule ;
		sh:prefixes rdf: ;
        sh:prefixes bot: ;
        sh:prefixes ifc: ;
		sh:construct """
            CONSTRUCT {
                ?site bot:hasBuilding ?building .  
            } WHERE {
                ?site rdf:type ifc:ifcsite . 
                ?relaggregates rdf:type ifc:ifcrelaggregates . 
                ?relaggregates ifc:relatingobject ?site . 
                ?relaggregates ifc:relatedobjects ?building . 
            }
			""" ;
	] 
.
'''

g.parse(data=data_graph, format='turtle')
sh.parse(data=shapes_graph, format='turtle')

# let's have PySHACL also do the RDFS inferencing

v = Validator(
    g, 
    shacl_graph=sh,
    options={
        "advanced": True, 
        "inplace": True, 
        "inference": "rdfs"
        }
    )
(conforms, report_graph, report_text) = v.run()
print(g.serialize())

# Returns the result below, showing 
# inst:IfcSite_63 a ifc:ifcsite,
#    rdfs:Resource ;
#    ns1:hasBuilding inst:IfcBuilding_84 .
# implying the inference was successfully completed!
