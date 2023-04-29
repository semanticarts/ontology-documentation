from rdflib import  Graph, URIRef, BNode, Literal
import rdflib


ttl = """@prefix :     <https://ontologies.semanticarts.com/o/gistCore#> .
@prefix gist: <https://ontologies.semanticarts.com/gist/> .
@prefix owl:  <http://www.w3.org/2002/07/owl#> .
@prefix rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .

gist:PlannedEvent  rdf:type  owl:Class ;
        owl:equivalentClass  [ rdf:type            owl:Class ;
                               owl:intersectionOf  ( gist:Event
                                                     [ rdf:type         owl:Restriction ;
                                                       owl:cardinality  "1"^^xsd:nonNegativeInteger ;
                                                       owl:onProperty   gist:plannedEndDateTime
                                                     ]
                                                     [ rdf:type         owl:Restriction ;
                                                       owl:cardinality  "1"^^xsd:nonNegativeInteger ;
                                                       owl:onProperty   gist:plannedStartDateTime
                                                     ]
                                                   )
                             ] ;
        skos:definition      "An event which, at the time it is created, is to occur in the future." ;
        skos:prefLabel       "Planned Event" ."""


def color(o):
    if isinstance(o, (URIRef)):
        return f""" "{o}" [color="BLACK"] """
    elif isinstance(o, (BNode)):
        return f""" "{o}" [color="ORANGE"] """
    elif isinstance(o, (Literal)):
        return f""" "{o}" [color="BLUE"] """
    else:
        return f""" "{o}" [color="BLACK"] """

g = Graph().parse(data=ttl, format="turtle")

# for x in g:
#     if str(x[1]) == "http://www.w3.org/1999/02/22-rdf-syntax-ns#first":
#         print("Line 1: ", x[0], x[1], x[2])
#         print("Line 2: ", list(g.objects(x[2])))
#     if str(x[1]) not in ("http://www.w3.org/1999/02/22-rdf-syntax-ns#first", "http://www.w3.org/1999/02/22-rdf-syntax-ns#rest"):
#         print("Line 3: ", x[0], x[1], x[2])

# index = 0
# for x in g:
#     print(color(str(x[0])))
#     print(color(str(x[2])))
#     if str(x[1]) in ("http://www.w3.org/2002/07/owl#intersectionOf", "http://www.w3.org/2002/07/owl#unionOf"):
#         top = str(x[2])
#     if str(x[1]) == "http://www.w3.org/1999/02/22-rdf-syntax-ns#first":
#         #print("Line 1: ", x[0], x[1], x[2])
#         print()
#         print("Line 2: ", list(g.objects(x[2])))
#     if str(x[1]) not in ("http://www.w3.org/1999/02/22-rdf-syntax-ns#first", "http://www.w3.org/1999/02/22-rdf-syntax-ns#rest"):
#         print("Line 3: ", x[0], x[1], x[2])


# def isListNode(statements):
#     listPredicates = set([
#         "http://www.w3.org/1999/02/22-rdf-syntax-ns#first",
#         "http://www.w3.org/1999/02/22-rdf-syntax-ns#rest"
#     ])
#     return len(statements) == 2 && statements.forEach(quad=>
#                                  listPredicates.has(quad.predicate.value)
#
#




# def createDot(subjects):
#     declared = {}
#     allStatements = []
#     seen = set()
#     for ss in subjects:
#         print(ss)
#         seen.add(ss)
#         statements = g.triples((ss, None, None))
#     print(list(statements))



def createDot(selectedSubjects, graphStore, debug=False):
    def renderList(store, declared, ss, statements, includeSubjects):
        # implement this function if needed
        pass

    def declareTerm(declared, term, includeSubjects):
        # implement this function if needed
        pass

    def expand(subject):
        # implement this function if needed
        pass

    def shrink(uri):
        # implement this function if needed
        pass

    def updateGraph(dotText):
        # implement this function if needed
        pass

    def escapeDot(text):
        # implement this function if needed
        pass

    def isListNode(statements):
        # implement this function if needed
        pass

    rdf = rdflib.namespace.RDF
    subjectsToAdd = []
    for subject in selectedSubjects:
        subjectsToAdd.extend([rdflib.term.URIRef(subject), rdflib.term.BNode(subject)])
    includeSubjects =  False #document.querySelector("#subjects input").checked
    excludeTypes = False     #document.querySelector("#type input").checked
    declared = {}
    allStatements = []
    seen = set()
    rdfGraph = ""
    while subjectsToAdd:
        ss = subjectsToAdd.pop(0)
        seen.add(ss)
        statements = list(graphStore.triples((ss,None,None)))
        print(statements)
        if isListNode(statements):
            print(statements)
            text, listMembers = renderList(graphStore, declared, ss, statements, includeSubjects)
            rdfGraph += text
            list_term_type = rdflib.term.BNode if listMembers[0].find(":_") > -1 else rdflib.term.URIRef
            listMembers = [list_term_type(value) for value in listMembers]
            listMembers = filter(lambda value: value not in seen, listMembers)
            listMembers = list(filter(lambda term: term.find(":_") > -1, listMembers))
            subjectsToAdd.extend(listMembers)
        else:
            allStatements.extend(statements)

            blank_nodes = [statement_object for statement in statements for statement_object in [statement[2]] if
                      statement[2].term_type == 'BNode']
            blank_nodes = filter(lambda value: value not in seen, blank_nodes)
            subjectsToAdd.extend(list(blank_nodes))
    for quad in allStatements:
        subjectRef, objectRef, text = "", "", ""
        text, subjectRef = declareTerm(declared, quad.subject, includeSubjects)
        rdfGraph += text
        if not (excludeTypes and quad.predicate == rdf.type):
            text, objectRef = declareTerm(declared, quad.object, includeSubjects)
            rdfGraph += text
            rdfGraph += ' "%s" -> "%s" [label="%s"];\
 ' % (escapeDot(subjectRef), escapeDot(objectRef), shrink(quad.predicate.toPython()))
    if debug:
        print("rdfGraph", rdfGraph)
    legend = ""
    # if document.querySelector("#prefix input").checked:
    #     legend = createLegend()
    dotText = 'digraph { node [shape="box", style="rounded"]; rankdir="LR"; ratio="auto"; subgraph RDF { %s } %s }' % (
    rdfGraph, legend)
    if debug:
        print("dotText", dotText)
    updateGraph(dotText)

createDot([URIRef("https://ontologies.semanticarts.com/gist/PlannedEvent")], g)
