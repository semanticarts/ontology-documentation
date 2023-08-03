import sys

import jinja2
import pydotplus as pydotplus
from owlready2 import *
from itertools import chain
import subprocess
from zipfile import ZipFile, ZIP_DEFLATED
from lxml import etree
from string import Template
from rdflib import *
import rdflib

from rdflib import Graph, URIRef, BNode, Literal, Namespace
from rdflib.term import Node

from rdflib.namespace import RDF, RDFS
import argparse
from typing import Dict, List, Tuple
from pathlib import Path
from io import StringIO
from textwrap import wrap
import io


debug = True

###########START OF CLASS DIAGRAMS

Triple = Tuple[Node, Node, Node]
Triples = List[Triple]
class_images_path = r"./class_images/"

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
    ref = "\n".join(wrap(str(term.replace("\"", "`")), width=50))
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
  gist_iri="https://w3id.org/semanticarts/ns/ontology/gist/"
  g.bind("gist",rdflib.Namespace(gist_iri), override=True)
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
    if not (excludeTypes and (triple[1] == RDF.type or triple[1] == RDFS.isDefinedBy)):
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



# def visualize(g, root, output, **kwargs):
#       stream = io.StringIO()
#       createDot(g, stream, root, **kwargs)
#       output.write(stream.getvalue())

def create_class_image(g, root, output, exclude_types=True):
    import io

    def visualize(g, root, output_file, output_filename, **kwargs):
        stream = io.StringIO()
        createDot(g, stream, root, **kwargs)
        output_file.write(stream.getvalue())
        output_file.flush()
        output_file.close()
        print(" ".join(["dot", "-T", "png", output_filename + ".dot",  "-o", output_filename + ".png"]))
        result = subprocess.check_call(["dot", "-T", "png", output_filename + ".dot",  "-o", output_filename + ".png"], shell=True)
        print(result)

    # g = Graph()
    g_draw = Graph()
    # g.parse(rdf)

debug = False


###########START OF CLASS DIAGRAMS

Triple = Tuple[Node, Node, Node]
Triples = List[Triple]
class_images_path = r"./class_images/"

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
    ref = "\n".join(wrap(str(term), width=50))
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



# def visualize(g, root, output, **kwargs):
#       stream = io.StringIO()
#       createDot(g, stream, root, **kwargs)
#       output.write(stream.getvalue())

def create_class_image(g, root, output, exclude_types=True):
    import io

    def visualize(g, root, output_file, output_filename, **kwargs):
        stream = io.StringIO()
        createDot(g, stream, root, **kwargs)
        output_file.write(stream.getvalue())
        output_file.flush()
        output_file.close()
        print(" ".join(["dot", "-T", "png", output_filename + ".dot",  "-o", output_filename + ".png"]))
        result = subprocess.check_call(["dot", "-T", "png", output_filename + ".dot",  "-o", output_filename + ".png"], shell=True)
        print(result)

    # g = Graph()
    g_draw = Graph()
    # g.parse(rdf)
    gist = Namespace('https://ontologies.semanticarts.com/gist/')

    g.namespace_manager.bind('gist', gist)

    # https://ontologies.semanticarts.com/gist/PlannedEvent
    g_res = g.query(f'describe  <{root}> ')
    for t in g_res:
        g_draw.add(t)
    for ns, ns_uri in g.namespace_manager.namespaces():
        g_draw.namespace_manager.bind(ns, ns_uri)
    visualize(g_draw, URIRef(root),
      #      output if output else open(Path(rdf.name).with_suffix('.dot'), 'w'),
            open(Path(output).with_suffix('.dot'), 'w'),output,
            excludeTypes=exclude_types)

  ###########END OF CLASS DIAGRAMS

    # https://ontologies.semanticarts.com/gist/PlannedEvent
    g_res = g.query(f'describe  <{root}> ')
    for t in g_res:
        g_draw.add(t)
    for ns, ns_uri in g.namespace_manager.namespaces():
        g_draw.namespace_manager.bind(ns, ns_uri)
    visualize(g_draw, URIRef(root),
      #      output if output else open(Path(rdf.name).with_suffix('.dot'), 'w'),
            open(Path(output).with_suffix('.dot'), 'w'),output,
            excludeTypes=exclude_types)

  ###########END OF CLASS DIAGRAMS

