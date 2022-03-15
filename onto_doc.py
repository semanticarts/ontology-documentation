import sys

from owlready2 import *
from collections import defaultdict
from itertools import chain
import jinja2

class NestedDefaultDict(defaultdict):
    def __init__(self, *args, **kwargs):
        super(NestedDefaultDict, self).__init__(NestedDefaultDict, *args, **kwargs)

    def __repr__(self):
        return repr(dict(self))


gist = 'ontology/v11.gistCore.owl'

d = defaultdict(list)
# set up the clustering of classes in the document
#
d["00100-Contact"] = ["Address", "ElectronicMessageAddress", "EmailAddress", "PostalAddress", "TelephoneNumber"]
d["00101-Contact_Predicates"] = ["hasAddress", "hasCommunicationAddress"]
d["00200-Agreement"] = ["Account", "Agreement", "Balance", "Commitment", "ContingentObligation", "Contract","ContractTerm", "DegreeOfCommitment", "Obligation", "Offer", "Transaction" ]
d["00300-Category"] = ["Category", "ControlledVocabulary", "Tag", "Taxonomy","Aspect"]
d["00400-Content"] = ["Content", "ContentExpression", "FormattedContent", "MediaType", "Medium", "Message", "RenderedContent", "Text", "ID", "SchemaMetaData"]
d["00500-Collection"] = ["Collection", "OrderedCollection", "OrderedMember"]
d["00600-Event"] = ["Event", "ContemporaneousEvent", "ContingentEvent", "HistoricalEvent", "PhysicalEvent", "PlannedEvent", ]
d["00700-Project"] = ["Project", "ScheduledTask", "Task", "TaskTemplate", "Template"]
d["00800-Specification"] = ["BundledCatalogItem", "CatalogItem", "ProductCategory", "ProductSpecification", "Requirement", "Restriction", "ServiceSpecification", "Specification" ]
d["00900-IoT"] = ["Actuator", "Controller", "ControllerType", "MessageDefinition", "PhenomenaType", "PhysicalActionType", "Sensor"]
d["01000-Magnitude"] = ["VolumeUnit", "Magnitude","Area", "Count", "ElectricCurrent", "InformationQuantity", "LuminousIntensity", "Mass", "MolarQuantity", "Monetary", "Percentage", "ProductMagnitude", "RatioMagnitude", "Temperature", "Duration", "Extent" ]
d["01100-System"] = [ "Component", "Equipment", "EquipmentType", "Function", "Network", "NetworkLink", "NetworkNode", "System"]
d["01200-Organization"] = ["CountryGovernment", "GeoPoliticalRegion", "GovernmentOrganization", "Group", "Organization"]
d["01300-Place"] = ["GeoPoint", "Building", "GeoRoute", "GeoSegment", "GeoVolume", "Landmark", "Place", "GeoRegion"]
d["01400-Human Behavior"] = ["Person", "Behavior", "IntellectualProperty", "Intention", "Language", "Artifact", "Goal", "Permission"]
d["01500-Time"] = ["TimeZone", "TimeZoneStandard", "TemporalRelation"]
d["01600-Physical World"] = ["PhysicalIdentifiableItem", "PhysicalSubstance", "LivingThing"]
d["01700-Unit"] = ["VolumeUnit", "UnitOfMeasure", "SimpleUnitOfMeasure", "ProductUnit", "AreaUnit", "CountingUnit", "CurrencyUnit", "DataSizeUnit", "ElectricalCurrentUnit", "LuminousIntensityUnit", "MoleUnit", "RatioUnit", "TemperatureUnit", "CoherentProductUnit", "CoherentRatioUnit", "CoherentUnit", "BaseUnit", "DistanceUnit" , "DurationUnit", "MassUnit"]



