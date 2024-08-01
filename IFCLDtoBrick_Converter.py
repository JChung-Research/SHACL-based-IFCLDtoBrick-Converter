

# pip install pyshacl and rdflib
from time import perf_counter
import os
import argparse

from pyshacl import Validator
from rdflib import Graph, Namespace

def IFCLDtoBrick_converter(inputFile, outputFile, shaclFile):

    g = Graph()

    # The IFC file is from 'https://github.com/gtfierro/brick-ifc-convert/blob/master/example_files/CIEE.ifc'
    # The IFC model was converted into IFC-LD graph using Devon's IFC-LD instance builder from 'https://github.com/devonsparks/ifcld-service/tree/main'
    # Only a few triples are selected to reduce the size of the file for this example

    # The goal of this shape graph is to construct Brick graphs
    sh = Graph()
    data_graph = inputFile#"CIEE_IFC-LD_light.ttl"
    g.parse(data_graph)
    shapes_graph = shaclFile#"IfcLDtoBrick_SHACL_Jihoon_20240709.ttl"
    sh.parse(shapes_graph)

    print("Generating Brick graphs..")

    # Implement RDFS inferencing using PySHACL
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


    # Define a SPARQL query to select triples from the Brick namespace
    brickGraph = Graph()
    brickQuery = """
        SELECT ?s ?p ?o
        WHERE {
            ?s ?p ?o .
            FILTER (strstarts(str(?s), "https://brickschema.org/schema/Brick#") ||
                    strstarts(str(?p), "https://brickschema.org/schema/Brick#") ||
                    strstarts(str(?o), "https://brickschema.org/schema/Brick#"))
        }
    """

    # Execute the query
    results = g.query(brickQuery)

    # from RDFLib import Graph, Namespace, URIRef, Literal
    brick = Namespace("https://brickschema.org/schema/Brick#")
    ifcld = Namespace("http://ifc-ld.org/graphs/")
    brickGraph.bind("brick", brick)
    brickGraph.bind("ifcld", ifcld)

    # Adding the selected triples to the BrickGraph variable
    for i, row in enumerate(results):
        brickGraph.add((row.s, row.p, row.o))
        print(f"Graph #{i}: {row.s} {row.p} {row.o}")

    print("Graph Generation is done!")

    context = {
        "@language": "en",
        "ifcld": "http://ifc-ld.org/graphs/",
        "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "brick": "https://brickschema.org/schema/Brick#",
        }

    # Save the Brick graph data
    brickGraph.serialize(
        destination=outputFile,#"CIEE_Brick.ttl", 
        indent=2, 
        # context=context,
        format="ttl",
        #auto_compact=True,
        encoding="utf-8"
        )

    print("Brick graphs are saved!")

t1_start = perf_counter()
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Convert IFC-LD triples to Brick triples')
    parser.add_argument('-i', type=str, help='input IFC-LD file path')
    parser.add_argument('-o', type=str, help='output Brick file path')
    parser.add_argument('-s', type=str, help='SHACL file path')

    args = parser.parse_args()

    if args.i:
        ifcldFilePath = args.i
    if args.s:
        shaclFilePath = args.s
    
    if os.path.isfile(ifcldFilePath) and os.path.isfile(shaclFilePath):
        if args.o:
            brickFilePath = args.o
        else:
            brickFilePath = os.path.splitext(ifcldFilePath)[0] + '.ttl'
        
        IFCLDtoBrick_converter(ifcldFilePath, brickFilePath, shaclFilePath)
    else:
        print(str(args.i) + ' is not a valid file')


    t1_stop = perf_counter()
    print("Conversion took ", t1_stop-t1_start, " seconds")


