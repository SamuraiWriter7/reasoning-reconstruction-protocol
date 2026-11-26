# RZIP — Reasoning Reconstruction and Compression Protocol

**Version: v0.1.0**  
**Status: Experimental Specification**

> Do not preserve every reasoning process.
> Preserve the structure that enables reasoning to emerge again.

## 1. Overview

RZIP is a lightweight protocol for storing, exchanging,
and reconstructing reusable reasoning structures.

Rather than preserving complete reasoning histories,
RZIP preserves the essential components required to
generate and verify reasoning under new conditions.

These components include:

- Facts and evidence
- Reusable reasoning rules
- Reasoning skeletons
- Applicability conditions
- Verification requirements

RZIP aims to reduce redundant reasoning while preserving
correctness, traceability, and contextual safety.

It is designed as a declarative, model-independent format.

Model interoperability and computational savings remain
subjects for experimental evaluation.

---

## 2. Background

Conventional reasoning systems often repeat similar
reasoning operations whenever a new question is received.

```text
Question
    |
    v
Reasoning from scratch
    |
    v
Answer
    |
    v
End
```

This approach may repeatedly consume computational
resources for problems with similar underlying structures.

RZIP introduces a different approach.

```text
Question
    |
    v
Retrieve reasoning skeleton
    |
    v
Check current context
    |
    v
Reconstruct reasoning
    |
    v
Verify result
    |
    v
Answer
```

The objective is not to eliminate new reasoning.

The objective is to avoid unnecessary repetition when
validated reasoning structures can be safely reused.

---

## 3. From Compression to Reconstruction

### First-generation concept

```text
Reasoning
    |
    v
Compression
    |
    v
Storage
    |
    v
Decompression
    |
    v
Restored reasoning
```

### Second-generation concept

```text
Reasoning
    |
    v
Skeleton extraction
    |
    v
Structural storage
    |
    v
Contextual reconstruction
    |
    v
New reasoning
    |
    v
Verification
```

RZIP adopts the second-generation concept.

The stored object is not a complete reasoning history.

It is a reusable structure capable of supporting
new reasoning under appropriate conditions.

RZIP does not guarantee the recovery of original
reasoning steps or internal model computations.

---

## 4. Design Principles

### 4.1 Structure over history

Preserve reusable reasoning structures rather than
every intermediate reasoning step.

### 4.2 Context before application

A reasoning rule MUST NOT be applied solely because
a previous problem appears similar.

Its applicability conditions MUST be evaluated
against the current input.

### 4.3 Verification before acceptance

Reconstructed results MUST be verified before
being accepted as valid outputs.

### 4.4 Explicit uncertainty

Unknown conditions MUST NOT be interpreted
as satisfied conditions.

### 4.5 Declarative representation

RZIP packages MUST describe reasoning structures
without containing arbitrary executable code.

### 4.6 Model independence

RZIP SHOULD avoid dependencies on proprietary model
internals and model-specific reasoning representations.

### 4.7 Human authority

RZIP MUST NOT grant permissions for external actions.

External execution remains subject to independent
authorization and governance.

### 4.8 Minimal reconstruction

Only the reasoning structures necessary for the
current task SHOULD be activated.

---

## 5. Architecture

RZIP defines five conceptual layers.

```text
+----------------------------------+
| Fact Layer                       |
| Facts, evidence, provenance      |
+----------------------------------+
                 |
                 v
+----------------------------------+
| Rule Layer                       |
| Reusable reasoning operations    |
+----------------------------------+
                 |
                 v
+----------------------------------+
| Skeleton Layer                   |
| Reasoning structure and order    |
+----------------------------------+
                 |
                 v
+----------------------------------+
| Context Layer                    |
| Applicability and constraints    |
+----------------------------------+
                 |
                 v
+----------------------------------+
| Verification Layer               |
| Validation and acceptance        |
+----------------------------------+
```

These layers represent logical components,
not mandatory sequential execution stages.

Context evaluation MUST occur before rule application.

Verification MUST occur before result acceptance.

| Layer | Responsibility |
|---|---|
| Fact Layer | Stores facts, evidence, and provenance references |
| Rule Layer | Defines reusable reasoning operations |
| Skeleton Layer | Defines the composition and order of reasoning operations |
| Context Layer | Defines applicability and prohibition conditions |
| Verification Layer | Defines how reconstructed results are checked |