import os

def path_exists(path):
    return os.path.exists(path)

func_dict = {
    "path_exists": path_exists
}

class NestedDefaultDict(defaultdict):
    def __init__(self, *args, **kwargs):
        super(NestedDefaultDict, self).__init__(NestedDefaultDict, *args, **kwargs)

    def __repr__(self):
        return repr(dict(self))


gist_ontology_file = './ontology/gistCore12.0.0.rdf'
ontologies_path = './ontology/'

d = defaultdict(list)
# set up the clustering of classes in the document

d["00090-Metadata"] = ["ControlledVocabulary", "Taxonomy", "Tag", "SchemaMetaData" ]
d["00091-Metadata_Predicates"] = ["tagText", "isSupersededBy"]
d["00100-Contact"] = ["Address", "ElectronicMessageAddress", "EmailAddress", "StreetAddress", "PostalAddress",
                      "TelephoneNumber"]
d["00101-Contact_Predicates"] = ["hasAddress", "hasCommunicationAddress"]
d["00200-Agreement"] = ["Account", "Agreement", "Balance", "Commitment", "ContingentObligation", "Contract",
                        "ContractTerm", "DegreeOfCommitment", "Obligation", "Offer", "Transaction"]
d["00201-Agreement_Predicates"] = ["hasParticipant", "hasParty", "hasGiver", "hasRecipient", "isTriggeredBy",
                                   "comesFromAgent", "goesToAgent", "isAffectedBy", "isUnderJurisdictionOf"]
d["00300-Category"] = ["Category", "Aspect"]
d["00301-Category_Predicates"] = ["hasDirectSuperCategory",
                                  "hasSuperCategory", "isCategorizedBy",
                                  "hasNavigationalParent", "hasUniqueSuperCategory", "hasUniqueNavigationalParent",
                                  "isAspectOf", "isCharacterizedAs"]
d["00400-Content"] = ["Content", "ContentExpression", "FormattedContent", "GeneralMediaType", "MediaType", "Medium",
                      "Message", "RenderedContent", "Text", "ID"]
d["00401-Content_Predicates"] = ["uniqueText", "encryptedText", "containedText", "isAbout",
                                 "isExpressedIn", "isRenderedOn"]
d["00500-Collection"] = ["Collection", "OrderedCollection", "OrderedMember"]
d["00501-Collection_Predicates"] = ["sequence", "providesOrderFor", "precedesDirectly", "hasMember",
                                    "hasFirstMember", "precedes"]
d["00600-Event"] = ["Event", "ContemporaryEvent", "ContingentEvent", "HistoricalEvent", "PhysicalEvent", "ScheduledEvent"]
d["00700-ID"] = ["ID"]
d["00701-ID_Predicates"] = ["isIdentifiedBy", "isAllocatedBy"]
d["00800-Task"] = ["Task", "Project", "ScheduledTask"]
d["00900-Specification"] = ["BundledCatalogItem", "CatalogItem", "ProductCategory", "ProductSpecification",
                            "Requirement", "Restriction", "ServiceSpecification", "Specification", "TaskTemplate", "Template", "ReferenceValue"]
d["01000-IoT"] = ["Actuator", "Controller", "ControllerType", "MessageDefinition", "PhenomenaType",
                  "PhysicalActionType", "Sensor"]
d["01001-IoT_Predicates"] = ["hasViableRange", "accepts", "respondsTo"]
d["01100-Magnitude"] = ["Volume", "Magnitude", "Area", "Count", "ElectricCurrent", "InformationQuantity",
                        "LuminousIntensity", "Mass", "MolarQuantity", "Monetary",  "ProductMagnitude",
                        "RatioMagnitude", "Temperature", "Duration", "Extent"]
