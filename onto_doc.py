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

debug = False


class NestedDefaultDict(defaultdict):
    def __init__(self, *args, **kwargs):
        super(NestedDefaultDict, self).__init__(NestedDefaultDict, *args, **kwargs)

    def __repr__(self):
        return repr(dict(self))


gist_ontology_file = './ontology/v11.1.gistCore.owl'
ontologies_path = './ontology/'

d = defaultdict(list)
# set up the clustering of classes in the document

d["00100-Contact"] = ["Address", "ElectronicMessageAddress", "EmailAddress", "StreetAddress", "PostalAddress",
                      "TelephoneNumber"]
d["00101-Contact_Predicates"] = ["hasAddress", "hasCommunicationAddress"]
d["00200-Agreement"] = ["Account", "Agreement", "Balance", "Commitment", "ContingentObligation", "Contract",
                        "ContractTerm", "DegreeOfCommitment", "Obligation", "Offer", "Transaction"]
d["00201-Agreement_Predicates"] = ["hasParticipant", "hasParty", "hasGiver", "hasRecipient", "isTriggeredBy",
                                   "comesFromAgent", "goesToAgent", "isAffectedBy", "isUnderJurisdictionOf"]
d["00300-Category"] = ["Category", "ControlledVocabulary", "Tag", "Taxonomy", "Aspect"]
d["00301-Category_Predicates"] = ["hasDirectSubCategory", "hasSubCategory", "hasDirectSuperCategory",
                                  "hasSuperCategory", "isCategorizedBy", "hasNavigationalChild",
                                  "hasNavigationalParent", "hasUniqueSuperCategory", "hasUniqueNavigationalParent",
                                  "isAspectOf", "isCharacterizedAs"]
d["00400-Content"] = ["Content", "ContentExpression", "FormattedContent", "GeneralMediaType", "MediaType", "Medium",
                      "Message", "RenderedContent", "Text", "ID", "SchemaMetaData"]
d["00401-Content_Predicates"] = ["tagText", "uniqueText", "encryptedText", "containedText", "isAbout", "isDescribedIn",
                                 "isExpressedIn", "isRenderedOn"]
d["00500-Collection"] = ["Collection", "OrderedCollection", "OrderedMember"]
d["00501-Collection_Predicates"] = ["sequence", "providesOrderFor", "followsDirectly", "precedesDirectly", "hasMember",
                                    "hasFirstMember", "isMemberOf", "precedes"]
d["00600-Event"] = ["Event", "ContemporaryEvent", "ContingentEvent", "HistoricalEvent", "PhysicalEvent", "PlannedEvent"]
d["00700-ID"] = ["ID"]
d["00701-ID_Predicates"] = ["identifies", "isIdentifiedBy", "isAllocatedBy"]
d["00800-Task"] = ["TaskExecution", "ProjectExecution", "ScheduledTaskExecution"]
d["00801-Task_Predicates"] = ["hasDirectSubTask", "hasSubTask", "isDirectSubTaskOf", "isSubTaskOf"]
d["00900-Specification"] = ["BundledCatalogItem", "CatalogItem", "ProductCategory", "ProductSpecification",
                            "Requirement", "Restriction", "ServiceSpecification", "Specification", "TaskTemplate", "Template", "ReferenceValue"]
d["01000-IoT"] = ["Actuator", "Controller", "ControllerType", "MessageDefinition", "PhenomenaType",
                  "PhysicalActionType", "Sensor"]
d["01001-IoT_Predicates"] = ["hasViableRange", "accepts", "respondsTo"]
d["01100-Magnitude"] = ["Volume", "VolumeUnit", "Magnitude", "Area", "Count", "ElectricCurrent", "InformationQuantity",
                        "LuminousIntensity", "Mass", "MolarQuantity", "Monetary", "Percentage", "ProductMagnitude",
                        "RatioMagnitude", "Temperature", "Duration", "Extent"]
d["01101-Magnitude_Predicates"] = ["hasPrecision", "hasMagnitude", "numericValue"]
d["01200-System"] = ["Component", "Equipment", "EquipmentType", "Function", "Network", "NetworkLink", "NetworkNode",
                     "System"]
d["01201-System_Predicates"] = ["contributesTo", "links", "linksFrom", "linksTo"]
d["01300-Organization"] = ["CountryGovernment", "GovernmentOrganization", "SubCountryGovernment",
                           "IntergovernmentalOrganization", "TreatyOrganization", "Organization"]