# d["Address"] = ["Address", "ElectronicMessageAddress", "EmailAddress", "PostalAddress", "TelephoneNumber"]
# d["Address_Predicates"] = ["hasAddress", "hasCommunicationAddress"]
# d["Agreement"] = ["Account", "Agreement", "Balance", "Commitment", "ContingentObligation", "Contract","ContractTerm", "DegreeOfCommitment", "Obligation", "Offer", "Transaction" ]
# d["Category"] = ["ControlledVocabulary", "Tag", "Taxonomy"]
# d["Content"] = ["ContentExpression", "FormattedContent", "MediaType", "Medium", "Message", "RenderedContent", "Text"]
# d["Event"] = ["ContemporaneousEvent", "ContingentEvent", "HistoricalEvent", "PhysicalEvent", "PlannedEvent", "Project", "ScheduledTask", "Task", "TaskTemplate"]
# d["Intention"] = ["BundledCatalogItem", "CatalogItem", "Goal", "Permission", "ProductCategory", "ProductSpecification", "Requirement", "Restriction", "ServiceSpecification", "Specification" ]
# d["IoT"] = ["Actuator", "Controller", "ControllerType", "MessageDefinition", "PhenomenaType", "PhysicalActionType", "Sensor"]
# d["Magnitude"] = ["Count", "ElectricCurrent", "InformationQuantity", "LuminousIntensity", "Mass", "MolarQuantity", "Monetary", "Percentage", "ProductMagnitude", "RatioMagnitude", "Temperature" ]
# d["Measure"] = ["Aspect", "OrderedCollection", "ReferenceValue"]
# d["Network"] = ["Artifact", "Component", "Equipment", "EquipmentType", "Function", "Network", "NetworkLink", "NetworkNode", "System"]
# d["Organization"] = ["CountryGovernment", "GeoPoliticalRegion", "GovernmentOrganization", "Group"]
# d["Place"] = ["Building", "GeoRoute", "GeoSegment", "GeoVolume", "Landmark", "Place"]
# d["TemporalRelation"] = ["TemporalRelation"]
# d["Time"] = ["DateInstant", "GreenwichInstant", "HumanInstant", "LocalInstant", "SystemInstant", "TimeZone", "TimeZoneStandard"]
# d["Top"] = ["Area", "AreaUnit", "BaseUnit", "Behavior", "Category", "Collection", "Content", "DistanceUnit", "Duration", "DurationUnit", "Event", "Extent", "GeoPoint", "GeoRegion", "ID",
#             "IntellectualProperty", "Intention", "Language", "LivingThing", "Magnitude", "MassUnit", "Organization", "Person", "PhysicalIdentifiableItem", "PhysicalSubstance", "ProductUnit",
#             "SchemaMetaData", "SimpleUnitOfMeasure", "Template", "TimeInstant", "UnitOfMeasure", "Volume", "VolumeUnit"]
# d["Unit"] = ["CountingUnit", "CurrencyUnit", "DataSizeUnit", "ElectricalCurrentUnit", "LuminousIntensityUnit", "MoleUnit", "RatioUnit", "TemperatureUnit"]
# d["UnitDim"] = ["CoherentProductUnit", "CoherentRatioUnit", "CoherentUnit"]


templateString = """
{% for section, classes in d.items() %}
#  <a name="{{ section[6:] }}">{{ section[6:] }}</a>

{% for itm1, itm in classes.items() %}
## <a name="{{ itm.class|replace("gist.","gist:") }}">{{ itm.class|replace("gist.","gist:") }}</a>

{% if itm.pref_label %}**Preferred Label** {{ itm.pref_label }}{% endif %}
	
{% if itm.definition %}**Definition** {{ itm.definition }}{% endif %}

{% if itm.example %}**Example** {{ itm.example }}{% endif %}

{% if itm.scope_note %}**Scope Note** {{ itm.scope_note }}{% endif %}

{% if itm.subclasses%}**Subclasses** {{ itm.subclasses|replace("gist.","gist:") }}{% endif %}

{% if itm.equivalent_class %}**EquivalentTo** {{ itm.equivalent_class|replace("gist.","gist:")|replace(".only", " only ")|replace("|", "or")|replace("&", "and")|replace(".value"," value ")|replace(".exactly"," exactly ")|replace(".some"," some ")|replace(".min"," min ")|replace(".max"," max ")|replace("[","")|replace("]","") }}{% endif %}

{% if itm.domain_of %}**Domain Of** {{ itm.domain_of }}{% endif %}

{% if itm.range_of %}**Range Of** {{ itm.range_of }}{% endif %}

{% if itm.disjoints %}**Disjoint With** {{ itm.disjoints }}{% endif %}

&nbsp;

{% endfor %}
&nbsp;

{% endfor %}

"""



onto = get_ontology(gist)