d["01101-Magnitude_Predicates"] = ["hasPrecision", "hasMagnitude", "numericValue"]
d["01200-System"] = ["Component", "Equipment", "EquipmentType", "Function", "Network", "NetworkLink", "NetworkNode",
                     "System"]
d["01201-System_Predicates"] = ["contributesTo", "links", "linksFrom", "linksTo", "hasIncumbent"]
d["01300-Government"] = ["CountryGovernment", "GovernmentOrganization", "SubCountryGovernment",
                           "IntergovernmentalOrganization"]
d["01301-Government_Predicates"] = ["isGovernedBy", "isRecognizedDirectlyBy", "isRecognizedBy",
                                      "isUnderJurisdictionOf"]
d["01400-Place"] = ["GeoPoint", "Building", "GeoRoute", "GeoSegment", "GeoVolume", "Landmark", "Place", "GeoRegion",
                    "GovernedGeoRegion", "CountryGeoRegion"]
d["01401-Place_Predicates"] = ["latitude", "longitude","isGeographicallyContainedIn",
                                "occupiesGeographically", "hasPhysicalLocation",
                                "occupiesGeographicallyPermanently",
                               "hasAltitude", "goesToPlace", "comesFromPlace", "occursIn"]
d["01500-Human Behavior"] = ["Person", "Organization", "Behavior", "IntellectualProperty", "Intention", "Language", "Artifact", "Goal",
                             "Permission"]
d["01501-Human Behavior_Predicates"] = ["hasBiologicalParent", "hasGoal"]
d["01600-Date and Time"] = ["TemporalRelation", "TimeInterval"]
d["01601-Date and Time_Predicates"] = ["isRecordedAt", "atDateTime", "endDateTime",
                                       "actualEndDateTime", "actualEndDate", "deathDate", "actualEndMicrosecond",
                                       "actualEndMinute", "actualEndYear", "plannedEndDateTime", "plannedEndDate",
                                       "plannedEndMinute", "plannedEndYear",
                                       "startDateTime", "actualStartDateTime", "actualStartDate", "birthDate",
                                       "actualStartMicrosecond", "actualStartMinute", "actualStartYear",
                                       "plannedStartDateTime", "plannedStartDate",
                                       "plannedStartMinute", "plannedStartYear"]
d["01700-Physical World"] = ["PhysicalIdentifiableItem", "PhysicalSubstance", "LivingThing"]
d["01800-Unit"] = ["VolumeUnit", "UnitOfMeasure", "SimpleUnitOfMeasure", "ProductUnit", "AreaUnit", "CountingUnit",
                   "CurrencyUnit", "CurrencyPerDurationUnit", "MonetaryPerDuration", "DataSizeUnit", "ElectricalCurrentUnit", "LuminousIntensityUnit", "MoleUnit",
                   "RatioUnit", "TemperatureUnit", "CoherentProductUnit", "CoherentRatioUnit", "CoherentUnit",
                   "BaseUnit", "DistanceUnit", "DurationUnit", "MassUnit"]
d["01801-Unit_Predicates"] = ["conversionOffset", "conversionFactor", "unitSymbol", "unitSymbolHtml",
                              "unitSymbolUnicode", "hasUnitOfMeasure", "hasDenominator", "hasBaseUnit",
                              "hasStandardUnit", "hasMultiplicand", "hasMultiplier", "hasNumerator"]
d["01901-Partitive_Predicates"] = ["hasDirectPart", "hasPart", "hasMember",
                                   "isMadeUpOf"]
d["02001-Annotation_Predicates"] = ["rangeIncludes", "domainIncludes", "license"]
d["02101-General Description_Predicates"] = ["description", "name"]
d["02101-General Relationship_Predicates"] = ["precedes", "prevents", "owns",  "allows",
                                 "directs", "requires", "conformsTo", "isConnectedTo", "isBasedOn",
                                 "produces"]


