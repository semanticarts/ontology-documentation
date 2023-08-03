from owlready2 import *
from itertools import chain


gist_ontology_file = './ontology/gistCore12.0.0.rdf'
ontologies_path = './ontology/'
onto_path.append(ontologies_path)
onto = get_ontology(gist_ontology_file)
onto.load()



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
d["00600-Event"] = ["Event", "ContemporaryEvent", "ContingentEvent", "HistoricalEvent", "PhysicalEvent", "ScheduledEvent", "TimeInterval"]
d["00700-ID"] = ["ID"]
d["00701-ID_Predicates"] = ["isIdentifiedBy", "isAllocatedBy"]
d["00800-Task"] = ["Task", "Project", "ScheduledTask"]
d["00900-Specification"] = ["BundledCatalogItem", "CatalogItem", "ProductCategory", "ProductSpecification",
                            "Requirement", "Restriction", "ServiceSpecification", "Specification", "TaskTemplate", "Template", "ReferenceValue"]
d["01000-IoT"] = ["Actuator", "Controller", "ControllerType", "MessageDefinition", "PhenomenaType",
                  "PhysicalActionType", "Sensor"]
d["01001-IoT_Predicates"] = ["hasViableRange", "accepts", "respondsTo"]
d["01100-Magnitude"] = ["Volume", "VolumeUnit", "Magnitude", "Area", "Count", "ElectricCurrent", "InformationQuantity",
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
d["01600-Date-and-Time"] = ["TemporalRelation"]
d["01601-Date-and-Time_Predicates"] = ["isRecordedAt", "atDateTime", "endDateTime",
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

ontology_classes = set([str(x).replace('gist.','') for x in set(onto.classes())])
print(ontology_classes)
class_keys = [x for x in d.keys()  if "0-" in x]
print("class_keys:  ", class_keys)
template_content = [d[z] for z in class_keys]
print(template_content)
template_classes = set(list(chain.from_iterable(template_content)))

print("ontology_classes.difference:    ", ontology_classes.difference(template_classes))
print("template_classes.difference:    ", template_classes.difference(ontology_classes))

ontology_properties= set([str(x).replace('gist.','') for x in set(onto.properties())])
print(ontology_properties)
property_keys = [x for x in d.keys()  if "1-" in x]
print("all keys:  ", d.keys())
print("property_keys:   ", property_keys)
template_content_properties = [d[z] for z in property_keys]
print("template_content_properties:   ", template_content_properties)
template_properties = set(list(chain.from_iterable(template_content_properties)))
print("template_properties:  ", template_properties)
print("ontology_properties.difference:    ", ontology_properties.difference(template_properties))
print("template_properties.difference:    ", template_properties.difference(ontology_properties))