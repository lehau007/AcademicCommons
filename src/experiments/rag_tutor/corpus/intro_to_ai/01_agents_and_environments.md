---
tier: official
subtype: lecture_slides
course_code: IT3160
title: Intelligent Agents and Environments
---

# Intelligent Agents

An intelligent agent perceives its environment through sensors and acts upon it through actuators. When designing an automated agent, four factors must be considered: the Performance measure, the Environment, the Actuators, and the Sensors. These four factors are commonly referred to as PEAS. For example, an automated taxi driver's performance measure might be a safe and fast trip, its environment includes roads and traffic, its actuators are the steering wheel and brakes, and its sensors include cameras and GPS.

# Agent Types

A simple reflex agent selects actions based solely on the current percept, completely ignoring the rest of its percept history. This works only in fully observable environments. A model-based reflex agent improves on this by maintaining internal states that depend on the percept history; these internal states help reflect unobserved aspects of the current state. The difference between a model-based reflex agent and a simple reflex agent is that the former tracks the world while the latter is memoryless.

# Rational Behavior

The "Acting rationally" approach defines rational behavior as doing the right thing. Doing the right thing means selecting an action that is expected to maximize goal achievement given the available information, evidences, and constraints. Rationality is entirely dependent on the agent's goals and does not necessarily require thinking, as seen in reflexes like blinking.

# Environment Properties

A fully observable environment is one where an agent's sensors give it complete access to the entire state of the environment at each point in time. This is in contrast to a partially observable environment where some states are hidden from the agent. Other useful environment dimensions include deterministic vs stochastic, episodic vs sequential, static vs dynamic, and discrete vs continuous. The fully observable property is particularly important because it directly determines whether a simple reflex policy is sufficient or whether internal state must be maintained.