templateString = """
{% for section, classes in d.items() %}
{% if "_Predicates" in section %}
## <a id="{{ section[6:]|replace("_"," ")|lower }}">{{ section[6:]|replace("_"," ") }}</a>
{% else %}
# <a id="{{ section[6:]|replace("_"," ")|lower }}">{{ section[6:]|replace("_"," ") }}</a>
{% endif %}

{% for itm1, itm in classes.items() %}
{% if "_Predicates" in section %}
### <a id="{{ itm.class|replace(".","")|replace("_","")|replace(":","")|lower }}-identifier">{{ itm.class|replace("gist.","gist:") }}</a>
{% else %}
## <a id="{{ itm.class|replace(".","")|replace("_","")|replace(":","")|lower }}-identifier">{{ itm.class|replace("gist.","gist:") }}</a>
{% endif %}


{% set myfile =  './class_images/' + itm.class.replace("gist.","").replace("gist:","") + '.png' %}
{% if path_exists(myfile) %}
![](./class_images/{{itm.class|replace("gist.","")|replace("gist:","")}}.png)
{% endif %}
=======
![{{itm.class|replace("gist.","")|replace("gist:","")}}](./class_images/{{itm.class|replace("gist.","")|replace("gist:","")}}.png)


{% if itm.pref_label %}**Preferred Label** {{ itm.pref_label }}{% endif %}

{% if itm.definition %}**Definition** {{ itm.definition }}{% endif %}

{% if itm.example %}**Example** {{ itm.example }}{% endif %}

{% if itm.scope_note %}**Scope Note** {{ itm.scope_note }}{% endif %}

{% if itm.subclasses%}**Subclasses** {{ itm.subclasses|replace("gist.","gist:") }}{% endif %}

{% if itm.equivalent_class %}**EquivalentTo** {{ itm.equivalent_class|replace("gist.","gist:")|replace(".only", " only ")|replace("|", "or")|replace("&", "and")|replace(".value"," value ")|replace(".exactly"," exactly ")|replace(".some"," some ")|replace(".min"," min ")|replace(".max"," max ")|replace("[","")|replace("]","") }}{% endif %}

{% if itm.domain_of %}**Domain Of** {{ itm.domain_of|replace("gist.","gist:") }}{% endif %}

{% if itm.range_of %}**Range Of** {{ itm.range_of|replace("gist.","gist:") }}{% endif %}

{% if itm.disjoints %}**Disjoint With** {{ itm.disjoints|replace("gist.","gist:") }}{% endif %}

{% endfor %}
&nbsp;
{% endfor %}

"""
##{{itm.class|replace("gist.","")|replace("gist:","")}}
onto_path.append(ontologies_path)
onto = get_ontology(gist_ontology_file)
onto.load()
gist = onto.get_namespace("https://w3id.org/semanticarts/ns/ontology/gist/")
owl = onto.get_namespace("http://www.w3.org/2002/07/owl#")
rdf = onto.get_namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
rdfs = onto.get_namespace("http://www.w3.org/2000/01/rdf-schema#")
skos = onto.get_namespace("http://www.w3.org/2004/02/skos/core#")
xml = onto.get_namespace("http://www.w3.org/XML/1998/namespace")
xsd = onto.get_namespace("http://www.w3.org/2001/XMLSchema#")


#skos_file = 'http://www.w3.org/2004/02/skos/core'
#skos_file_local = './ontology/skos.rdf'
#skos_onto = get_ontology(skos_file_local).load()
#onto.imported_ontologies.append(skos_onto)

prefLabel = skos.prefLabel
definition = skos.definition
example = skos.example
scopeNote = skos.scopeNote

classes = list(onto.classes())
graph = default_world.as_rdflib_graph()

print(list(graph.namespace_manager.namespaces()))
print(len(graph))
for x in classes:
    root = str(x.iri)
    output_filename = class_images_path + str(x).split(".")[1]
    output = open(Path(output_filename).with_suffix('.dot'), 'w', encoding='utf-8')
    print(output_filename, root)
    create_class_image(graph, root, output_filename)

if debug: print("classes:  ", classes)

