One driver's route changed. Hundreds of other drivers arrived earlier or later.

Experiment 007 began with a question: Could a cooperative traffic system predict how one route choice affects everyone else?

Our original Test A ran 30 SUMO simulations with 1,000 vehicles. The estimator got the direction of the network effect right in just 8 of 20 selected probes (40%), below our predeclared 60% threshold.

We stopped before testing collective route optimization.

Then we investigated the failure rather than moving the goalposts.

First, a P0–P3 forensic audit reconstructed the original outcomes and examined 20,000 matched driver comparisons. For the 20 equal-free-flow route changes, the model's predicted effect on others effectively mirrored its prediction for the rerouted driver. That was a structural limitation—not independent knowledge of how traffic would respond.

Next, six instrumented replays reproduced their original trip outcomes exactly while recording vehicle movements, road-entry timing and waiting. One predicted-zero route change added 3,177 network-seconds of travel time, including 2,829 network-seconds of additional recorded waiting. Two combined route changes also produced a −2,989 network-second interaction relative to adding their separate effects.

These are synthetic traffic simulations, not real-world results. We observed timing and queue-associated changes, but did not establish a unique causal bottleneck.

**The next scientific sequence:**

1. Develop a better network-externality estimator that accounts for junction queues, congestion propagation and actual road-entry timing.
2. Validate it independently on fresh, unseen simulations—not the cases used to design it.
3. Proceed to Test B only if it passes: compare cooperative against equally informed independent routing, while measuring realized collective efficiency and individual fairness.

We have not demonstrated that cooperative routing works better. We now understand more precisely what must be predicted before that claim can be tested.

Read the full investigation, evidence and reproducible code:
https://github.com/yonnastgetahun/cooperative_traffic_research/blob/main/docs/RESEARCH_UPDATE_EXP007_COMPLETE_INVESTIGATION_2026-11-02.md

#AIProductManagement #ProductLeadership #AppliedAI #MultiAgentSystems #BuildingInPublic
