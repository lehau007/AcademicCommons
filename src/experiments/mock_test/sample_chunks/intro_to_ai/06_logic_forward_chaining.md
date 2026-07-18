---
topic: Logic
chunk_id: intro_ai_logic_02
source: intro_to_ai_qa#7
---

# Forward Chaining Inference

Forward chaining is a data-driven inference procedure used in propositional logic. In forward chaining, when a new fact is added, the system finds all rules that have that fact as a premise. If the other premises of those rules are already known to hold, the consequent is added to the set of known facts, which can then trigger further inferences.

Forward chaining is sound and complete for definite-clause knowledge bases and runs in time linear in the size of the knowledge base. It is particularly suitable for production-rule systems and expert systems where the agent receives streams of observations and must derive consequences incrementally. The dual procedure, backward chaining, is goal-driven and starts from a query rather than from new facts.
