---
topic: ML
chunk_id: intro_ai_ml_02
source: intro_to_ai_qa#10,#14
---

# Neural Network Training and Topology

A feed-forward neural network is structured so that no node output is used as an input to a node in the same layer or in a preceding layer. In contrast, a recurrent network features closed loops, allowing node outputs to be directed back as inputs to nodes in the same or preceding layers. Recurrent topologies enable processing of sequential data.

Training of a neural network proceeds in epochs. After the entire training set has been exploited (completing one epoch), the system checks the total error. If the current total error E is less than the tolerable error E_threshold, training terminates and outputs the final weights; otherwise, the error is reset to 0 and a new epoch begins. This termination criterion balances convergence quality with computational cost.
