---
topic: Planning
chunk_id: intro_ai_planning_01
source: intro_to_ai_qa#2
---

# Progression and Regression Planning

Progression planners use forward state-space search by considering the effect of all possible actions from a given state. Regression planners use backward state-space search, determining what must have been true in the previous state in order to achieve the current state or goal. The two directions can be combined in bidirectional planners.

Classical planning frameworks such as STRIPS represent actions with preconditions and effects, which both progression and regression planners can exploit. Forward search benefits from strong domain-specific heuristics derived from relaxed planning graphs, while backward search benefits when the goal description is small relative to the state. Choosing the right direction can dramatically reduce the planning search space.