object_properties = list(onto.object_properties())
if debug: print("object_properties:   ", object_properties)
data_properties = list(onto.data_properties())
if debug: print("data_properties:   ", data_properties)
disjoint_classes = list(onto.disjoint_classes())
if debug: print("disjoint_classes:    ", disjoint_classes)
disjoint_properties = list(onto.disjoint_properties())
if debug: print("disjoint_properties:    ", disjoint_properties)
annotation_properties = list(onto.annotation_properties())
if debug: print("annotation_properties:    ", annotation_properties)
general_axioms = list(onto.general_axioms())
if debug: print("general_axioms:    ", general_axioms)
equivalent_classes = []
for i in onto.classes():
    eq_class = i.equivalent_to
    if eq_class: equivalent_classes.append((i, eq_class))
if debug: print("equivalent_classes:    ", equivalent_classes)

propertiesWithClassAsRange = defaultdict(list)
for p in object_properties:
    for x in p.range:
        [propertiesWithClassAsRange[z.strip()].append(p) for z in str(x).split("|")]
propertiesWithClassAsDomain = defaultdict(list)
for p in object_properties:
    for x in p.domain:
        [propertiesWithClassAsDomain[z.strip()].append(p) for z in str(x).split("|")]


def match():
    includedClasses = []
    missingClasses = []
    s = None
    for k in d.keys():
        for c in d[k]:
            if c: s = onto.search(iri="*" + c)
            if s:
                includedClasses.append(c)
            else:
                missingClasses.append(c)


    print("In the ontology:  ", includedClasses)
    print("Not in the ontology:  ", missingClasses)


def match_v2():
    properties_in_template = []
    classes_in_template = []
    for key in d.keys():
        if not "Predicates" in key:
            classes_in_template.append(d[key])
        else:
            properties_in_template.append(d[key])
    onto_classes = [x.name for x in list(onto.classes())]
    onto_properties = [x.name for x in list(onto.properties())]
    classes_in_template_set = set(list(chain.from_iterable(classes_in_template)))
    onto_classes_set = set(onto_classes)
    properties_in_template_set = set(list(chain.from_iterable(properties_in_template)))
    onto_properties_set = set(onto_properties)
    classes_in_template_only = classes_in_template_set - onto_classes_set
    properties_in_template_only = properties_in_template_set - onto_properties_set
    print("items in template but not in ontology")
    print("classes:  ", classes_in_template_only)
    print("properties:  ", properties_in_template_only)
    classes_in_ontology_only = onto_classes_set - classes_in_template_set
    properties_in_ontology_only = onto_properties_set - properties_in_template_set
    print("items in ontology but not in template")
    print("classes:  ", classes_in_ontology_only)
    print("properties:  ", properties_in_ontology_only)



def link_up(s):
    s1 = s.replace("gist.", "gist:")
    s2 = "".join([c if c.isalnum() else "" for c in s1]).lower()
    return f"[{s1}](#{s2}-identifier)"


# #find prefLabel
template_data = NestedDefaultDict()

def get_label(entity):
    """Returns the label of an entity."""
    if hasattr(entity, "prefLabel") and entity.prefLabel:
        return entity.prefLabel.first()
    if hasattr(entity, "label") and entity.label:
        return entity.label.first()
    if hasattr(entity, "__name__"):
        return entity.__name__
    if hasattr(entity, "name"):
        return str(entity.name)
    if isinstance(entity, str):
        return entity
    return repr(entity)


# def get_definition(entity):
#     """Returns the label of an entity."""
#     if hasattr(entity, "definition") and entity.definition:
#         return entity.definition.first()
#     return ''

# def get_definition(entity):
#     """Returns the definition of an entity."""
#     print(entity)
#     if hasattr(entity, "definition") and entity.definition:
#         return entity.definition.first()
#     return ''

def get_definition(entity):
    """Returns the definition of an entity."""
    i = entity.name
    myIRI = f"<https://w3id.org/semanticarts/ns/ontology/gist/{i}>"
    try:
        results = default_world.sparql("""SELECT *
                   { """ + myIRI + """ <http://www.w3.org/2004/02/skos/core#prefLabel> ?prefLabel .
                   OPTIONAL { """ + myIRI + """ <http://www.w3.org/2004/02/skos/core#definition> ?definition . }
                   }
            """, error_on_undefined_entities=False)
        if results:
            d = next(results)
            return d[1]
    except Exception as e:
        print(e)
        return ''