d["01301-Organization_Predicates"] = ["governs", "isGovernedBy", "isRecognizedDirectlyBy", "isRecognizedBy",
                                      "recognizes", "hasIncumbent", "isUnderJurisdictionOf"]
d["01400-Place"] = ["GeoPoint", "Building", "GeoRoute", "GeoSegment", "GeoVolume", "Landmark", "Place", "GeoRegion",
                    "GovernedGeoRegion", "CountryGeoRegion"]
d["01401-Place_Predicates"] = ["latitude", "longitude", "containsGeographically", "isGeographicallyContainedIn",
                               "isGeographicallyOccupiedBy", "occupiesGeographically", "hasPhysicalLocation",
                               "isGeographicallyPermanentlyOccupiedBy", "occupiesGeographicallyPermanently",
                               "hasAltitude", "goesToPlace", "comesFromPlace", "occursIn"]
d["01500-Human Behavior"] = ["Person", "Behavior", "IntellectualProperty", "Intention", "Language", "Artifact", "Goal",
                             "Permission"]
d["01501-Human Behavior_Predicates"] = ["hasBiologicalParent", "hasGoal"]
d["01600-Date-and-Time"] = ["TimeZone", "TimeZoneStandard", "TemporalRelation"]
d["01601-Date-and-Time_Predicates"] = ["hasOffsetToUniversal", "isRecordedAt", "atDateTime", "endDateTime",
                                       "actualEndDateTime", "actualEndDate", "deathDate", "actualEndMicrosecond",
                                       "actualEndMinute", "actualEndYear", "plannedEndDateTime", "plannedEndDate",
                                       "plannedEndMinute", "plannedEndYear",
                                       "startDateTime", "actualStartDateTime", "actualStartDate", "birthDate",
                                       "actualStartMicrosecond", "actualStartMinute", "actualStartYear",
                                       "plannedStartDateTime", "plannedStartDate",
                                       "plannedStartMinute", "plannedStartYear", "usesTimeZoneStandard"]
d["01700-Physical World"] = ["PhysicalIdentifiableItem", "PhysicalSubstance", "LivingThing"]
d["01800-Unit"] = ["VolumeUnit", "UnitOfMeasure", "SimpleUnitOfMeasure", "ProductUnit", "AreaUnit", "CountingUnit",
                   "CurrencyUnit", "DataSizeUnit", "ElectricalCurrentUnit", "LuminousIntensityUnit", "MoleUnit",
                   "RatioUnit", "TemperatureUnit", "CoherentProductUnit", "CoherentRatioUnit", "CoherentUnit",
                   "BaseUnit", "DistanceUnit", "DurationUnit", "MassUnit"]
d["01801-Unit_Predicates"] = ["conversionOffset", "conversionFactor", "unitSymbol", "unitSymbolHtml",
                              "unitSymbolUnicode", "hasUnitOfMeasure", "hasDenominator", "hasBaseUnit",
                              "hasStandardUnit", "hasMultiplicand", "hasMultiplier", "hasNumerator"]
d["01901-Partitive_Predicates"] = ["hasDirectPart", "hasPart", "isDirectPartOf", "hasMember", "isMemberOf", "isPartOf",
                                   "isMadeUpOf"]
d["02001-Annotation_Predicates"] = ["rangeIncludes", "domainIncludes", "license"]
d["02101-General Description_Predicates"] = ["description", "name"]
d["02101-General Relationship_Predicates"] = ["precedes", "prevents", "owns", "affects", "allows",
                                 "directs", "requires", "conformsTo", "isConnectedTo", "isBasedOn",
                                 "isBasisFor", "follows", "produces"]


