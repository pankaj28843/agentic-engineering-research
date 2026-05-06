# Glossary

## Agentic engineering

Developing software with coding agents that can write and execute code. The human role shifts from typing most code to specifying goals, shaping context, designing feedback loops, and validating outcomes.

## Coding agent

An LLM wrapped in software that can call tools in a loop to achieve a goal. For coding agents, the defining tool is code execution, usually combined with filesystem access, shell commands, search, editing, tests, and browser automation.

## Harness

Everything around the model that makes the model useful: system prompts, tools, skills, MCP servers, filesystem, sandbox, browser access, orchestration logic, hooks, feedback loops, and constraints.

## Harness engineering

Designing and iterating the guides, sensors, tools, state, and control loops that make coding agents more reliable. In Fowler's framing, harness elements can be feedforward guides or feedback sensors, and can be computational or inferential.

## Context engineering

Curating what the model sees so it is likely to produce the desired behavior. Context engineering includes instructions, rules, skills, retrieved files, tools, memory, examples, and compaction strategies.

## Guide

A feedforward control that steers an agent before it acts: `AGENTS.md`, skills, code conventions, architecture rules, examples, plans, and specs.

## Sensor

A feedback control that observes an agent's output and lets it self-correct: tests, linters, type checkers, browser screenshots, traces, LLM judges, code review agents, performance budgets, and security scanners.

## Computational control

Deterministic CPU-run control such as tests, linters, type checks, structural analysis, schema validation, or link checking.

## Inferential control

Probabilistic semantic control such as LLM-as-judge, AI code review, design critique, or trace summarization.

## Harnessability

How amenable a codebase or workflow is to agent control. Strong types, clear module boundaries, stable architecture, readable docs, executable tests, and deterministic tooling increase harnessability.

## Requisite variety

A cybernetics idea: a regulator needs enough variety to govern the system. For coding agents, reducing system variety through standard topologies, service templates, and enforced boundaries makes comprehensive harnesses easier.

## Behavior harness

The subset of a harness that increases confidence that software functionally behaves as intended. This is harder than maintainability harnessing because AI-generated tests can pass while missing the real behavior.

## Approved fixtures / approved scenarios

A testing pattern where input and expected output live in domain-friendly fixture files. Once the runner is trusted, reviewing behavior becomes scanning diffs instead of auditing assertion code.
