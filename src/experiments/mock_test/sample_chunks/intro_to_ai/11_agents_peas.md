---
topic: Planning
chunk_id: intro_ai_planning_02
source: intro_to_ai_qa#1,#4,#15,#16
---

# Agents, PEAS, and Environments

When designing an automated agent, the four factors to consider are the Performance measure, Environment, Actuators, and Sensors. For example, an automated taxi driver's performance measure might be a safe and fast trip, its environment includes roads and traffic, its actuators are the steering wheel and brakes, and its sensors include cameras and GPS. This PEAS description is the starting point for agent design.

A simple reflex agent selects actions based solely on the current percept, completely ignoring the rest of its percept history. In contrast, a model-based reflex agent maintains internal states that depend on the percept history, which helps reflect unobserved aspects of the current state. A fully observable environment is one where an agent's sensors give it complete access to the entire state of the environment at each point in time. Rational behavior is defined as doing the right thing, which means selecting an action that is expected to maximize goal achievement given the available information, evidences, and constraints.