templateString = """
{% for section, classes in d.items() %}
# <a id="{{ section[6:]|replace("_"," ")|lower }}">{{ section[6:]|replace("_"," ") }}</a>

{% for itm1, itm in classes.items() %}
## <a id="{{ itm.class|replace(".","")|replace("_","")|replace(":","")|lower }}-identifier">{{ itm.class|replace("gist.","gist:") }}</a>

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

onto_path.append(ontologies_path)
onto = get_ontology(gist_ontology_file)

gist = onto.get_namespace("https://ontologies.semanticarts.com/gist/")
owl = onto.get_namespace("http://www.w3.org/2002/07/owl#")
rdf = onto.get_namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
rdfs = onto.get_namespace("http://www.w3.org/2000/01/rdf-schema#")
skos = onto.get_namespace("http://www.w3.org/2004/02/skos/core#")
xml = onto.get_namespace("http://www.w3.org/XML/1998/namespace")
xsd = onto.get_namespace("http://www.w3.org/2001/XMLSchema#")

onto.load()
skos_file = 'http://www.w3.org/2004/02/skos/core'
skos_file_local = './ontology/skos.rdf'
skos_onto = get_ontology(skos_file_local).load()
onto.imported_ontologies.append(skos_onto)
prefLabel = skos.prefLabel
definition = skos.definition
example = skos.example
scopeNote = skos.scopeNote

classes = list(onto.classes())
if debug: print(classes)
object_properties = list(onto.object_properties())
if debug: print(object_properties)
data_properties = list(onto.data_properties())
if debug: print(data_properties)
disjoint_classes = list(onto.disjoint_classes())
if debug: print(disjoint_classes)
disjoint_properties = list(onto.disjoint_properties())
if debug: print(disjoint_properties)
annotation_properties = list(onto.annotation_properties())
if debug: print(annotation_properties)
general_axioms = list(onto.general_axioms())
if debug: print(general_axioms)
equivalent_classes = []
for i in onto.classes():
    eq_class = i.equivalent_to
    if eq_class: equivalent_classes.append((i, eq_class))
if debug: print(equivalent_classes)

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


#
def get_the_info(i):
    template_data_ = {}
    template_data_["class"] = str(i)
    template_data_["pref_label"] = prefLabel[i].first() or ""
    template_data_["definition"] = definition[i].first() or ""
    template_data_["example"] = example[i].first() or ""
    template_data_["scope_note"] = scopeNote[i].first() or ""
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
    myIRI = f"<https://ontologies.semanticarts.com/gist/{i}>"
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
    metrics_table += '## For The <<{}>> Namespace\n\n'.format(onto.base_iri)
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
                if (myIRI != None):
                    template_data[k][str(myIRI)] = get_the_info(myIRI)

    output = ''
    for k in sorted(d.keys()):
        toPrinter = {k: template_data[k]}
        t = jinja2.Template(templateString)
        output += t.render(d=toPrinter)
    metrics_table = get_metrics()
    print(metrics_table, file=output_file)
    print(output, file=output_file)

def run_pandoc(output_ebook, input_markdown, metadata_yaml, book_title):
    title="title=" + book_title

    #result = subprocess.check_call(["pandoc", "-S", "--toc", "-o", output_ebook, metadata_yaml, input_markdown, "-M" "title=", book_title], shell=True)
    result = subprocess.check_call(
        ["pandoc", "-S", "--toc", "-o", output_ebook, metadata_yaml, input_markdown, "-M", title],
        shell=True)
    return result


def sort_hyperlinks(f, fout):
    infile = ZipFile(f)
    outfile = ZipFile(fout, "w", ZIP_DEFLATED)

    # load up the locations
    nav = infile.read("nav.xhtml")
    xmldoc = etree.fromstring(nav)
    dict = {}
    for link in xmldoc.xpath('//x:a/@href', namespaces={"x":"http://www.w3.org/1999/xhtml"}):
        split_link = link.split("#")
        dict[split_link[1]] = split_link[0]
    #print(dict["gistemailaddress"])

    for f in infile.infolist():

        if "ch0" in f.filename:
            newfile = infile.read(f.filename)
            for x in dict.keys():
                newfile = str(newfile).replace("a href=\"#" + x + "-identifier", "a href=\"" + str(dict[x]) + "#" + str(x) ).replace("\\n","").replace("\\xc2\\xa0","")



            outfile.writestr(f.filename, newfile)
        else:
            newfile = infile.read(f.filename)
            outfile.writestr(f.filename, newfile)


def test_this_out():
    import os
    input_markdown = r'.\output\2023-04-05_gist_11.1.0.md'
    output_ebook = r'.\output\2023-04-05_gist_11.1.0.md.epub'
    output_ebook_sorted_links = r'.\output\2023-04-05_gist_11.1.0.md.sorted.epub'
    metadata_yaml = r'.\figures.etc/metadata.yaml'
    book_title = "The Zest of gist"
    cwd = os.getcwd()
    os.chdir(r'c:\Users\Pedro\PycharmProjects\ontology-documentation')


    output = open(input_markdown, 'w')
    create_documentation(output_file=output)
    output.close()
    if run_pandoc(output_ebook, input_markdown, metadata_yaml, book_title) == 0:
        sort_hyperlinks(output_ebook, output_ebook_sorted_links)
    print("Finished")
    os.chdir(cwd)
    myIRI = "<" + str(gist.PlannedEvent.iri) + ">"
    sparql_string_template = Template("select *  where {  $myIRI ?p ?o} ")
    #sparql_string_template_rdflib = Template("""prefix gist: <https://ontologies.semanticarts.com/gist/> select *  where { values (?s ?p) {  $myIRI  (gist:|!gist:)* } ?s (gist:|!gist:)* ?o} """)
    sparql_string_template_rdflib_old = Template(
        """prefix gist: <https://ontologies.semanticarts.com/gist/> 
            select *  where {  
                #values (?s ?p) {  $myIRI  (gist:|!gist:)* } 
                #bind((gist:|!gist:) as ?p
                #bind($myIRI as ?s)                
                #?s ?p ?o .
                $myIRI ?p ?o .

                } 
                """)
    sparql_string_template_rdflib = Template(
        """prefix gist: <https://ontologies.semanticarts.com/gist/> 
            describe $myIRI
                """)
    print(sparql_string_template_rdflib.substitute(myIRI=myIRI))
    graph = Graph().parse(gist_ontology_file)
    gist = Namespace('https://ontologies.semanticarts.com/gist/')
    xsd = Namespace('http://www.w3.org/2001/XMLSchema')
    graph.namespace_manager.bind('gist', gist)
    graph.namespace_manager.bind('xsd', xsd)
    graph_res = graph.query("""DESCRIBE <https://ontologies.semanticarts.com/gist/PlannedEvent>""")
    # def pprint_terms(terms, graph):
    #     print(*[t.n3(graph.namespace_manager) for t in terms])
    # results = default_world.sparql(sparql_string_template.substitute(myIRI=myIRI), error_on_undefined_entities=False)
    # print(list(results))
    # results_rdflib = graph.query(sparql_string_template_rdflib.substitute(myIRI=myIRI))
    # for x in results_rdflib:
    #     print(x)
    #     pprint_terms(x, graph)
    #     print("-"*40)
    # !pip install pydotplus
    # !pip install graphviz