In v0.1, all five layers are represented within
a single JSON document.

---

## 6. Reasoning Skeleton

A reasoning skeleton is a reusable arrangement
of reasoning operations.

For example:

```text
Observe symptom
       |
       v
Identify candidate causes
       |
       v
Inspect current evidence
       |
       v
Evaluate candidates
       |
       v
Verify conclusion
```

The skeleton does not determine the conclusion
in advance.

It provides a structure through which a new
conclusion may be generated and evaluated.

The same skeleton may support different inputs,
contexts, and outcomes.

---

## 7. Context Evaluation

RZIP defines three applicability decisions.

| Decision | Meaning | Required behavior |
|---|---|---|
| APPLY | Required conditions are satisfied and no prohibition is active | Permit reconstruction |
| REJECT | A required condition fails or a prohibition is active | Do not apply the rule |
| UNKNOWN | Available information is insufficient | Defer application |

The evaluation procedure is:

```text
Evaluate context
       |
       +--> REJECT
       |       |
       |       v
       |    Do not reuse
       |
       +--> UNKNOWN
       |       |
       |       v
       |    Request evidence or defer
       |
       +--> APPLY
               |
               v
          Reconstruct
               |
               v
            Verify
```

A known prohibition takes precedence over uncertainty.

If any required condition is known to be false,
the decision is REJECT.

If no rejection condition is established but a
required condition or prohibition remains unresolved,
the decision is UNKNOWN.

APPLY permits reconstruction.

It does not guarantee that the reconstructed
result is correct.

---

## 8. Epistemic Classification

RZIP distinguishes facts, reconstructed content,
and hypotheses.

| Type | Name | Meaning |
|---|---|---|
| F | Fact | A claim supported by relevant evidence |
| R | Reconstructed | Content generated from stored reasoning structures |
| H | Hypothesis | A proposed explanation or claim requiring evaluation |

Illustrative example:

```json
{
  "claim": "The missing dependency may explain the error.",
  "type": "H",
  "verification_status": "unverified",
  "source": "S001"
}
```

Epistemic classification and verification status
are independent properties.

A reconstructed claim is not automatically a fact.

A hypothesis is not automatically incorrect.

A stored fact may also require revalidation when
its original context or validity period changes.

---

## 9. Minimal Reasoning Example

Consider the following reusable rule.

```text
a * x = b

Therefore:

x = b / a
```

### Required conditions

- The value of `a` is defined.
- The value of `b` is defined.
- Both values belong to the supported numeric domain.
- `a` is not zero.

### Prohibited conditions

- Division by zero.
- Unsupported input types.
- Inputs outside the declared numeric domain.

### Verification

Substitute the reconstructed result into
the original equation.

```text
a * x = b
```

For example:

```text
Input:
    a = 2
    b = 10

Context decision:
    APPLY

Reconstructed result:
    x = 5

Verification:
    2 * 5 = 10

Verification result:
    PASS
```

If `a` is zero, the rule MUST be rejected.

If a required input is missing, the applicability
decision MUST be UNKNOWN unless a known rejection
condition takes precedence.

The reference validator uses explicitly supported
operations rather than arbitrary code evaluation.

---

## 10. Pattern Completion and Separation

RZIP anticipates two complementary runtime functions.

### Pattern Completion

Identify reasoning skeletons that may be relevant
to the current problem.

### Pattern Separation

Distinguish superficially similar problems by
evaluating their actual conditions.

```text
Current problem
       |
       v
Pattern completion
       |
       v
Candidate skeletons
       |
       v
Pattern separation
       |
       v
Context evaluation
       |
       v
Applicable skeleton
```

Similarity alone MUST NOT authorize reuse.

Automated retrieval, similarity ranking, and
pattern separation engines are outside the
implementation scope of v0.1.

---

## 11. Related Components

RZIP separates storage, extraction, execution,
and research responsibilities.

| Component | Responsibility |
|---|---|
| RCA | Reasoning Compression Algorithm |
| RZIP | Reasoning structure storage and exchange |
| Runtime | Context evaluation, reconstruction, and verification |
| KEM | Knowledge Epicenter Mapping |
| RRG | Reasoning Resource Governance |

