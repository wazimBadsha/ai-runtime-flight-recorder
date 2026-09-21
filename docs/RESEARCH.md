# Research positioning

## What the current ecosystem already covers

Public repositories show that several teams are building deterministic agent replay, trace diffing, counterfactual forks, and “flight recorder” systems.

Examples include:

- TARDIS — deterministic flight recorder / time-travel debugging for AI agents.
- AgentRewind — tracing, deterministic replay and run diffing.
- agentrec — deterministic record/replay with local cassettes.
- agentreplay — deterministic replay, mutation and structural diff.
- Retrace — record/replay with causal-diff language.
- Kinescope — deterministic replay plus fork-and-fix counterfactuals.
- deja — trajectory comparison with statistical inference.
- Agentic Stash — deterministic replay, fork/diff, seals and redaction.

These projects establish that “record/replay for agents” is already an active open-source category.

## Differentiation

AIBPE therefore does **not** position record/replay as the novel idea.

Its central object is the **behavioral provenance graph** and its central operation is a **declared intervention** over a graph dependency. The design asks:

> Which declared dependency changed, what downstream behavior changed with it, and what evidence was produced by isolating that variable?

The intended contribution is the open schema and protocol around that workflow.

## Claims policy

Do not describe AIBPE as “the first”, “the only”, or “nobody has built this”. Open-source discovery is incomplete and projects evolve quickly.

Use:

> “A focused open-source implementation of intervention-aware behavioral provenance for AI systems.”

That statement describes scope without making an unprovable priority claim.
