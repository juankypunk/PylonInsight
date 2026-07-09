# Contributing to PylonInsight

First of all, thank you for your interest in contributing to PylonInsight!

PylonInsight is an open-source project focused on the historical analysis of Pylontech battery systems using BatteryView exports. Our goal is to build a transparent, reproducible, and extensible platform for battery diagnostics and long-term health monitoring.

## Project Philosophy

Before contributing, please keep these principles in mind:

- Original BatteryView exports are considered immutable.
- Every diagnostic result must be supported by measurable evidence.
- Documentation comes before implementation.
- Hypotheses must be clearly distinguished from confirmed facts.
- Transparency is preferred over "black box" algorithms.

## Ways to Contribute

You can contribute in many different ways:

- Report bugs.
- Improve documentation.
- Reverse engineer BatteryView file formats.
- Submit parser improvements.
- Improve SQL queries.
- Propose new diagnostic metrics.
- Share anonymized BatteryView datasets for validation.
- Review documentation and code.

## Reporting Issues

When reporting an issue, please include as much information as possible:

- BatteryView version
- BMS firmware version
- Inverter model
- Number of battery modules
- Operating system
- Steps to reproduce
- Relevant log files

## Sharing BatteryView Campaigns

BatteryView exports are extremely valuable for improving PylonInsight.

Before sharing:

- Remove any personal information if necessary.
- Do not modify CSV contents.
- Keep the original ZIP structure.
- Include any relevant observations (ambient temperature, SOC, operating mode, etc.).

Sample datasets are always appreciated.

## Coding Guidelines

- Write clear and readable code.
- Prefer simple solutions over clever ones.
- Add comments only when they improve understanding.
- Keep functions focused on a single responsibility.
- Write tests whenever practical.

## Documentation

Documentation is a first-class citizen.

Whenever a new BatteryView field is understood:

1. Document it.
2. Explain the evidence supporting the interpretation.
3. Assign a confidence level:
   - Confirmed
   - Likely
   - Hypothesis

Only after that should the parser or analytics engine be updated.

## Discussions

If you are unsure about a design decision, open a discussion or issue before implementing large changes.

We value reproducibility and maintainability over implementation speed.

Thank you for helping make PylonInsight better!