gist = onto.get_namespace("https://ontologies.semanticarts.com/gist/")
owl = onto.get_namespace("http://www.w3.org/2002/07/owl#")
rdf = onto.get_namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
rdfs = onto.get_namespace("http://www.w3.org/2000/01/rdf-schema#")
skos = onto.get_namespace("http://www.w3.org/2004/02/skos/core#")
xml = onto.get_namespace("http://www.w3.org/XML/1998/namespace")
xsd = onto.get_namespace("http://www.w3.org/2001/XMLSchema#")

onto.load()


classes = list(onto.classes())
object_properties = list(onto.object_properties())
data_properties = list(onto.data_properties())
disjoint_classes = list(onto.disjoint_classes())
disjoint_properties = list(onto.disjoint_properties())
annotation_properties = list(onto.annotation_properties())
general_axioms = list(onto.general_axioms())
equivalent_classes = []
for i in onto.classes():
    eq_class = i.equivalent_to
    if eq_class: equivalent_classes.append((i,eq_class))


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
    for k in d.keys():
        for c in d[k]:
            if c: s = onto.search(iri = "*" + c)
            if s:
                includedClasses.append(c)
            else:
                missingClasses.append(c)

#    print(includedClasses)
#    print(missingClasses)


def linkUp(s):
    s1 = s.replace("gist.","gist:")
    return f"[{s1}](#{s1})"

# #find prefLabel
template_data = NestedDefaultDict()
#
def getTheInfo(i):
    template_data_ = {}
    template_data_["class"] = str(i)
    template_data_["pref_label"] = i.prefLabel.first() or ""
    template_data_["definition"] = i.definition.first() or ""
    template_data_["example"] = i.example.first() or ""
    template_data_["scope_note"] = i.scopeNote.first() or ""
    # print("Class properties:  ", [(x, "Domain:  ", x.domain, "Range: ", x.range) for x in i.get_class_properties() if ('gist' in x.iri)])
    #myTemplate["Class properties"] = [x for x in i.get_class_properties() if (str(i) in str(x.range))]
    #myTemplate["Class properties"] = [x for x in i.get_class_properties() if (str(i) in str(x.domain))]
    try:
        #print("SC:" ,onto.search(subclass_of=i))
        template_data_["subclasses"] = ", ".join([linkUp(str(i)) for i in list(i.subclasses()) if i]) or ""
    except Exception as e:
        print(e)
        #continue
    try:
        template_data_["equivalent_class"] = i.equivalent_to
    except Exception as f:
        print(f)
        #continue
    propertiesThatHaveClassAsDomain = propertiesWithClassAsDomain[str(i)]
    template_data_["domain_of"] = ", ".join([linkUp(str(i)) for i in propertiesThatHaveClassAsDomain]) or ""
    propertiesThatHaveClassAsRange = propertiesWithClassAsRange[str(i)]
    template_data_["range_of"] = ", ".join([linkUp(str(i)) for i in propertiesThatHaveClassAsRange]) or ""
    dj = list(i.disjoints())

    djs = []
    [djs.append(dj_.entities) for dj_ in dj]
    flat_list = chain.from_iterable(djs)
    actual_disjoints = set(flat_list) - set([i])
    template_data_["disjoints"] = ", ".join([linkUp(str(i)) for i in actual_disjoints if i]) or ""
    return template_data_


def getPredicateInfo(i):
    template_data_ = {}
    myIRI = f"<https://ontologies.semanticarts.com/gist/{i}>"
    try:
        results = default_world.sparql("""SELECT *
                   { """ +  myIRI + """ <http://www.w3.org/2004/02/skos/core#prefLabel> ?prefLabel .
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



for k in d.keys():
    for l in d[k]:
        if "_" in k:
            template_data[k][str(l)] = getPredicateInfo(l)
        else:
            myIRI = onto.search_one(iri=gist.base_iri + l)
            template_data[k][str(myIRI)] = getTheInfo(myIRI)



output = ''
for k in sorted(d.keys()):
    toPrinter = {k: template_data[k]}
#    print(toPrinter)
    t = jinja2.Template(templateString)
    output += t.render(d = toPrinter)
    #output1 = re.sub('(gist\.)', "gist:", output)
print(output)
#print(object_properties)
#print(data_properties)

# """ProductUnit
#  and (hasMultiplicand only
#     (BaseUnit or CoherentProductUnit or CoherentRatioUnit))
#  and (hasMultiplier only
#     (BaseUnit or CoherentProductUnit or CoherentRatioUnit))
# """