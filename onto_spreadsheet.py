from owlready2 import *
from rdflib import Graph
from collections import defaultdict
from itertools import chain
import jinja2

debug = False
## queries
q_findAllCategoryInstances = '''
PREFIX gist: <https://ontologies.semanticarts.com/gist/>
prefix owl:  <http://www.w3.org/2002/07/owl#>
prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
prefix skos: <http://www.w3.org/2004/02/skos/core#>
prefix xsd: <http://www.w3.org/2001/XMLSchema#>


# Find all instances of subclasses of Category
select ?CategoryInstance ?CategoryClass ?PrefLabel ?Definition ?Description
where 
{?CategoryInstance a ?CategoryClass. 
 ?CategoryClass rdfs:subClassOf* gist:Category .
 OPTIONAL {?CategoryInstance skos:prefLabel ?PrefLabel}
 OPTIONAL {?CategoryInstance skos:definition ?Definition}
 OPTIONAL {?CategoryInstance gist:description ?Description}
 FILTER NOT EXISTS{ ?CategoryClass owl:deprecated "true"^^xsd:boolean }
 FILTER NOT EXISTS{ ?CategoryInstance owl:deprecated "true"^^xsd:boolean }
        } 
order by ?CategoryClass ?CategoryInstance
'''
q_findAllRestrictionsOnAllClasses = '''
PREFIX gist: <https://ontologies.semanticarts.com/gist/>
prefix owl:  <http://www.w3.org/2002/07/owl#>
prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
prefix skos: <http://www.w3.org/2004/02/skos/core#>
prefix xsd: <http://www.w3.org/2001/XMLSchema#>

# Find all restrictions on all (non-deprecated) classes
SELECT distinct ?class  ?property ?r_type ?n ?filter 
WHERE {?restriction rdf:type owl:Restriction . 
       ?restriction owl:onProperty ?property . 
       ?class a owl:Class.
       FILTER(!(STRSTARTS(STR(?class), # ignore things in gist namespace
                "http://ontologies.semanticarts.com/gist/") ))     
       FILTER (!isBlank(?class))
       FILTER NOT EXISTS{ ?class owl:deprecated "true"^^xsd:boolean }

      {?restriction ?r_type ?filter .
       ?class rdfs:subClassOf ?restriction.
       FILTER (?r_type IN (owl:someValuesFrom , owl:allValuesFrom , owl:hasValue )) }
 UNION
      {?restriction ?r_type ?n.
       ?class rdfs:subClassOf ?restriction.
       FILTER NOT EXISTS{ ?class owl:deprecated "true"^^xsd:boolean }
       FILTER (?r_type IN (owl:minCardinality, owl:minQualifiedCardinality,
         owl:maxCardinality, owl:maxQualifiedCardinality, owl:qualifiedCardinality)) 
       ?restriction owl:onClass ?filter.} 
 UNION
      {{?class owl:intersectionOf ?intersection.} UNION 
       {?class owl:equivalentClass/owl:intersectionOf ?intersection.}
       FILTER NOT EXISTS{ ?class owl:deprecated "true"^^xsd:boolean }
       ?intersection rdf:rest/rdf:first* ?restriction.
       ?restriction ?r_type ?filter .
       FILTER (?r_type IN (owl:someValuesFrom , owl:allValuesFrom , owl:hasValue )) }
 UNION
      {{?class owl:intersectionOf ?intersection.} UNION 
       {?class owl:equivalentClass/owl:intersectionOf ?intersection.}
       FILTER NOT EXISTS{ ?class owl:deprecated "true"^^xsd:boolean }
       ?intersection rdf:rest/rdf:first* ?restriction.
       ?restriction ?r_type ?n.
       FILTER (?r_type IN (owl:minCardinality, owl:minQualifiedCardinality,
         owl:maxCardinality, owl:maxQualifiedCardinality, owl:qualifiedCardinality)) 
       ?restriction owl:onClass ?filter. }   
}    
order by ?class ?r_type ?filter ?property
'''

q_findConceptNamesAndAnnotations = '''
PREFIX gist: <https://ontologies.semanticarts.com/gist/>
prefix owl:  <http://www.w3.org/2002/07/owl#>
prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
prefix skos: <http://www.w3.org/2004/02/skos/core#>
prefix xsd: <http://www.w3.org/2001/XMLSchema#>

# Returns every resource of one or more specified types in a set of ontology files 
# along with their selected annotations. 

# To use this, comment out the line per your needs.
PREFIX gist: <https://ontologies.semanticarts.com/gist/>

SELECT DISTINCT ?Ontology ?Resource ?Parent ?Label ?Type ?Def ?Note ?ScopeNote  ?Comment
WHERE {?Resource rdf:type ?Type .
       OPTIONAL {?Resource rdfs:isDefinedBy ?Ontology . }
FILTER(?Type in (owl:Class, owl:DatatypeProperty, owl:ObjectProperty ))
OPTIONAL {?Resource rdfs:subClassOf ?Parent.
                      FILTER (!(isBlank(?Parent)))
                      FILTER (?Parent != owl:Thing)}
OPTIONAL {?Resource rdfs:subPropertyOf ?Parent}
OPTIONAL {?Resource skos:definition ?Def. }
OPTIONAL {?Resource (skos:prefLabel | rdfs:label) ?Label. }
OPTIONAL {?Resource rdfs:comment ?Comment. }
OPTIONAL {?Resource skos:note ?Note. }
OPTIONAL {?Resource skos:scopeNote ?ScopeNote. }

# FILTER(STRSTARTS(STR(?Resource), # use this to get URIs ONLY in the pleo namespace
# "https://ontologies.platts.com/pleo/") )
# FILTER(STRSTARTS(STR(?Resource), # use this to get URIs ONLY in the pleox namespace
# "https://taxonomies.platts.com/pleo/") )
FILTER(!(STRSTARTS(STR(?Resource), # ignore things in owl namespace
"http://www.w3.org/2002/07/owl#") ))
# FILTER(!(STRSTARTS(STR(?Resource), # ignore things in gist namespace
# "https://ontologies.semanticarts.com/gist/") ))
}
ORDER BY  ?Ontology ?Type ?Parent ?Resource
'''

gist = './ontology/2022-03-15_v11.gistCore.owl'

# onto = get_ontology(gist)
# #print(list(default_world))
#
# g = default_world.as_rdflib_graph()
# res_findAllCategoryInstances = g.query(q_findAllCategoryInstances)
# print(list(res_findAllCategoryInstances))
# res_findAllRestrictionsOnAllClasses = g.query(q_findAllRestrictionsOnAllClasses)
# print(list(res_findAllRestrictionsOnAllClasses))
# res_findConceptNamesAndAnnotations  = g.query(q_findConceptNamesAndAnnotations )
# print(list(res_findConceptNamesAndAnnotations))

g1 = Graph()
g1.parse(gist, format="xml")
res_findAllCategoryInstances = g1.query(q_findAllCategoryInstances)
print("1:  ", list(res_findAllCategoryInstances))
res_findAllRestrictionsOnAllClasses = g1.query(q_findAllRestrictionsOnAllClasses)
print("2:  ", list(res_findAllRestrictionsOnAllClasses))
res_findConceptNamesAndAnnotations  = g1.query(q_findConceptNamesAndAnnotations )
print("3:  ", list(res_findConceptNamesAndAnnotations))