# def get_example(entity):
#     """Returns the example of an entity."""
#     if hasattr(entity, "example") and entity.example:
#         return entity.example.first()
#     return ''

def get_example(entity):
    """Returns the example of an entity."""
    i = entity.name
    myIRI = f"<https://w3id.org/semanticarts/ns/ontology/gist/{i}>"
    try:
        results = default_world.sparql("""SELECT *
                   { """ + myIRI + """ <http://www.w3.org/2004/02/skos/core#prefLabel> ?prefLabel .
                   OPTIONAL { """ + myIRI + """ <http://www.w3.org/2004/02/skos/core#example> ?example . }
                   }
            """, error_on_undefined_entities=False)
        if results:
            d = next(results)
            return d[1]
    except Exception as e:
        print(e)
        return ''

# def get_scopeNote(entity):
#     """Returns the scope note of an entity."""
#     if hasattr(entity, "scopeNote") and entity.scopeNote:
#         return entity.scopeNote.first()
#     return ''

def get_scopeNote(entity):
    """Returns the scopeNote of an entity."""
    i = entity.name
    myIRI = f"<https://w3id.org/semanticarts/ns/ontology/gist/{i}>"
    try:
        results = default_world.sparql("""SELECT *
                   { """ + myIRI + """ <http://www.w3.org/2004/02/skos/core#prefLabel> ?prefLabel .
                   OPTIONAL { """ + myIRI + """ <http://www.w3.org/2004/02/skos/core#scopeNote> ?scopeNote . }
                   }
            """, error_on_undefined_entities=False)
        if results:
            d = next(results)
            return d[1]
    except Exception as e:
        print(e)
        return ''



def get_the_info(i):
    print("Getting the info")
    print(i)
    print("properties for ", str(i), "  :   ", list(i.get_properties(i)))
    template_data_ = {}
    template_data_["class"] = str(i)
    template_data_["pref_label"] = get_label(i)  #prefLabel[i].first() or ""
    template_data_["definition"] = get_definition(i)  #definition[i].first() or ""
    template_data_["example"] = get_example(i)  #example[i].first() or ""
    template_data_["scope_note"] = get_scopeNote(i)  #scopeNote[i].first() or ""
    # print("Class properties:  ", [(x, "Domain:  ", x.domain, "Range: ", x.range) for x in i.get_class_properties() if ('gist' in x.iri)])
    # myTemplate["Class properties"] = [x for x in i.get_class_properties() if (str(i) in str(x.range))]
    # myTemplate["Class properties"] = [x for x in i.get_class_properties() if (str(i) in str(x.domain))]
    try:
        # print("SC:" ,onto.search(subclass_of=i))
        template_data_["subclasses"] = ", ".join([link_up(str(i)) for i in list(i.subclasses()) if i]) or ""
    except Exception as e:
        print(e)
        # continue
    try:
        template_data_["equivalent_class"] = i.equivalent_to
    except Exception as f:
        print(f)
        # continue
    propertiesThatHaveClassAsDomain = propertiesWithClassAsDomain[str(i)]
    template_data_["domain_of"] = ", ".join([link_up(str(i)) for i in propertiesThatHaveClassAsDomain]) or ""
    propertiesThatHaveClassAsRange = propertiesWithClassAsRange[str(i)]
    template_data_["range_of"] = ", ".join([link_up(str(i)) for i in propertiesThatHaveClassAsRange]) or ""
    dj = list(i.disjoints())

    djs = []
    [djs.append(dj_.entities) for dj_ in dj]
    flat_list = chain.from_iterable(djs)
    actual_disjoints = set(flat_list) - set([i])
    template_data_["disjoints"] = ", ".join([link_up(str(i)) for i in actual_disjoints if i]) or ""
    return template_data_