```text
Reasoning examples
        |
        v
       RCA
        |
        v
       RZIP <------ Resource governance
        |
        v
      Runtime
        |
        v
 Verified reasoning
```

KEM may independently analyze multiple reasoning
structures to investigate potential knowledge
epicenters.

RZIP does not attempt to establish historical
or causal origins by itself.

RCA, KEM, and RRG integration are outside
the implementation scope of v0.1.

---

## 12. Relationship to Efficient AI

AI efficiency can be addressed at multiple levels.

| Level | Optimization target |
|---|---|
| Model compression | Model weights and memory requirements |
| Rule extraction | Redundant reasoning procedures |
| Reasoning reconstruction | Reuse of validated structures |
| Resource governance | Unnecessary reasoning activity |

RZIP focuses on reasoning reconstruction.

It is complementary to model compression,
quantization, and resource governance.

A lightweight model may potentially benefit from
reusable reasoning skeletons generated or validated
by other systems.

However, RZIP does not assume that model compression
guarantees safety, accuracy, or energy efficiency.

These properties require independent evaluation.

---

## 13. Security and Trust Boundaries

RZIP documents are declarative data.

They MUST NOT independently:

- Execute arbitrary code
- Modify files
- Access external networks
- Grant system permissions
- Override human-defined constraints
- Bypass verification requirements

A runtime MUST treat imported reasoning structures
as untrusted until they have been validated.

Structural validation alone does not establish
semantic correctness or authenticity.

Provenance references do not independently prove
the truth of a stored claim.

External actions require separate authorization.

---

## 14. Provenance and Reuse

Reasoning assets SHOULD preserve information
necessary to identify their origin and permitted use.

Relevant metadata may include:

- Asset identifier
- Protocol version
- Creator or originating source
- Creation timestamp
- Evidence references
- Reuse permissions
- Revision information

RZIP does not establish ownership, authorship,
or compensation rights automatically.

It MUST NOT assume access to private model reasoning
or unauthorized reasoning histories.

Only information available for authorized storage
and reuse should be included.

Future extensions may connect RZIP assets to
contribution tracking and value circulation protocols.

---

## 15. Memory Consolidation and Forgetting

Future versions may investigate the consolidation
of multiple reasoning records into reusable structures.

```text
Experiences
     |
     v
Reusable rules
     |
     v
Reasoning skeletons
     |
     v
Validated knowledge assets
```

Consolidation MUST NOT silently discard important
exceptions, safety constraints, or required evidence.

Low usage frequency alone is insufficient grounds
for removing safety-critical reasoning information.

Automated consolidation, forgetting, retention
policies, and deletion mechanisms are outside
the scope of v0.1.

---

## 16. Repository Structure

```text
reasoning-reconstruction-protocol/
├── README.md
├── specs/
│   └── rzip-v0.1.md
├── schemas/
│   └── reasoning-skeleton.schema.json
├── examples/
│   ├── valid.json
│   ├── denied.json
│   └── unknown.json
├── scripts/
│   └── validate.py
└── .github/
    └── workflows/
        └── validate.yml
```

The initial specification consists of eight files.

| Path | Purpose |
|---|---|
| `README.md` | Project overview |
| `specs/rzip-v0.1.md` | Normative protocol specification |
| `schemas/reasoning-skeleton.schema.json` | JSON Schema definition |
| `examples/valid.json` | Successful reconstruction example |
| `examples/denied.json` | Rejected application example |
| `examples/unknown.json` | Unresolved applicability example |
| `scripts/validate.py` | Reference validator and semantic checks |
| `.github/workflows/validate.yml` | Continuous integration |

---

## 17. Validation

### Requirements

- Python 3.11 or later
- jsonschema 4.x

### Install the validation dependency

```bash
python -m pip install "jsonschema>=4,<5"
```

### Run validation

```bash
python scripts/validate.py
```

The planned reference validator checks:

- JSON Schema compliance
- Required layer definitions
- Identifier uniqueness
- Internal reference consistency
- Supported reasoning operations
- Context evaluation
- Reconstruction correctness
- Verification results
- Expected rejection behavior
- Expected uncertainty behavior

The validator is a limited reference implementation.

It does not attempt to validate unrestricted
natural-language reasoning.

---

## 18. Continuous Integration