def rdf2dot_pwin(g, stream, opts={}):
    """
    Convert the RDF graph to DOT
    writes the dot output to the stream
    """

    nodes = {}
    g.bind_namespaces = "rdflib"

    def node(x,g, color):
        if x not in nodes:
            nodes[x] = '''"{}" [color="{}"]'''.format(qname(x,g), color)
        print(nodes[x])
        return nodes[x]


    def qname(x, g):
        try:
            q = g.compute_qname(x)
            return q[0] + ":" + q[2]
        except:
            return x

    def color(o):
        if isinstance(o, (rdflib.URIRef)):
            return "BLACK"
        elif isinstance(o, (rdflib.BNode)):
            return "ORANGE"
        elif isinstance(o, (rdflib.Literal)):
            return "BLUE"
        else:
            return "BLACK"

    stream.write('''digraph {
    node [shape="box", style="rounded"];
    rankdir="LR"; ratio="auto";
    subgraph RDF {''')
    listMembers = []
    statements = []
    for s, p, o in g:

        first = rdflib.URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#first")
        rest = rdflib.URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#rest")
        if p == first:
            listMembers.append((s,p,o))
            for s1,p1,o1 in g:
                if s1 == s and p1 == rest:
                    statements.append((s1,p1,o1))
        if isinstance(s, (rdflib.URIRef,rdflib.BNode)):
            sn = node(s,g, color(s))
        if isinstance(o, (rdflib.URIRef, rdflib.BNode)):
            on = node(o,g, color(o))
        #print(s, qname(s,g))
        opstr = ("""\t"%s" -> "%s" [ color=%s, label="%s"] ;\n""")
        stream.write(opstr % (qname(s,g), qname(o,g), color(o), qname(p, g)))
    print(listMembers)
    print(statements)
    for y in nodes.keys():
        stream.write(nodes[y] +'\n')
    stream.write("}\n}")




if __name__ == "__main__":
    import io

    def visualize(g):
        stream = io.StringIO()
        rdf2dot_pwin(g, stream, opts={})
        f=open('./output/myGraph.dot','w')
        f.write(stream.getvalue())






    g = Graph()
    g_draw = Graph()
    g.parse(gist_ontology_file)
    gist = Namespace('https://ontologies.semanticarts.com/gist/')

    g.namespace_manager.bind('gist', gist)

    g_res = g.query('describe  <https://ontologies.semanticarts.com/gist/PlannedEvent> ')
    for x in g_res:
        g_draw.add(x)
    visualize(g_draw)