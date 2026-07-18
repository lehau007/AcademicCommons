---
tier: community
subtype: summary_note
course_code: IT3160
title: Neural Networks Study Notes
---

# Network Architectures

Neural networks come in several architectural styles. A feed-forward network is structured so that no node output is used as an input to a node in the same layer or in a preceding layer. Information flows strictly from input toward output. In contrast, a recurrent network features closed loops, allowing node outputs to be directed back as inputs to nodes in the same or preceding layers. This recurrence gives recurrent networks the ability to model temporal dependencies and maintain a form of memory across time steps.

# Training Loop and Termination

Training a neural network typically proceeds in epochs. An epoch is one complete pass over the training set. The termination condition for the training loop of a neural network can be stated as follows: after the entire training set has been exploited (completing one epoch), the system checks the total error. If the current total error E is less than the tolerable error (E_threshold), training terminates and outputs the final weights; otherwise, the error is reset to 0 and a new epoch begins. Additional stopping criteria include maximum epoch count and early stopping on a validation set.