GitHub Actions is intended to execute the
reference validator whenever relevant repository
changes are introduced.

The initial validation cases are:

| Case | Expected decision | Expected verification |
|---|---|---|
| Valid linear equation | APPLY | PASS |
| Division by zero | REJECT | NOT_RUN |
| Missing required input | UNKNOWN | NOT_RUN |
| Incorrect reconstructed result | APPLY | FAIL |

REJECT and UNKNOWN are successful validation
outcomes when they match the expected behavior.

The incorrect-result case is intended to be
tested internally by the reference validator.

A failed verification MUST prevent acceptance
of the reconstructed result.

Passing CI demonstrates conformance to the
implemented validation cases.

It does not establish general reasoning correctness,
production readiness, or computational savings.

---

## 19. Evaluation Framework

Future experiments should compare two approaches.

### Baseline reasoning

Solve each problem without using a stored
RZIP reasoning skeleton.

### RZIP-assisted reasoning

Retrieve, evaluate, reconstruct, and verify
using a reusable reasoning skeleton.

Suggested evaluation metrics:

| Metric | Purpose |
|---|---|
| Accuracy | Measure correctness |
| Latency | Measure end-to-end processing time |
| Resource consumption | Measure computational requirements |
| Misapplication rate | Detect inappropriate rule reuse |
| Verification failure rate | Detect invalid reconstructed outputs |
| Reuse rate | Measure successful structural reuse |
| Storage overhead | Measure reasoning asset storage requirements |

Evaluation should include retrieval, context evaluation,
reconstruction, and verification costs.

Compression ratio alone is not a sufficient
measure of success.

Correctness and safety take precedence over
computational savings.

No performance improvement is claimed by v0.1.

---

## 20. Scope of v0.1

### Included

- Declarative JSON representation
- Five-layer reasoning structure
- Reusable reasoning rules
- Reasoning skeleton definitions
- Context applicability conditions
- APPLY / REJECT / UNKNOWN decisions
- F / R / H classification
- Deterministic reference reconstruction
- Result verification
- Schema and semantic validation
- Continuous integration configuration

### Excluded

- Automated reasoning extraction
- Arbitrary code execution
- Full reasoning history restoration
- Vector-based skeleton retrieval
- Automated memory consolidation
- Automated forgetting
- Binary compression formats
- Model-to-model transfer experiments
- Autonomous external tool execution
- Knowledge epicenter discovery
- Economic settlement
- Energy-saving performance guarantees

---

## 21. Future Research Directions

| Version | Possible research direction |
|---|---|
| v0.1 | Minimal reasoning reconstruction and validation |
| v0.2 | Multi-rule composition and dependency graphs |
| v0.3 | Pattern completion and pattern separation |
| v0.4 | Memory consolidation and controlled forgetting |
| v0.5 | Cross-model reasoning asset exchange |
| Future | Provenance and value circulation integration |

These directions are illustrative.

Future development should be driven by
demonstrated requirements rather than
speculative feature expansion.

---

## 22. Philosophical Foundation

RZIP treats reasoning as a reconstructable
structural process.

The relationship may be expressed as:

```text
Knowledge Epicenter
        |
        v
Reasoning Structure
        |
        v
Contextual Reasoning
        |
        v
Validated Knowledge
```

RZIP focuses on the reasoning structure.

In the wind model of intelligence, reasoning
can be understood as a flow generated by
a particular configuration of conditions.

```text
Wind           = Reasoning
Pressure       = Question
Configuration  = Reasoning skeleton
Environment    = Context
Observation    = Verification
```

RZIP does not attempt to preserve every wind
that has ever passed.

It preserves structures that may allow
appropriate reasoning to emerge again.

---

## 23. Project Status

RZIP v0.1 is an experimental protocol specification.

Its initial objective is deliberately limited:

> Store one reasoning rule, apply it to a new
> problem under appropriate conditions, and
> verify the reconstructed result.

The specification should remain small until
further requirements are demonstrated.

---

## 24. License

License selection is pending.

Reuse of external reasoning assets remains
subject to their respective permissions
and applicable terms.

---

## Closing Principle

> Intelligence does not need to remember
> every path it has taken.
>
> It needs reliable structures that allow
> it to find an appropriate path again.

**RZIP — Preserve the structure. Reconstruct the reasoning.**
