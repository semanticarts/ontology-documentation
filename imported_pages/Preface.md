# Preface

**gist** is Semantic Arts' minimalist upper [ontology](https://www.semanticarts.com/semantic-ontology-the-basics/) for the enterprise. It is designed to provide the maximum coverage of typical business concepts with the fewest number of primitives and the least amount of ambiguity. 

gist represents the fundamental concepts and relationships that exist for most business use cases and is designed to be domain-independent. This flexibility allows gist to be applied to a wide spectrum of domains and facilitates both interoperability and integration of knowledge. We have designed gist for clarity and completeness to cover nearly all the concepts that exist in real-world ontology development. 

 

Our gist ontology is free (as in free speech and free beer): it is distributed under the [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/) license. You can use it as you see fit for any purpose, as long as you give us attribution.



### The Periodic Table of gist

The gist ontology defines around 100 classes and about the same number of attributes and relationships and serves as a foundation for building more specialized ontologies. The gist periodic table is a graphical representation of gist coverage organized into abstract conceptual clusters.



<img src="C:\Users\Pedro\PycharmProjects\ontology-documentation\figures.etc\periodic-table-05-04-25-1.png" alt="gist_periodic_table" style="zoom:57%;" />



#### **Design Features**

Significant design features of gist include:

gist defines a small number of top-level concepts on which everything else is based, both in gist itself and in enterprise or application ontologies that use gist as a foundation. These concepts are not philosophical abstractions with unfamiliar terms such as endurant, perdurant, or qualia; they are everyday concepts with ordinary names such as person, organization, and agreement, whose meanings are just what you would expect. These high-level concepts provide building blocks for defining more specific domain concepts in a gist-based ontology.

gist has extensive and fine-grained disjointness at the highest level in order to help you avoid making certain types of logical errors in your ontologies or data that are based on gist. By explicitly stating, for example, that governmental organizations (such as the US federal government) can’t be intergovernmental organizations (such as the UN), a reasoner will complain of logical inconsistency if something has been typed as both. Without disjointness, such inconsistencies will not be surfaced. 

gist uses domain and range specifications sparingly in order to make properties more broadly applicable. To eliminate redundancy and reduce cognitive load, inverse properties are not defined. Subclasses are typically defined using a pattern that specifies how they specialize the superclass.



#### **Latest Release**

gist 14.0.0 was released on October 31, 2025. It is a major release that includes changes that break compatibility with previous versions of gist. The release package includes documentation and scripts to help you migrate your extension ontologies and instance data from earlier versions of gist.

 

The most notable changes in this release are:

- Introduction of a KnowledgeConcept class for expressing knowledge that arises from the distillation of experience. Using subclasses and instances of KnowledgeConcept, you can add more knowledge to your knowledge graph! 
- Addition of an Assignment class and associated predicates to represent task assignments, pay rate assignments, supervisor assignments, etc.
- Full refresh of annotations, including definitions, scope notes, and examples, for greater clarity and consistency.
- More nuanced model of offers and associated predicates.
- More streamlined class hierarchy, including commitments and agreements, composites and components, geographic classes, and others.

 

See the [release notes](https://github.com/semanticarts/gist/blob/v14.0.0/docs/ReleaseNotes.md) for full details of what’s new in gist 14.0.0.

 

 The release package includes:

- The gist core ontology, serialized as Turtle, RDF/XML, and JSON-LD.
- Supplementary ontologies of RDFS annotations and materialized subclass inferences to support a variety of applications and reasoners.
- Documentation and release notes in both HTML and Markdown formats.
- Migration scripts and documentation to upgrade your ontologies and instance data to gist 14. 



#### **How to Get gist**

Our gist ontology is free (as in free speech and free beer): it is distributed under the [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/) license, which only requires that you attribute the source ([http://semanticarts.com/gist](http://www.semanticarts.com/gist/)) when you use it. In addition, we require that any gist concepts remain in the gist namespace (https://w3id.org/semanticarts/ns/ontology/gist/) and that you not define your own terms within the gist namespace.

 

gist is publicly available from any of the following sources:

 

- [Download the latest gist release package]((https:/downloads.semanticarts.com/gistCore_Current_Version.zip)).
- Import gist directly into Protégé using the link https://w3id.org/semanticarts/ontology/gistCore
- Clone or download gist from the [GitHub repository](https://github.com/semanticarts/gist/tree/v14.0.0).

 

(Can't afford free? [Purchase a perpetual license](https://www.semanticarts.com/gist/gist-license/))

 

Looking for an older version of gist?  All former versions of gist are still available at [ https://github.com/semanticarts/gist/releases](https://github.com/semanticarts/gist/releases) .
