import jinja2
from owlready2 import *

debug = False


class NestedDefaultDict(defaultdict):
    def __init__(self, *args, **kwargs):
        super(NestedDefaultDict, self).__init__(NestedDefaultDict, *args, **kwargs)

    def __repr__(self):
        return repr(dict(self))


gist_ontology_file = './ontology/v11.1.gistCore.owl'

d = defaultdict(list)
# set up the clustering of classes in the document
#
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
                                    "isMemberOf", "precedes"]
d["00600-Event"] = ["Event", "ContemporaryEvent", "ContingentEvent", "HistoricalEvent", "PhysicalEvent", "PlannedEvent"]
d["00700-ID"] = ["ID"]
d["00701-ID_Predicates"] = ["identifies", "isIdentifiedBy", "isAllocatedBy"]
d["00800-Project"] = ["Project", "ScheduledTask", "Task", "TaskTemplate", "Template"]
d["00801-Project_Predicates"] = ["hasDirectSubTask", "hasSubTask", "isDirectSubTaskOf", "isSubTaskOf", "hasGoal"]
d["00900-Specification"] = ["BundledCatalogItem", "CatalogItem", "ProductCategory", "ProductSpecification",
                            "Requirement", "Restriction", "ServiceSpecification", "Specification", "ReferenceValue"]
d["01000-IoT"] = ["Actuator", "Controller", "ControllerType", "MessageDefinition", "PhenomenaType",
                  "PhysicalActionType", "Sensor"]
d["01001-IoT_Predicates"] = ["hasViableRange", "accepts"]
d["01100-Magnitude"] = ["Volume", "VolumeUnit", "Magnitude", "Area", "Count", "ElectricCurrent", "InformationQuantity",
                        "LuminousIntensity", "Mass", "MolarQuantity", "Monetary", "Percentage", "ProductMagnitude",
                        "RatioMagnitude", "Temperature", "Duration", "Extent"]
d["01101-Magnitude_Predicates"] = ["hasPrecision", "hasMagnitude", "numericValue"]
d["01200-System"] = ["Component", "Equipment", "EquipmentType", "Function", "Network", "NetworkLink", "NetworkNode",
                     "System"]
d["01201-System_Predicates"] = ["contributesTo", "links", "linksFrom", "linksTo"]
d["01300-Organization"] = ["CountryGovernment", "GovernmentOrganization", "SubCountryGovernment",
                           "InterGovermentOrganization", "TreatyOrganization", "Group", "Organization"]
d["01301-Organization_Predicates"] = ["governs", "isGovernedBy", "isRecognizedDirectlyBy", "isRecognizedBy",
                                      "recognizes", "hasJurisdictionOver", "hasIncumbent"]
d["01400-Place"] = ["GeoPoint", "Building", "GeoRoute", "GeoSegment", "GeoVolume", "Landmark", "Place", "GeoRegion",
                    "GovernedGeoRegion", "CountryGeoRegion"]
d["01401-Place_Predicates"] = ["latitude", "longitude", "containsGeographically", "isGeographicallyContainedIn",
                               "isGeographicallyOccupiedBy", "occupiesGeographically", "hasPhysicalLocation",
                               "isGeographicallyPermanentlyOccupiedBy", "occupiesGeographicallyPermanently",
                               "hasAltitude", "goesToPlace", "comesFromPlace", "occursIn"]
d["01500-Human Behavior"] = ["Person", "Behavior", "IntellectualProperty", "Intention", "Language", "Artifact", "Goal",
                             "Permission"]
d["01501-Human Behavior_Predicates"] = ["hasBiologicalParent"]
d["01600-Date-and-Time"] = ["TimeZone", "TimeZoneStandard", "TemporalRelation"]
d["01601-Date-and-Time_Predicates"] = ["hasOffsetToUniversal", "isRecordedAt", "atDateTime", "endDateTime",
                                       "actualEndDateTime", "actualEndDate", "deathDate", "actualEndMicrosecond",
                                       "actualEndMinute", "actualEndYear", "plannedEndDateTime", "plannedEndDate",
                                       "plannedEndMicrosecond", "plannedEndMinute", "plannedEndYear",
                                       "startDateTime", "actualStartDateTime", "actualStartDate", "birthDate",
                                       "actualStartMicrosecond", "actualStartMinute", "actualStartYear",
                                       "plannedStartDateTime", "plannedStartDate", "plannedStartMicrosecond",
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
d["02001-General_Predicates"] = ["description", "name", "precedes", "produced", "prevents", "owns", "affects", "allows",
                                 "directs", "requires", "respondsTo", "conformsTo", "isConnectedTo", "isBasedOn",
                                 "isBasisFor"]

remaining_notes = ''' 

Human Behavior:
hasDeathDate, hasBiologicalParent,  hasBirthDate,hasBiologicalOffspring,produces,goesToAgent, comesFromAgent, owns,  hasGoal, isCharacterizedAs (also Category),   isAllocatedBy (also under Identifiers),  hasIncumbent,    

IoT:
hasViableRange, accepts (as currently defined it is for IoT, but I might also put it in [Permission, Requirement, Causation] since I suspect we will want to broaden the meaning), respondsTo,directs (but again I suspect we will broaden this so it perhaps should also go in General)


Collection:
sequence,providesOrderFor,followsDirectly,  precedesDirectly,
hasMember,  isMemberOf (also in Partitive - can we have them in both?)
precedes (also in General)

Time [ change name to 'Date and Time' if possible]
isRecordedAt,
Add all new predicates for gist 11 - look for atDateTime and everything else in that hierarchy)


General:
description,name, precedes,   conformsTo,  isConnectedTo,isBasedOn,  isBasisFor, 

Permission, Requirement, Causation (maybe this should just be General, but it feels like some kind of grouping)
requires, accepts (see also above under IoT), affects,  isAffectedBy,prevents, allows,
'''

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
skos_onto = get_ontology(skos_file).load()
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


#    print(includedClasses)
#    print(missingClasses)


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
    #    print(toPrinter)
    t = jinja2.Template(templateString)
    output += t.render(d=toPrinter)
    # output1 = re.sub('(gist\.)', "gist:", output)
print(output)
# print(object_properties)
# print(data_properties)

# """ProductUnit
#  and (hasMultiplicand only
#     (BaseUnit or CoherentProductUnit or CoherentRatioUnit))
#  and (hasMultiplier only
#     (BaseUnit or CoherentProductUnit or CoherentRatioUnit))
# """