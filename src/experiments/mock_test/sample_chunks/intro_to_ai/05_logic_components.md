---
topic: Logic
chunk_id: intro_ai_logic_01
source: intro_to_ai_qa#20,#9
---

# Components of a Logic

A logic is defined as a triplet consisting of a language, a semantic, and an inference system. The language is a class of sentences described by a precise syntax, the semantic describes the meaning of elements in the language, and the inference system consists of derivation rules used over the language. Together these components let an agent represent knowledge and derive new facts.

In First Order Logic, terms are built using variables, constants, and function symbols such as FatherOf(X). Predicates are then built by applying relations to these terms, for example Tall(FatherOf(Bill)). This compositional structure gives FOL much greater expressive power than propositional logic while keeping inference tractable for many fragments.
