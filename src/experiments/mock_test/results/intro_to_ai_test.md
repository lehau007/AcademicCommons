# Mock Test — intro_to_ai

Total questions: **9**

## Test Plan Summary
- Planned total: 10
  - CSP: 1
  - Logic: 2
  - ML: 2
  - Planning: 2
  - RL: 1
  - Search: 2

## Questions

### Q1. [CSP | easy | multiple_choice]

Which of the following best describes 'The min-conflicts heuristic'?

- A. the starting point for agent design
- B. a value selection strategy where the algorithm chooses the value that violates the fewest constraints
- C. then built by applying relations to these terms, for example Tall(FatherOf(Bill))
- D. a value between 0 and 1 used to bound the infinite sum of rewards over time in the discounted return model

**Answer:** B. a value selection strategy where the algorithm chooses the value that violates the fewest constraints

_Explanation:_ Source chunk 'intro_ai_csp_02' defines The min-conflicts heuristic as: a value selection strategy where the algorithm chooses the value that violates the fewest constraints

_Citations:_
- `intro_ai_csp_02` (Iterative CSP Algorithms) — score=0.92
  > # Iterative CSP Algorithms  The min-conflicts heuristic is a value selection strategy where the algorithm chooses the value that violates the fewest constraints. It functions like hill-climbing whe...

### Q2. [Logic | easy | short_answer]

What is If the other premises of those rules?

**Answer:** already known to hold, the consequent is added to the set of known facts, which can then trigger further inferences

_Explanation:_ Derived by templating an X-is-Y sentence from chunk 'intro_ai_logic_02'.

_Citations:_
- `intro_ai_logic_02` (Forward Chaining Inference) — score=0.90
  > # Forward Chaining Inference  Forward chaining is a data-driven inference procedure used in propositional logic. In forward chaining, when a new fact is added, the system finds all rules that have ...

### Q3. [Logic | medium | true_false]

True or False: A logic is defined as a triplet consisting of a language, a semantic, and an inference system.

- True
- False

**Answer:** True

_Explanation:_ Statement is taken verbatim from chunk 'intro_ai_logic_01'.

_Citations:_
- `intro_ai_logic_01` (Components of a Logic) — score=0.95
  > # Components of a Logic  A logic is defined as a triplet consisting of a language, a semantic, and an inference system. The language is a class of sentences described by a precise syntax, the seman...

### Q4. [ML | easy | true_false]

True or False: Recurrent topologies enable processing of sequential data.

- True
- False

**Answer:** True

_Explanation:_ Statement is taken verbatim from chunk 'intro_ai_ml_02'.

_Citations:_
- `intro_ai_ml_02` (Neural Network Training and Topology) — score=0.95
  > # Neural Network Training and Topology  A feed-forward neural network is structured so that no node output is used as an input to a node in the same layer or in a preceding layer. In contrast, a re...

### Q5. [ML | medium | multiple_choice]

Which of the following best describes 'This TPE framing'?

- A. a type of search problem where the state is composed of variables Xi that take values from a specific domain Di
- B. sound and complete for definite-clause knowledge bases and runs in time linear in the size of the knowledge base
- C. broad enough to cover supervised, unsupervised, and reinforcement learning settings
- D. already known to hold, the consequent is added to the set of known facts, which can then trigger further inferences

**Answer:** C. broad enough to cover supervised, unsupervised, and reinforcement learning settings

_Explanation:_ Source chunk 'intro_ai_ml_01' defines This TPE framing as: broad enough to cover supervised, unsupervised, and reinforcement learning settings

_Citations:_
- `intro_ai_ml_01` (Defining a Machine Learning Problem) — score=0.92
  > # Defining a Machine Learning Problem  According to Mitchell (1997), a machine learning problem is defined as improving with experience at some task. Specifically, it requires improving over a task...

### Q6. [Planning | easy | multiple_choice]

Which of the following best describes 'Rational behavior'?

- A. an informed search method that expands the unexpanded node with the lowest evaluation value
- B. already known to hold, the consequent is added to the set of known facts, which can then trigger further inferences
- C. defined as doing the right thing, which means selecting an action that is expected to maximize goal achievement given the available information, evidences, and constraints
- D. a class of sentences described by a precise syntax, the semantic describes the meaning of elements in the language, and the inference system consists of derivation rules used over the language

**Answer:** C. defined as doing the right thing, which means selecting an action that is expected to maximize goal achievement given the available information, evidences, and constraints

_Explanation:_ Source chunk 'intro_ai_planning_02' defines Rational behavior as: defined as doing the right thing, which means selecting an action that is expected to maximize goal achievement given the available information, evidences, and constraints

_Citations:_
- `intro_ai_planning_02` (Agents, PEAS, and Environments) — score=0.92
  > # Agents, PEAS, and Environments  When designing an automated agent, the four factors to consider are the Performance measure, Environment, Actuators, and Sensors. For example, an automated taxi dr...

### Q7. [RL | easy | short_answer]

What is The discount rate?

**Answer:** a value between 0 and 1 used to bound the infinite sum of rewards over time in the discounted return model

_Explanation:_ Derived by templating an X-is-Y sentence from chunk 'intro_ai_rl_01'.

_Citations:_
- `intro_ai_rl_01` (Discounted Return in Reinforcement Learning) — score=0.90
  > # Discounted Return in Reinforcement Learning  The discount rate is a value between 0 and 1 used to bound the infinite sum of rewards over time in the discounted return model. It also favors earlie...

### Q8. [Search | easy | true_false]

True or False: The admissibility of h(n) determines whether A* returns optimal solutions.

- True
- False

**Answer:** True

_Explanation:_ Statement is taken verbatim from chunk 'intro_ai_search_02'.

_Citations:_
- `intro_ai_search_02` (Informed and Local Search) — score=0.95
  > # Informed and Local Search  A* search is an informed search method that expands the unexpanded node with the lowest evaluation value. A* uses the evaluation function f(n) = g(n) + h(n), where g(n)...

### Q9. [Search | medium | multiple_choice]

Which of the following best describes 'Alpha-Beta pruning'?

- A. a type of search problem where the state is composed of variables Xi that take values from a specific domain Di
- B. a key optimization in adversarial search; alpha-beta pruning removes branches of the search tree that do not influence the final decision and with perfect move ordering this technique can double the depth of the search
- C. explicit, these methods often outperform generic state-space search on combinatorial problems
- D. defined as doing the right thing, which means selecting an action that is expected to maximize goal achievement given the available information, evidences, and constraints

**Answer:** B. a key optimization in adversarial search; alpha-beta pruning removes branches of the search tree that do not influence the final decision and with perfect move ordering this technique can double the depth of the search

_Explanation:_ Source chunk 'intro_ai_search_02' defines Alpha-Beta pruning as: a key optimization in adversarial search; alpha-beta pruning removes branches of the search tree that do not influence the final decision and with perfect move ordering this technique can double the depth of the search

_Citations:_
- `intro_ai_search_02` (Informed and Local Search) — score=0.92
  > # Informed and Local Search  A* search is an informed search method that expands the unexpanded node with the lowest evaluation value. A* uses the evaluation function f(n) = g(n) + h(n), where g(n)...

## Metrics
- Coverage: 100.0% (6/6 topics)
- Dedup removed: 1 (rate=10.0%)
- Citation validity: 100.0% (9/9)
