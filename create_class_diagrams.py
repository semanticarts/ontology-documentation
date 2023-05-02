from rdflib import Graph, URIRef, BNode, Literal, Namespace
from rdflib.term import Node
from rdflib.namespace import RDF
import argparse
from typing import Dict, List, Tuple
from pathlib import Path
from io import StringIO
from textwrap import wrap

Triple = Tuple[Node, Node, Node]
Triples = List[Triple]

def listNode(statements: Triples) -> bool:
    return len(statements) == 2 and all(s[1] in [RDF.first, RDF.rest] for s in statements)


def color(o):
    if isinstance(o, (URIRef)):
        return "BLACK"
    if isinstance(o, (BNode)):
        return "ORANGE"
    if isinstance(o, (Literal)):
        return "BLUE"
    return "BLACK"

def qname(x: URIRef, g: Graph) -> str:
    try:
        q = g.compute_qname(x, generate=False)
        return q[0] + ":" + q[2]
    except:
        return str(x)


def declareTerm(g: Graph, declared: Dict[URIRef, str], term: URIRef) -> Tuple[str, str]:
  if term in declared:
    return '', declared[term]
  declaration = ''
  ref = str(term)
  attributes = []
  if isinstance(term, Literal):
    ref = wrap(str(term), width=50)
    attributes.append('color="blue"')
  elif isinstance(term, BNode):
    attributes.extend(('color="orange"', 'shape="point"', 'width="0.2"'))
  else:
    ref = qname(term, g)

  declared[term] = ref
  declaration = f'   "{ref}" [{";".join(attributes)}];\n'

  return [declaration, ref]



def renderList(g: Graph,
                declared: dict,
                head: URIRef,
                statements: Triples) -> Tuple[str, List[URIRef]]:
  listMembers = []
  while True:
    headNode = next(s[2] for s in statements if s[1] == RDF.first)
    listMembers.append(headNode);
    nextNode = next(s[2] for s in statements if s[1] == RDF.rest)
    if (nextNode == RDF.nil):
      break
    statements = list(g.triples((nextNode, None, None)))

  [dotText, listRef] = declareTerm(g, declared, head)
  memberRefs = []
  for member in listMembers:
    memberText, memberRef = declareTerm(g, declared, member)
    dotText += memberText
    memberRefs.append(memberRef)

  attributes = [
    'shape=record',
    f'label="{"|".join(f"<p{m}>" for m in range(len(memberRefs)))}"'
  ]
  dotText += f'   "{listRef}" [{",".join(attributes)}];\n ';
  dotText += "\n".join(f'"{listRef}":p{i} -> "{m}" ;' for i, m in enumerate(memberRefs))

  return dotText, listMembers


def createDot(g: Graph, stream: StringIO, root: URIRef, **kwargs) -> str:
  subjectsToAdd = [root]
  excludeTypes = kwargs.get('excludeTypes', False)
  declared = {}
  allStatements = []
  seen = set()
  rdfGraph = ''
  while subjectsToAdd:
    ss = subjectsToAdd.pop(0)
    seen.add(ss)
    statements = list(g.triples((ss, None, None)))
    if listNode(statements):
      [text, listMembers] = renderList(g, declared, ss, statements)
      rdfGraph += text
      subjectsToAdd.extend(ls for ls in listMembers if isinstance(ls, BNode) and not ls in seen)
    else:
      allStatements.extend(statements)
      subjectsToAdd.extend(s[2] for s in statements if isinstance(s[2], BNode) and not s[2] in seen)

  for triple in allStatements:
    [text, subjectRef] = declareTerm(g, declared, triple[0]);
    rdfGraph += text
    if not (excludeTypes and triple[1] == RDF.type):
      [text, objectRef] = declareTerm(g, declared, triple[2])
      rdfGraph += text;
      rdfGraph += f'  "{subjectRef}" -> "{objectRef}"  [label="{qname(triple[1], g)}"];\n '

  stream.write(f"""digraph {{
    node [shape="box", style="rounded"];
    rankdir="LR"; ratio="auto";
    subgraph RDF {{
      {rdfGraph}
    }}
  }}""")

def run_main(rdf, root, output, exclude_types):
    import io


    def visualize(g, root, output, **kwargs):
        stream = io.StringIO()
        createDot(g, stream, root, **kwargs)
        output.write(stream.getvalue())


    # parser = argparse.ArgumentParser()
    # parser.add_argument("rdf", type=argparse.FileType("r"), help="RDF content to visualize")
    # parser.add_argument("root", action="store", help="URL of visualization root")
    # parser.add_argument("--exclude-types", action="store_true", help="Suppress rdf:type triples")
    # parser.add_argument("-o", "--output", type=argparse.FileType("w"), help="DOT file to create")
    # args = parser.parse_args()

    g = Graph()
    g_draw = Graph()
    g.parse(rdf)
    gist = Namespace('https://ontologies.semanticarts.com/gist/')

    g.namespace_manager.bind('gist', gist)

    # https://ontologies.semanticarts.com/gist/PlannedEvent
    g_res = g.query(f'describe  <{root}> ')
    for t in g_res:
        g_draw.add(t)
    for ns, ns_uri in g.namespace_manager.namespaces():
        g_draw.namespace_manager.bind(ns, ns_uri)
    visualize(g_draw, URIRef(root),
              output if output else open(Path(rdf.name).with_suffix('.dot'), 'w'),
              excludeTypes=exclude_types)

if __name__ == "__main__":
    import io



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
    rdf = io.StringIO(ttl)
    rdf.name = "PlannedEvent"
    root = "https://ontologies.semanticarts.com/gist/PlannedEvent"
    output = False
    exclude_types = True

    run_main(rdf, root, output, exclude_types)



