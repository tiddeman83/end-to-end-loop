---
name: grilling
description: Interview the user relentlessly about a plan or design. Use when the user wants to stress-test a plan before building, or uses any 'grill' trigger phrases.
---

# Grilling

Use this subskill to stress-test a plan, design, architecture, backlog, release
proposal, implementation strategy, or product decision before the agent starts
building. It is especially important at the agile feature and user-story level, where vague intent must become a tightly scoped, well thought spec before implementation.

## Core Behavior

Interview the user relentlessly about every aspect of the plan until there is a
shared understanding. Walk down each branch of the design tree, resolving
dependencies between decisions one by one.

For each question:

1. Ask exactly one question.
2. Provide your recommended answer immediately after the question.
3. Explain how the answer changes scope, dependencies, or verification.
4. Wait for the user's feedback before continuing.
5. Use the user's answer to choose the next branch of the design tree.

Do not ask multiple questions at once. Asking multiple questions at once is
bewildering and defeats the purpose of the grilling flow.

## Codebase Exploration Rule

If a question can be answered by exploring the codebase, explore the codebase
instead of asking the user. Ask the user only when the answer is a product,
preference, priority, risk-tolerance, or intent decision that cannot be resolved
from the repository.

## Trigger Phrases

Use this subskill when the user says things like:

- "grill me"
- "grill this plan"
- "stress-test this design"
- "interrogate this architecture"
- "poke holes in this plan"
- "ask me hard questions before we build"
- "make sure we really understand the plan"

## Agile Spec and Verification Focus

Use grilling to refine features and user stories into buildable specs. Before the
normal end-to-end loop starts implementation, the agent should understand:

- the user story or job-to-be-done;
- whether this is the first run in the target project;
- the production runtime environment where the tool will run;
- the local development environment where changes and verification happen;
- the user's confirmation of that environment model when first-run context is new;
- the smallest useful slice;
- explicit out-of-scope boundaries;
- dependencies and sequencing;
- acceptance criteria;
- verification layers, including unit, integration, smoke, manual, security, CI,
  telemetry, or reviewer checks where applicable.

Verification is the most important output of grilling. Every recommended answer
should prefer precise, observable verification over vague confidence.

## Grilling Loop

1. State the current shared understanding in one or two sentences.
2. Identify the next unresolved decision or dependency, prioritizing scope and
   verification gaps first.
3. If codebase exploration can answer it, inspect the relevant files first.
4. Ask one precise question.
5. Give the recommended answer and why, including the verification implication.
6. Wait for feedback.
7. Update the shared understanding and continue with the next unresolved branch.

Stop when the design tree has no material unresolved branches, the user stops the
grilling, or the remaining questions are implementation details better handled by
the normal end-to-end loop.
