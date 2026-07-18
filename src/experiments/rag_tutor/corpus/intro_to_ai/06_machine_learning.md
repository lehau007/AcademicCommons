---
tier: official
subtype: lecture_slides
course_code: IT3160
title: Machine Learning Foundations
---

# Defining a Machine Learning Problem

According to Mitchell (1997), a machine learning problem is defined as improving with experience at some task. Specifically, the three core elements that define a machine learning problem are: improving over a task T, with respect to a performance measure P, based on experience E. This T, P, E formulation cleanly separates what the learner is asked to do, how it will be judged, and what data it is allowed to learn from.

# Information Gain in Decision Trees

Information gain is a statistical measure that calculates the expected reduction in entropy caused by partitioning instances according to a specific attribute. In Decision Tree learning, information gain is used to determine which attribute is most useful for classifying training instances at each node, with the algorithm selecting the attribute that yields the highest information gain. This greedy attribute-selection strategy underlies algorithms such as ID3 and C4.5.

# Reinforcement Learning Discounting

In Reinforcement Learning the agent learns from delayed rewards. The discount rate (a value between 0 and 1) is used to bound the infinite sum of rewards over time in the discounted return model. It also favors earlier rewards over later ones, giving the agent a preference for finding shorter paths to its goal. A discount rate near 1 makes the agent far-sighted while a discount rate near 0 makes it myopic.
