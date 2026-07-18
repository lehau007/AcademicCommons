---
tier: official
subtype: lecture_slides
course_code: IT3160
title: Logic and Inference
---

# What is a Logic

A logic is defined as a triplet consisting of a language, a semantic, and an inference system. The language is a class of sentences described by a precise syntax. The semantic describes the meaning of elements in the language, typically by mapping sentences to truth values in possible worlds. The inference system consists of derivation rules used over the language that allow new sentences to be produced from existing ones in a sound (and ideally complete) manner.

# Forward Chaining in Propositional Logic

Forward chaining is a data-driven inference procedure for propositional Horn-clause knowledge bases. In forward chaining, when a new fact is added, the system finds all rules that have that fact as a premise. If the other premises of those rules are already known to hold, the consequent is added to the set of known facts, which can then trigger further inferences. The procedure terminates when no new facts can be derived. Forward chaining is sound and complete for Horn knowledge bases and runs in linear time.

# First Order Logic Terms and Predicates

First Order Logic (FOL) extends propositional logic with quantifiers, variables, and structured objects. In FOL, terms are built using variables, constants, and function symbols (for example FatherOf(X)). Predicates are then built by applying relations to these terms (for example Tall(FatherOf(Bill))). A well-formed formula is constructed by combining predicates with logical connectives and quantifiers. This expressive power lets FOL describe rich domains that propositional logic cannot capture.