def getPredicateInfo(i):
    template_data_ = {}
    myIRI = f"<https://w3id.org/semanticarts/ns/ontology/gist/{i}>"
    try:
        results = default_world.sparql("""SELECT *
                   { """ + myIRI + """ <http://www.w3.org/2004/02/skos/core#prefLabel> ?prefLabel .
                   OPTIONAL { """ + myIRI + """ <http://www.w3.org/2004/02/skos/core#definition> ?definition . }
                   }
            """, error_on_undefined_entities=False)
        template_data_["class"] = f"gist:{i}"

        if results:
            d = next(results)
            template_data_["pref_label"] = d[0]
            template_data_["definition"] = d[1]

    except Exception as e:
        print(e)
    return template_data_


def get_imports():
    imports_table = ''
    if onto.imported_ontologies:
        ontology_imports = []
        for imp in onto.imported_ontologies:
            ontology_imports.append(str(imp))
        imports_table += '\n\n# <a id="ontology-imports">Imports</a>\n'
        imports_table += "|import| \n"
        imports_table += "|-|\n"
        for x in ontology_imports:
            imports_table += f"|{x}|\n"
    return imports_table

imported_ontologies = ''

def get_imported_ontologies(recursive=False):
    """Return a list with imported ontologies.

    If `recursive` is `True`, ontologies imported by imported ontologies
    are also returned.
    """

    def rec_imported(onto):
        for ontology in onto.imported_ontologies:
            if ontology not in imported:
                imported.add(ontology)
                rec_imported(ontology)

    if recursive:
        imported = set()
        rec_imported(onto)
        return list(imported)

    return imported_ontologies

def get_metrics():
    # ontology metrics
    individuals = set()
    for c in onto.classes():
        for i in c.instances():
            individuals.add(i)

    metrics = {}
    metrics_table = ''

    metrics["General"] = {}
    metrics["General"]["Classes"] = len(classes)
    metrics["General"]["Axioms"] = len(general_axioms)
    metrics["General"]["Object Properties"] = len(object_properties)
    metrics["General"]["Data Properties"] = len(data_properties)
    metrics["General"]["Annotation Properties"] = len(annotation_properties)
    metrics["General"]["Individuals"] = len(individuals)

    metrics["Class Axioms"] = {}
    metrics["Class Axioms"]["Subclass Of"] = list(default_world.sparql("""
               SELECT (COUNT(?x) AS ?c)
               { ?x rdfs:subClassOf ?s . FILTER(ISIRI(?x)). }
                """))[0][0]
    metrics["Class Axioms"]["Equivalent Classes"] = len(equivalent_classes)
    metrics["Class Axioms"]["Disjoint Classes"] = len(disjoint_classes)

    metrics["Property Axioms"] = {}
    metrics["Property Axioms"]["Subproperty Of"] = list(default_world.sparql("""
               SELECT (COUNT(?x) AS ?c)
               { ?x rdfs:subPropertyOf ?s . }
                """))[0][0]
    metrics["Property Axioms"]["Disjoint Properties"] = len(disjoint_properties)
    metrics_table += '\n\n# <a id="ontology-metrics">Metrics</a>\n'
    metrics_table += '## For The <<{}>> Ontology\n\n'.format(onto.base_iri)
    metrics_table += "|Metric Type|Count| \n"
    metrics_table += "|-|-| \n"

    for category, metric in metrics.items():
        metrics_table += '| **{}** ||'.format(category) + '\n'
        for value, count in metric.items():
            metrics_table += '|{}|{}|'.format(value, count) + '\n'
    return metrics_table

    def match():
        includedClasses = []
        missingClasses = []
        for k in d.keys():
            for c in d[k]:
                if c: s = onto.search(iri="*" + c)
                if s:
                    includedClasses.append(c)
                else:
                    missingClasses.append(c)

    #    print(includedClasses)
    #    print(missingClasses)


