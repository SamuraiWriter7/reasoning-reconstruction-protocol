# Changelog

All notable changes to the Reasoning Reconstruction
and Compression Protocol (RZIP) will be documented
in this file.

This project follows the Keep a Changelog format
and uses Semantic Versioning.

## [0.1.0] - 2026-11-26

### Added

#### Core Specification

- Initial RZIP technical specification.
- Declarative JSON-based reasoning asset format.
- Five-layer reasoning architecture:
  - Fact Layer
  - Rule Layer
  - Skeleton Layer
  - Context Layer
  - Verification Layer
- Basic provenance and reuse permission metadata.
- Model-independent reasoning representation.

#### Reasoning Reconstruction

- Reusable reasoning rules.
- Ordered reasoning skeletons.
- Deterministic arithmetic reconstruction.
- Supported arithmetic operations:
  - Addition
  - Subtraction
  - Multiplication
  - Division
- Exact rational arithmetic using Python Fraction.
- Canonical integer and rational output representations.
- Acyclic reasoning dependencies.
- Context-dependent rule application.

#### Context Evaluation

- Three-valued applicability decisions:
  - APPLY
  - REJECT
  - UNKNOWN
- Required condition evaluation.
- Prohibited condition evaluation.
- Explicit handling of missing input values.
- Decision precedence:

  REJECT > UNKNOWN > APPLY

- Prevention of reconstruction under rejected
  or unresolved conditions.

#### Epistemic Classification

- F: Fact
- R: Reconstructed
- H: Hypothesis
- Independent verification status.
- Preservation of claim classifications.
- Internal claim source references.
- Prevention of automatic epistemic promotion.

#### Verification

- Declarative verification operations.
- Exact rational comparison.
- Verification coverage for reconstructed outputs.
- Verification outcomes:
  - PASS
  - FAIL
  - NOT_RUN
- Reconstruction status:
  - SUCCESS
  - ERROR
  - NOT_RUN
- Explicit result acceptance policy.
- Output suppression when verification fails.
- Independent expected-result assertions.

#### JSON Schema

- JSON Schema Draft 2020-12.
- Mandatory field validation.
- Supported operation vocabulary.
- Operation arity validation.
- Operand representation constraints.
- Applicability decision constraints.
- Epistemic classification constraints.
- Expected result consistency validation.
- Rejection of undeclared document fields.

#### Reference Validator

- Python 3.11 reference implementation.
- JSON Schema validation.
- Semantic document validation.
- Global identifier uniqueness checks.
- Internal reference consistency checks.
- Rule dependency validation.
- Context evaluation.
- Deterministic reconstruction.
- Result verification.
- Expected-result comparison.
- Document immutability checks.
- Canonical rational representation checks.

#### Example Fixtures

- `examples/valid.json`
  - Successful reasoning reconstruction.
  - APPLY / SUCCESS / PASS.

- `examples/denied.json`
  - Prohibited reasoning reconstruction.
  - REJECT / NOT_RUN / NOT_RUN.

- `examples/unknown.json`
  - Deferred reasoning reconstruction.
  - UNKNOWN / NOT_RUN / NOT_RUN.

#### Internal Validation Tests

- Incorrect reconstructed result detection.
- Rejection precedence.
- Exact rational reconstruction.
- Arithmetic error containment.
- Expected-result independence.
- Duplicate identifier detection.
- Unknown rule reference detection.
- Self-dependency detection.
- Undeclared input detection.
- Boolean input rejection.
- Floating-point input rejection.
- Unknown context reference detection.
- Verification coverage validation.
- Unknown claim source detection.
- Unsupported operation rejection.
- Invalid timestamp detection.
- Context input overwrite prevention.
- Noncanonical rational rejection.
- Invalid acceptance state detection.
- Forward dependency detection.
- Duplicate JSON key detection.
- Nonstandard NaN rejection.
- Nonstandard Infinity rejection.

#### Continuous Integration

- GitHub Actions validation workflow.
- Python syntax validation.
- Automatic dependency installation.
- Validation on push and pull request.
- Manual workflow execution.
- Read-only repository permissions.
- Workflow execution timeout.

### Changed

- Transitioned the original RZIP concept from
  reasoning compression toward reasoning reconstruction.
- Shifted the primary storage target from complete
  reasoning histories to reusable reasoning skeletons.
- Separated reasoning extraction, structural storage,
  runtime execution, and knowledge epicenter research.
- Prioritized contextual applicability and verification
  over compression ratio.

### Security

- Restricted execution to explicitly supported
  arithmetic operations.
- Prohibited arbitrary executable expressions.
- Prevented reconstruction without an APPLY decision.
- Prevented acceptance without successful verification.
- Prevented overwriting declared context inputs.
- Rejected invalid rule dependencies.
- Introduced reference implementation resource limits:
  - Maximum JSON document size: 1,000,000 bytes.
  - Maximum rules: 100.
  - Maximum skeleton steps: 100.
  - Maximum verification checks: 100.
  - Maximum input integer size: 256 bits.
  - Maximum intermediate fraction component size:
    4,096 bits.
- Preserved the separation between provenance
  and execution authorization.
- Excluded autonomous external actions.

### Validation

The initial reference validation suite contains
26 validation cases.

| Category | Cases |
|---|---:|
| Example fixtures | 3 |
| Internal runtime tests | 5 |
| Structural safety tests | 15 |
| JSON safety tests | 3 |
| Total | 26 |

The initial GitHub Actions validation workflow
completed successfully.

### Limitations

RZIP v0.1 remains an experimental specification.

The reference implementation is limited to
deterministic arithmetic reasoning reconstruction.

This release does not establish:

- General-purpose reasoning correctness.
- Natural-language semantic verification.
- Automatic reasoning skeleton extraction.
- Complete historical reasoning restoration.
- Cross-model interoperability.
- Production-grade security.
- Quantitative inference cost reduction.
- Quantitative energy savings.
- A guaranteed compression ratio.

Successful validation demonstrates conformance
to the implemented reference cases only.

### Deferred

The following research directions are intentionally
excluded from the initial release:

- Reasoning Compression Algorithm (RCA) integration.
- Automated pattern completion.
- Automated pattern separation.
- Semantic skeleton retrieval.
- General branching reasoning structures.
- Automated memory consolidation.
- Controlled forgetting mechanisms.
- Cross-model reasoning asset exchange.
- Knowledge Epicenter Mapping (KEM).
- Reasoning Resource Governance (RRG) integration.
- Lightweight model integration.
- Binary compression formats.
- Contribution tracking and value circulation.

Future extensions should be driven by demonstrated
requirements rather than speculative expansion.

---

## Design Milestone

RZIP v0.1 establishes the initial foundation for
conditionally reusable reasoning structures.

The central design principle is:

> Preserve the structure.
> Reconstruct the reasoning.
> Verify before acceptance.

The objective is not to recover every reasoning
process from the past.

The objective is to enable appropriate reasoning
to emerge again under current conditions.
