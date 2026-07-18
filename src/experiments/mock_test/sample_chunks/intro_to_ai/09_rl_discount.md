---
topic: RL
chunk_id: intro_ai_rl_01
source: intro_to_ai_qa#13
---

# Discounted Return in Reinforcement Learning

The discount rate is a value between 0 and 1 used to bound the infinite sum of rewards over time in the discounted return model. It also favors earlier rewards over later ones, giving the agent a preference for finding shorter paths to its goal. A discount close to 1 makes the agent farsighted while a discount close to 0 makes it myopic.

Reinforcement learning agents learn policies that maximize expected discounted return through trial and error interaction with an environment. Algorithms such as Q-learning and SARSA update value estimates from sampled transitions. The discount rate therefore plays a dual role: it ensures the value function is well-defined for infinite-horizon problems and it shapes the agent's preference between near-term and long-term reward.