def create_documentation(output_file=sys.stdout):
    for k in d.keys():
        for l in d[k]:
            if debug:  print(l)
            if "_" in k:
                template_data[k][str(l)] = getPredicateInfo(l)
            else:
                myIRI = onto.search_one(iri=gist.base_iri + l)
                print("myIRI:  ", myIRI)
                print(gist.base_iri)
                print(l)
                print(gist.base_iri + l)
                if (myIRI != None):
                    template_data[k][str(myIRI)] = get_the_info(myIRI)

    output = ''
    for k in sorted(d.keys()):
        toPrinter = {k: template_data[k]}
        t = jinja2.Template(templateString)
        t.globals.update(func_dict)
        output += t.render(d=toPrinter)
    imports_table = get_imports()
    metrics_table = get_metrics()
    print(imports_table, file=output_file)
    print(metrics_table, file=output_file)
    print(output, file=output_file)

def run_pandoc(output_ebook, input_markdown, metadata_yaml, book_title):
    title="title=" + book_title

    #result = subprocess.check_call(["pandoc", "-S", "--toc", "-o", output_ebook, metadata_yaml, input_markdown, "-M" "title=", book_title], shell=True)
    result = subprocess.check_call(
        ["pandoc",  "--toc", "-o", output_ebook, metadata_yaml, input_markdown, "-M", title],
        shell=True)
    return result


def sort_hyperlinks(f, fout):
    infile = ZipFile(f)
    outfile = ZipFile(fout, "w", ZIP_DEFLATED)

    # load up the locations
    nav = infile.read("EPUB/nav.xhtml")
    xmldoc = etree.fromstring(nav)
    dict = {}
    for link in xmldoc.xpath('//x:a/@href', namespaces={"x":"http://www.w3.org/1999/xhtml"}):
        if "/" in link:
            split_link = link.split("/")
            dict[split_link[1]] = split_link[0]
        if "#" in link:
            split_link = link.split("#")
            dict[split_link[1]] = split_link[0]
    #print(dict["gistemailaddress"])

    for f in infile.infolist():

        if "ch0" in f.filename:
            newfile = infile.read(f.filename)
            print("type:   ", type(newfile))
            for x in dict.keys():
            # newfile = str(newfile).replace("a href=\"#" + x + "-identifier", "a href=\"" + str(dict[x]) + "#" + str(x) ).replace("\\n"," ").replace("\\xc2\\xa0"," ").replace("\\xe2\\x80\\x98", "'").replace("\\xe2\\x80\\x99","'").replace("\\xe2\\x80\\x9","-")
                newfile = newfile.replace(bytes(("a href=\"#" + x + "-identifier").encode('utf-8')), bytes(("a href=\"").encode('utf-8')) + (dict[x]).encode('utf-8') + bytes(("#" + x).encode('utf-8')))##.replace("\\n"," ").replace("\\xc2\\xa0"," ").replace("\\xe2\\x80\\x98", "'").replace("\\xe2\\x80\\x99","'").replace("\\xe2\\x80\\x9","-")

            #print("type_:   ", type(newfile))


            outfile.writestr(f.filename, newfile)
        else:
            newfile = infile.read(f.filename)
            outfile.writestr(f.filename, newfile)


def test_this_out():
    import os

    input_markdown = r'.\output\2023-08-03_gist_12.0.0.md'
    output_ebook = r'.\output\2023-08-03_gist_12.0.0.md.epub'
    output_ebook_sorted_links = r'.\output\2023-08-03_gist_12.0.0.md.sorted.epub'
    metadata_yaml = r'C:/Users/Pedro/PycharmProjects/ontology-documentation/figures.etc/metadata.yaml'
    css = r'C:/Users/Pedro/PycharmProjects/ontology-documentation/figures.etc/epub.css'

    book_title = "The Zest of gist"
    cwd = os.getcwd()
    os.chdir(r'c:\Users\Pedro\PycharmProjects\ontology-documentation')


    output = open(input_markdown, 'w')
    create_documentation(output_file=output)
    output.close()
    if run_pandoc(output_ebook, input_markdown, metadata_yaml, book_title) == 0:
        sort_hyperlinks(output_ebook, output_ebook_sorted_links)
    print("Finished")



if __name__ == "__main__":
    test_this_out()