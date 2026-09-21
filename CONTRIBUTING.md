# Contributing

AIBPE is an infrastructure project. Contributions should preserve the evidence-oriented semantics of the core APIs.

## Before opening a pull request

- run `PYTHONPATH=src python -m unittest discover -s tests -p 'test_*.py'`
- run `PYTHONPATH=src python examples/full_demo.py`
- keep public schemas backward compatible within a minor release
- never add real credentials or customer data to fixtures
- document any new evidence level or event type

## Design rule

Do not turn an inference into a fact. When an algorithm can only identify a correlation or candidate contributor, the API and documentation must say so.
