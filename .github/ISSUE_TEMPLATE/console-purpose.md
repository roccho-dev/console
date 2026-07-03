---
name: Console purpose issue
about: Define console repository purpose and projection boundary
title: "Define console repository purpose and projection boundary"
labels: ""
assignees: ""
---

## Purpose

Define `roccho-dev/console` as the deployable visualization surface for ADRS / governance state.

## Boundary

`console` consumes decisions, work state, component libraries, and deployment constraints, then publishes a visualization. It is not the authority for those inputs.

## Dependencies

- `roccho-dev/adrs`: ADR / decision input.
- `roccho-dev/ui`: reusable UI library input.
- `roccho-dev/deploy`: deployment policy / runtime integration input.
- GitHub Projects: optional projection input/output for Kanban/Roadmap visibility only.

## Non-authority rule

GitHub Projects, generated dashboards, screenshots, and deployed pages are projections. They must not become ADR, work-ledger, deployment, or merge authority.
