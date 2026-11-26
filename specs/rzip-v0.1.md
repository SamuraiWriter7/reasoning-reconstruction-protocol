# RZIP Technical Specification v0.1

## Reasoning Reconstruction and Compression Protocol

| Property | Value |
|---|---|
| Protocol | RZIP |
| Version | 0.1.0 |
| Status | Experimental |
| Format | JSON |
| Architecture | Five-layer reasoning skeleton |
| Reference runtime | Python 3.11+ |

---

## 1. Purpose

RZIP defines a declarative protocol for preserving,
exchanging, and reconstructing reusable reasoning
structures.

The protocol preserves the structural conditions
required to generate and verify reasoning rather
than attempting to reproduce complete historical
reasoning processes.

The primary objective of RZIP is to enable safe
reasoning reuse under new conditions.

RZIP aims to:

- Reduce redundant reasoning operations.
- Preserve reusable reasoning structures.
- Define explicit applicability conditions.
- Distinguish facts from reconstructed content
  and hypotheses.
- Verify reconstructed results.
- Maintain traceability and trust boundaries.

RZIP does not guarantee computational savings,
general reasoning correctness, or model interoperability.

---

## 2. Normative Language

The following terms indicate requirement levels.

- MUST: Mandatory requirement.
- MUST NOT: Mandatory prohibition.
- SHOULD: Recommended requirement.
- SHOULD NOT: Recommended prohibition.
- MAY: Optional behavior.

An implementation claiming conformance to RZIP v0.1
MUST satisfy all applicable mandatory requirements.

---

## 3. Scope

### 3.1 Included

RZIP v0.1 defines:

- A single-document JSON representation.
- Five logical reasoning layers.
- Declarative reasoning rules.
- Ordered reasoning skeletons.
- Context evaluation.
- Three-valued applicability decisions.
- Epistemic classification.
- Deterministic reconstruction.
- Result verification.
- Basic provenance metadata.
- Schema and semantic validation.

### 3.2 Excluded

RZIP v0.1 does not define:

- Automated reasoning extraction.
- Complete reasoning history restoration.
- Arbitrary code execution.
- Automated skeleton retrieval.
- Semantic similarity algorithms.
- Automated memory consolidation.
- Automated forgetting.
- Binary compression.
- Knowledge epicenter discovery.
- Autonomous external tool execution.
- Economic settlement.
- Cross-model compatibility guarantees.

---

## 4. Core Terminology

### 4.1 Reasoning Asset

A structured RZIP document containing reusable
reasoning information and associated constraints.

### 4.2 Fact

A claim supported by relevant evidence.

A stored fact MUST NOT be assumed to remain valid
under every future context.

### 4.3 Rule

A declarative reasoning operation that transforms
defined inputs into an output.

### 4.4 Reasoning Skeleton

An ordered arrangement of reusable reasoning rules.

A reasoning skeleton defines how reasoning may
be reconstructed without prescribing an outcome
independent of the current input.

### 4.5 Context

The current conditions under which a reasoning
structure is evaluated.

### 4.6 Reconstruction

The generation of a new result by applying a
stored reasoning skeleton to current inputs.

### 4.7 Verification

The evaluation of a reconstructed result against
explicitly defined acceptance conditions.

---

## 5. Architectural Separation

RZIP separates reasoning extraction, storage,
execution, and research.

```text
Reasoning Examples
        |
        v
       RCA
        |
        v
       RZIP
        |
        v
      Runtime
        |
        v
 Verified Result
```

| Component | Responsibility |
|---|---|
| RCA | Extract reusable reasoning structures |
| RZIP | Preserve and exchange reasoning structures |
| Runtime | Evaluate context and reconstruct reasoning |
| KEM | Investigate potential knowledge epicenters |
| RRG | Govern reasoning resource allocation |

RZIP MUST NOT assume responsibility for arbitrary
external execution or historical origin discovery.

RCA, KEM, and RRG integration are outside the
implementation scope of v0.1.

---

## 6. Five-Layer Architecture

RZIP defines five logical layers.

```text
+----------------------------------+
| Fact Layer                       |
+----------------------------------+
| Rule Layer                       |
+----------------------------------+
| Skeleton Layer                   |
+----------------------------------+
| Context Layer                    |
+----------------------------------+
| Verification Layer               |
+----------------------------------+
```

These layers describe logical responsibilities.

They do not prescribe a sequential execution order.

Context evaluation MUST occur before reconstruction.

Verification MUST occur before result acceptance.

---

## 7. Document Structure

An RZIP v0.1 document MUST contain the following
top-level fields.

| Field | Type | Required |
|---|---|---|
| protocol | string | Yes |
| version | string | Yes |
| asset_id | string | Yes |
| metadata | object | Yes |
| facts | array | Yes |
| rules | array | Yes |
| skeleton | object | Yes |
| context | object | Yes |
| verification | object | Yes |
| claims | array | Yes |

The document MAY additionally contain an `expected`
object for reference validation fixtures.

Unknown top-level fields MUST be rejected by
the v0.1 reference validator.

The `protocol` field MUST equal `RZIP`.

The `version` field MUST equal `0.1.0`.

The `asset_id` MUST be a non-empty string.

---

## 8. Metadata

The metadata object defines basic asset provenance.

| Field | Type | Required |
|---|---|---|
| title | string | Yes |
| description | string | Yes |
| creator | string | Yes |
| created_at | string | Yes |
| source | string | Yes |
| reuse_permission | string | Yes |

Example:

```json
{
  "title": "Linear equation reconstruction",
  "description": "Reconstruct x from a * x = b.",
  "creator": "RZIP Example Author",
  "created_at": "2026-11-26T00:00:00Z",
  "source": "Original illustrative reasoning rule",
  "reuse_permission": "example-only"
}
```

The `created_at` field MUST contain an RFC 3339
date-time value with a timezone.

Metadata describes declared provenance.

It does not independently establish authenticity,
legal ownership, or factual correctness.

A reuse permission declaration MUST NOT override
applicable external authorization requirements.

---

## 9. Fact Layer

The Fact Layer preserves supporting facts
and evidence references.

Each fact MUST contain:

| Field | Type | Required |
|---|---|---|
| id | string | Yes |
| claim | string | Yes |
| evidence | string | Yes |
| verification_status | string | Yes |

Supported verification statuses are:

- verified
- unverified
- failed

Example:

```json
{
  "id": "F001",
  "claim": "For a nonzero rational a, a * x = b implies x = b / a.",
  "evidence": "Elementary algebra",
  "verification_status": "verified"
}
```

A fact marked as verified represents a declaration
associated with the stored evidence.

The runtime MUST NOT treat this declaration as
independent proof of its truth.

The reference validator checks the representation
of facts but does not establish the truth of
unrestricted natural-language claims.

---

## 10. Rule Layer

The Rule Layer defines reusable reasoning operations.

Each rule MUST contain:

| Field | Type | Required |
|---|---|---|
| id | string | Yes |
| description | string | Yes |
| operation | string | Yes |
| inputs | array of strings | Yes |
| output | string | Yes |

Example:

```json
{
  "id": "P001",
  "description": "Calculate x by dividing b by a.",
  "operation": "divide",
  "inputs": ["b", "a"],
  "output": "x"
}
```

The operation MUST belong to the supported
operation vocabulary.

RZIP v0.1 supports the following operations:

| Operation | Input count | Meaning |
|---|---|---|
| add | 2 | First input plus second input |
| subtract | 2 | First input minus second input |
| multiply | 2 | First input times second input |
| divide | 2 | First input divided by second input |

Input order MUST be preserved.

For noncommutative operations, such as subtraction
and division, changing input order changes the result.

An unsupported operation MUST cause document
validation to fail.

A rule MUST NOT contain arbitrary executable code.

The runtime MUST NOT evaluate operation names
as programming language expressions.

---

## 11. Supported Numeric Domain

RZIP v0.1 uses a limited exact rational arithmetic
domain for reference reconstruction.

### 11.1 Input values

Context input values MUST be JSON integers.

Booleans MUST NOT be treated as integers.

Floating-point values, strings representing numbers,
null values, arrays, and objects are outside the
supported numeric domain.

### 11.2 Intermediate values

Intermediate reconstruction values MAY be rational
numbers.

The reference implementation SHOULD use exact
rational arithmetic, such as Python Fraction.

### 11.3 Output representation

An integral result MUST be represented as a
JSON integer.

A non-integral rational result MUST be represented
as an object containing:

```json
{
  "numerator": 1,
  "denominator": 3
}
```

The denominator MUST be positive and nonzero.

The numerator and denominator MUST be reduced
to their simplest form.

Floating-point approximation MUST NOT be used
for the reference equality verification.

### 11.4 Arithmetic safety

Division by zero MUST NOT produce a result.

Arithmetic execution errors MUST prevent acceptance
of the reconstructed result.

Implementations SHOULD impose resource limits on
input sizes and intermediate arithmetic values.

---

## 12. Skeleton Layer

The Skeleton Layer defines the order in which
reasoning rules are applied.

The skeleton object MUST contain:

| Field | Type | Required |
|---|---|---|
| id | string | Yes |
| description | string | Yes |
| steps | array of strings | Yes |

Example:

```json
{
  "id": "S001",
  "description": "Solve a linear equation.",
  "steps": ["P001"]
}
```

Each entry in `steps` references a rule identifier.

The steps MUST be evaluated in their declared order.

Every referenced rule MUST exist.

The steps array MUST NOT be empty.

For the v0.1 reference profile:

- Rule identifiers MUST NOT repeat within a skeleton.
- Rule output names MUST be unique.
- A rule MUST NOT overwrite a context input.
- Rule inputs MUST be available from declared context
  inputs or preceding rule outputs.
- A rule MUST NOT depend on its own output.
- Forward dependencies MUST NOT be permitted.

These requirements establish a bounded,
acyclic execution sequence.

General branching, recursive execution, and
arbitrary dependency graphs are outside v0.1.

---

## 13. Context Layer

The Context Layer defines the current input and
the conditions governing rule application.

The context object MUST contain:

| Field | Type | Required |
|---|---|---|
| inputs | object | Yes |
| required_inputs | array of strings | Yes |
| required_conditions | array | Yes |
| prohibited_conditions | array | Yes |

Example:

```json
{
  "inputs": {
    "a": 2,
    "b": 10
  },
  "required_inputs": ["a", "b"],
  "required_conditions": [
    {
      "left": {
        "ref": "a"
      },
      "operator": "ne",
      "right": {
        "value": 0
      }
    }
  ],
  "prohibited_conditions": [
    {
      "left": {
        "ref": "a"
      },
      "operator": "eq",
      "right": {
        "value": 0
      }
    }
  ]
}
```

The `required_inputs` array declares the permitted
context input names required by the skeleton.

A missing required input is a valid uncertainty
condition.

It MUST NOT cause schema validation to fail
solely because the input is missing.

Every supplied input name MUST be declared
in `required_inputs`.

The reference validator MUST reject supplied
inputs outside the supported numeric domain.

---

## 14. Condition Representation

Conditions MUST be represented declaratively.

Each condition MUST contain:

| Field | Type |
|---|---|
| left | operand |
| operator | string |
| right | operand |

An operand MUST contain exactly one of:

- `ref`: A variable reference.
- `value`: An integer literal.

Reference operand:

```json
{
  "ref": "a"
}
```

Literal operand:

```json
{
  "value": 0
}
```

An operand MUST NOT contain both fields.

Supported comparison operators are:

| Operator | Meaning |
|---|---|
| eq | Equal |
| ne | Not equal |
| gt | Greater than |
| gte | Greater than or equal to |
| lt | Less than |
| lte | Less than or equal to |

An unsupported operator MUST cause document
validation to fail.

Context condition references MUST refer to
declared context input names.

Context conditions MUST NOT reference
reconstruction outputs.

---

## 15. Three-Valued Condition Evaluation

An individual condition produces one of:

- TRUE
- FALSE
- UNKNOWN

If both operands are available, the runtime
MUST evaluate the comparison.

If a declared input required for comparison
is missing, the condition MUST evaluate to UNKNOWN.

UNKNOWN MUST NOT be converted to TRUE or FALSE
without additional evidence.

A condition containing an undeclared reference
is structurally invalid and MUST be rejected.

A missing declared reference is an uncertainty
condition, not a structural reference error.

---

## 16. Applicability Decisions

RZIP defines three runtime applicability decisions.

| Decision | Meaning |
|---|---|
| APPLY | Reconstruction is permitted |
| REJECT | Reconstruction is prohibited |
| UNKNOWN | Applicability cannot be established |

### 16.1 REJECT

The runtime MUST return REJECT when:

- Any required condition is FALSE.
- Any prohibited condition is TRUE.

A known rejection condition takes precedence
over missing inputs and unresolved conditions.

### 16.2 UNKNOWN

If no rejection condition has been established,
the runtime MUST return UNKNOWN when:

- A required input is missing.
- A required condition is UNKNOWN.
- A prohibited condition is UNKNOWN.

### 16.3 APPLY

The runtime MUST return APPLY only when:

- All required inputs are available.
- All required conditions are TRUE.
- All prohibited conditions are FALSE.

### 16.4 Decision precedence

```text
REJECT > UNKNOWN > APPLY
```

Decision procedure:

```text
Evaluate all context conditions
        |
        v
Known rejection condition?
        |
      YES -----> REJECT
        |
       NO
        |
        v
Missing input or unresolved condition?
        |
      YES -----> UNKNOWN
        |
       NO
        |
        v
      APPLY
```

The runtime MUST NOT reconstruct reasoning
when the decision is REJECT or UNKNOWN.

Structural document validation MUST occur
before applicability evaluation.

Invalid documents do not receive a normal
applicability decision.

---

## 17. Reconstruction Procedure

Reconstruction MUST occur only after APPLY
has been established.

The runtime MUST:

1. Create an execution environment from current inputs.
2. Read the ordered skeleton steps.
3. Resolve each referenced rule.
4. Resolve the rule input values.
5. Execute the supported declarative operation.
6. Store the result under the declared output name.
7. Continue until all steps are complete.
8. Submit reconstructed values for verification.

```text
APPLY
  |
  v
Initialize input environment
  |
  v
Resolve next rule
  |
  v
Execute supported operation
  |
  v
Store reconstructed value
  |
  v
More steps?
  |
  +-- YES --> Resolve next rule
  |
  +-- NO ---> Verification
```

The runtime MUST NOT:

- Execute undeclared operations.
- Modify the input document.
- Overwrite context inputs.
- Introduce undeclared dependencies.
- Skip required verification.
- Perform external actions.

A reconstruction error MUST terminate the
current reconstruction attempt.

---

## 18. Verification Layer

The Verification Layer defines the acceptance
conditions for reconstructed results.

The verification object MUST contain:

| Field | Type | Required |
|---|---|---|
| checks | array | Yes |

At least one verification check MUST be present.

Each verification check MUST contain:

| Field | Type |
|---|---|
| id | string |
| operation | string |
| inputs | array of strings |
| operator | string |
| expected | operand |

Supported verification operations are:

| Operation | Input count | Meaning |
|---|---|---|
| identity | 1 | Return the referenced value |
| add | 2 | Add referenced values |
| subtract | 2 | Subtract referenced values |
| multiply | 2 | Multiply referenced values |
| divide | 2 | Divide referenced values |

Example:

```json
{
  "checks": [
    {
      "id": "V001",
      "operation": "multiply",
      "inputs": ["a", "x"],
      "operator": "eq",
      "expected": {
        "ref": "b"
      }
    }
  ]
}
```

This check verifies:

```text
a * x = b
```

Verification references MUST resolve to declared
context inputs or reconstructed rule outputs.

Every reconstructed rule output MUST be
referenced by at least one verification check,
either as an input or as the expected reference.

This coverage requirement does not establish
that the checks are semantically sufficient.

A runtime MUST NOT consider verification successful
solely because reconstruction completed.

---

## 19. Verification Outcomes

The runtime defines three verification outcomes.

| Outcome | Meaning |
|---|---|
| PASS | All required checks succeeded |
| FAIL | At least one required check failed or could not complete |
| NOT_RUN | Verification was not executed |

### 19.1 PASS

Verification MUST return PASS only when
every declared check evaluates to TRUE.

### 19.2 FAIL

Verification MUST return FAIL when:

- Any check evaluates to FALSE.
- A required verification value is unavailable.
- A verification operation cannot be completed.

### 19.3 NOT_RUN

Verification MUST return NOT_RUN when:

- Applicability is REJECT.
- Applicability is UNKNOWN.
- Reconstruction fails before verification begins.

A reconstruction error MUST remain distinguishable
from a context rejection.

The runtime MUST NOT relabel an arithmetic failure
as a successful context rejection.

---

## 20. Acceptance Policy

A reconstructed result MAY be accepted only when:

```text
Document validation = SUCCESS

AND

Applicability = APPLY

AND

Reconstruction = SUCCESS

AND

Verification = PASS
```

All other combinations MUST prevent acceptance.

| Applicability | Reconstruction | Verification | Accepted |
|---|---|---|---|
| APPLY | SUCCESS | PASS | Yes |
| APPLY | SUCCESS | FAIL | No |
| APPLY | ERROR | NOT_RUN | No |
| REJECT | NOT_RUN | NOT_RUN | No |
| UNKNOWN | NOT_RUN | NOT_RUN | No |

Acceptance indicates conformance to the declared
verification conditions.

It does not establish universal correctness,
external authorization, or factual truth.

---

## 21. Epistemic Classification

RZIP distinguishes three epistemic categories.

| Code | Category |
|---|---|
| F | Fact |
| R | Reconstructed |
| H | Hypothesis |

Each claim MUST contain:

| Field | Type |
|---|---|
| id | string |
| claim | string |
| type | string |
| verification_status | string |
| source | string |

Example:

```json
{
  "id": "C001",
  "claim": "The equation can be solved using P001.",
  "type": "R",
  "verification_status": "unverified",
  "source": "P001"
}
```

The `type` field MUST be one of:

- F
- R
- H

The `verification_status` field MUST be one of:

- verified
- unverified
- failed

The source MUST reference an existing fact,
rule, skeleton, or verification check.

A reconstructed claim MUST NOT automatically
be classified as a fact.

A hypothesis MUST NOT automatically be rejected
because it is unverified.

A successful arithmetic verification MUST NOT
automatically mark unrelated natural-language
claims as verified.

The v0.1 runtime MUST preserve claim classifications.

Automatic epistemic promotion is outside
the implementation scope of v0.1.

---

## 22. Identifier Integrity

The following identifiers MUST be non-empty strings:

- Fact identifiers.
- Rule identifiers.
- Skeleton identifier.
- Verification check identifiers.
- Claim identifiers.

Identifiers MUST be globally unique within the
document across these five categories.

All internal references MUST resolve to the
appropriate declared object or variable.

Object identifiers and variable names belong
to separate namespaces.

A duplicated identifier MUST cause document
validation to fail.

An unresolved structural reference MUST cause
document validation to fail.

---

## 23. Complete Reference Document

The following document illustrates a complete
RZIP v0.1 asset.

```json
{
  "protocol": "RZIP",
  "version": "0.1.0",
  "asset_id": "RZIP-001",
  "metadata": {
    "title": "Linear equation reconstruction",
    "description": "Solve a * x = b using a reusable rule.",
    "creator": "RZIP Example Author",
    "created_at": "2026-11-26T00:00:00Z",
    "source": "Original illustrative reasoning rule",
    "reuse_permission": "example-only"
  },
  "facts": [
    {
      "id": "F001",
      "claim": "For nonzero rational a, a * x = b implies x = b / a.",
      "evidence": "Elementary algebra",
      "verification_status": "verified"
    }
  ],
  "rules": [
    {
      "id": "P001",
      "description": "Divide b by a.",
      "operation": "divide",
      "inputs": ["b", "a"],
      "output": "x"
    }
  ],
  "skeleton": {
    "id": "S001",
    "description": "Solve a linear equation.",
    "steps": ["P001"]
  },
  "context": {
    "inputs": {
      "a": 2,
      "b": 10
    },
    "required_inputs": ["a", "b"],
    "required_conditions": [
      {
        "left": {
          "ref": "a"
        },
        "operator": "ne",
        "right": {
          "value": 0
        }
      }
    ],
    "prohibited_conditions": [
      {
        "left": {
          "ref": "a"
        },
        "operator": "eq",
        "right": {
          "value": 0
        }
      }
    ]
  },
  "verification": {
    "checks": [
      {
        "id": "V001",
        "operation": "multiply",
        "inputs": ["a", "x"],
        "operator": "eq",
        "expected": {
          "ref": "b"
        }
      }
    ]
  },
  "claims": [
    {
      "id": "C001",
      "claim": "A solution may be reconstructed using P001.",
      "type": "R",
      "verification_status": "unverified",
      "source": "P001"
    }
  ],
  "expected": {
    "decision": "APPLY",
    "reconstruction": "SUCCESS",
    "verification": "PASS",
    "accepted": true,
    "outputs": {
      "x": 5
    }
  }
}
```

---

## 24. Reference Runtime Result

A successful runtime result SHOULD use the
following representation.

```json
{
  "asset_id": "RZIP-001",
  "decision": "APPLY",
  "reconstruction": "SUCCESS",
  "verification": "PASS",
  "accepted": true,
  "outputs": {
    "x": 5
  }
}
```

A rejected application result:

```json
{
  "asset_id": "RZIP-002",
  "decision": "REJECT",
  "reconstruction": "NOT_RUN",
  "verification": "NOT_RUN",
  "accepted": false,
  "outputs": {}
}
```

An unresolved application result:

```json
{
  "asset_id": "RZIP-003",
  "decision": "UNKNOWN",
  "reconstruction": "NOT_RUN",
  "verification": "NOT_RUN",
  "accepted": false,
  "outputs": {}
}
```

The `outputs` object MUST contain only accepted
reconstructed values.

When acceptance fails, `outputs` MUST be empty.

Diagnostic candidate values MAY be retained
internally but MUST NOT be presented as accepted
results.

---

## 25. Expected Validation Results

The optional `expected` object is reserved
for validation fixtures.

It MUST contain:

| Field | Type |
|---|---|
| decision | string |
| reconstruction | string |
| verification | string |
| accepted | boolean |
| outputs | object |

The reference validator MUST compare the actual
runtime outcome against the declared expected
outcome.

The runtime MUST NOT use the expected outcome
to determine applicability, reconstruction,
verification, or acceptance.

Expected outcomes are test assertions,
not execution instructions.

A mismatch MUST cause the validation fixture
to fail.

---

## 26. Reference Validation Pipeline

The validator MUST perform the following stages.

```text
Load JSON
    |
    v
Validate JSON Schema
    |
    v
Validate identifiers
    |
    v
Validate internal references
    |
    v
Validate rule dependencies
    |
    v
Evaluate context
    |
    +--> REJECT  --> Compare expected result
    |
    +--> UNKNOWN --> Compare expected result
    |
    v
  APPLY
    |
    v
Reconstruct
    |
    +--> ERROR --> Compare expected result
    |
    v
Verify
    |
    v
Determine acceptance
    |
    v
Compare expected result
```

The reference validator MUST reject:

- Malformed JSON.
- Duplicate JSON object keys.
- Unsupported protocol versions.
- Missing mandatory document fields.
- Invalid field types.
- Duplicate identifiers.
- Unsupported operations.
- Invalid operation arity.
- Unresolved structural references.
- Duplicate skeleton steps.
- Invalid rule dependencies.
- Invalid verification references.
- Missing verification coverage.
- Unexpected runtime outcomes.

The validator MUST distinguish structural invalidity
from valid runtime rejection.

---

## 27. Required Validation Cases

The initial reference implementation MUST
evaluate the following cases.

### 27.1 Valid reconstruction

Input:

```text
a = 2
b = 10
```

Expected:

```text
Decision: APPLY
Reconstruction: SUCCESS
Verification: PASS
Accepted: true
Output: x = 5
```

### 27.2 Prohibited reconstruction

Input:

```text
a = 0
b = 10
```

Expected:

```text
Decision: REJECT
Reconstruction: NOT_RUN
Verification: NOT_RUN
Accepted: false
Outputs: empty
```

### 27.3 Unknown applicability

Input:

```text
b = 10
a = missing
```

Expected:

```text
Decision: UNKNOWN
Reconstruction: NOT_RUN
Verification: NOT_RUN
Accepted: false
Outputs: empty
```

### 27.4 Incorrect reconstructed result

Input:

```text
a = 2
b = 10
candidate x = 7
```

Verification:

```text
2 * 7 != 10
```

Expected:

```text
Decision: APPLY
Reconstruction: SUCCESS
Verification: FAIL
Accepted: false
Outputs: empty
```

The incorrect candidate MUST be introduced
through an internal verification test.

The normal runtime MUST NOT accept arbitrary
candidate output overrides from the RZIP document.

### 27.5 Rejection precedence

Input:

```text
a = 0
b = missing
```

Expected:

```text
Decision: REJECT
Reconstruction: NOT_RUN
Verification: NOT_RUN
Accepted: false
Outputs: empty
```

Known prohibitions MUST take precedence
over unresolved input conditions.

### 27.6 Exact rational reconstruction

Input:

```text
a = 3
b = 1
```

Expected:

```text
Decision: APPLY
Reconstruction: SUCCESS
Verification: PASS
Accepted: true
```

Output:

```json
{
  "x": {
    "numerator": 1,
    "denominator": 3
  }
}
```

### 27.7 Reconstruction error

A structurally valid fixture MAY be constructed
in which context checks permit an operation
that subsequently attempts division by zero.

Expected:

```text
Decision: APPLY
Reconstruction: ERROR
Verification: NOT_RUN
Accepted: false
Outputs: empty
```

This case confirms that arithmetic failures
cannot bypass the acceptance policy.

The reference implementation MAY perform cases
27.4 through 27.7 internally to preserve
the minimal repository structure.

---

## 28. Pattern Completion

Pattern Completion refers to identifying
potentially relevant stored reasoning skeletons.

```text
Current Input
      |
      v
Candidate Retrieval
      |
      v
Candidate Skeletons
```

Retrieved candidates MUST remain subject to
context evaluation.

Retrieval MUST NOT establish applicability.

Automated retrieval is outside v0.1.

The reference implementation uses explicitly
selected reasoning assets.

---

## 29. Pattern Separation

Pattern Separation refers to distinguishing
similar-looking problems with different
underlying conditions.

```text
Similar Symptoms
       |
       v
Context Comparison
       |
       +--> Applicable
       |
       +--> Prohibited
       |
       +--> Unresolved
```

Similarity MUST NOT override required conditions
or prohibited conditions.

RZIP v0.1 implements explicit context evaluation
as a limited foundation for future pattern
separation systems.

It does not implement an automated semantic
pattern separation engine.

---

## 30. Memory Consolidation and Forgetting

Future implementations MAY consolidate multiple
reasoning assets into more general structures.

```text
Experiences
     |
     v
Rules
     |
     v
Skeletons
     |
     v
Reusable Reasoning Assets
```

Consolidation SHOULD preserve:

- Relevant evidence.
- Provenance references.
- Safety-critical exceptions.
- Applicability conditions.
- Prohibited conditions.
- Verification requirements.

Low utilization frequency alone SHOULD NOT
justify removal of safety-critical information.

Automated consolidation and forgetting are
outside the implementation scope of v0.1.

---

## 31. Security Model

RZIP documents MUST be treated as untrusted data.

An RZIP document MUST NOT independently:

- Execute arbitrary code.
- Access the network.
- Modify external files.
- Invoke external tools.
- Grant permissions.
- Override human constraints.
- Disable verification.

The runtime MUST use an explicitly supported
operation vocabulary.

The reference implementation MUST NOT use
dynamic evaluation of document-provided expressions.

The following execution mechanisms MUST NOT
be used to interpret RZIP operations:

- eval
- exec
- Dynamic imports
- Shell command execution
- Deserialization of executable objects

The runtime SHOULD enforce limits on:

- Document size.
- Number of rules.
- Number of skeleton steps.
- Number of verification checks.
- Integer magnitude.
- Intermediate arithmetic growth.
- Execution duration.

Schema validation does not establish semantic safety.

Verification does not establish external authorization.

External actions remain subject to independent
authorization and governance.

---

## 32. Failure Classification

RZIP distinguishes document failures,
runtime decisions, reconstruction failures,
and verification failures.

| Category | Meaning |
|---|---|
| DOCUMENT_INVALID | Structural or semantic document validation failed |
| REJECT | Current context prohibits reconstruction |
| UNKNOWN | Current applicability cannot be established |
| RECONSTRUCTION_ERROR | An authorized reconstruction attempt failed |
| VERIFICATION_FAIL | A reconstructed result failed verification |
| SUCCESS | Reconstruction passed all required checks |

DOCUMENT_INVALID MUST NOT be interpreted
as a normal runtime applicability decision.

REJECT and UNKNOWN are expected runtime outcomes.

They are not implementation failures when
the behavior matches the declared test expectation.

---

## 33. Conformance Levels

### 33.1 Document conformance

A document conforms structurally when:

- It satisfies the JSON Schema.
- It contains the required layers.
- Its identifiers and references are valid.
- Its reasoning operations are supported.
- Its dependencies satisfy the v0.1 constraints.

### 33.2 Runtime conformance

A runtime conforms to the v0.1 reference profile
when it:

- Evaluates context deterministically.
- Implements APPLY, REJECT, and UNKNOWN.
- Preserves rejection precedence.
- Prevents unauthorized reconstruction.
- Performs supported arithmetic operations.
- Executes all required verification checks.
- Prevents acceptance after failures.

### 33.3 Fixture conformance

A validation fixture conforms when its actual
runtime outcome matches its declared expected
outcome.

A fixture expecting REJECT or UNKNOWN MAY
successfully pass validation.

---

## 34. Continuous Integration

GitHub Actions SHOULD execute the reference
validator on:

- Pushes.
- Pull requests.
- Manual workflow dispatch.

The reference validator MUST return:

- Exit code 0 when all required validation
  fixtures and internal checks succeed.
- A nonzero exit code when any required
  validation fails.

Passing CI demonstrates conformance to the
implemented reference cases.

It MUST NOT be interpreted as proof of:

- General reasoning correctness.
- Production-grade security.
- Cross-model interoperability.
- Reduced energy consumption.
- Reduced inference cost.
- Universal reconstruction validity.

---

## 35. Evaluation Requirements

Future experimental evaluation SHOULD compare:

### Baseline

Reasoning without a stored RZIP asset.

### RZIP-assisted reasoning

Reasoning reconstructed from a stored asset
under evaluated conditions.

Suggested metrics:

| Metric | Meaning |
|---|---|
| Accuracy | Correct outcomes |
| Latency | Total processing duration |
| Resource consumption | Total computational resources used |
| Misapplication rate | Incorrectly permitted reuse |
| Verification failure rate | Reconstructed outputs failing checks |
| Reuse rate | Successful reuse of stored structures |
| Storage overhead | Cost of retaining reasoning assets |

The evaluation MUST include relevant retrieval,
context evaluation, reconstruction, and verification
overheads when making efficiency claims.

Compression ratio alone is not a sufficient
measure of practical benefit.

No quantitative performance improvement
is claimed by RZIP v0.1.

---

## 36. Versioning

RZIP uses semantic versioning.

```text
MAJOR.MINOR.PATCH
```

The initial protocol version is:

```text
0.1.0
```

Future versions MAY introduce:

- Expanded operation vocabularies.
- Richer dependency structures.
- Branching reasoning skeletons.
- Automated pattern retrieval.
- Memory consolidation.
- Cross-model exchange profiles.
- Additional provenance mechanisms.

A v0.1 runtime MUST reject unsupported
document versions.

Future compatibility is not guaranteed
during the experimental 0.x series.

---

## 37. Repository Structure

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

The initial repository intentionally contains
eight files.

Additional validation cases MAY be implemented
within the reference validator.

---

## 38. Limitations

RZIP v0.1 is intentionally limited.

It demonstrates:

- Declarative reasoning representation.
- Context-dependent applicability.
- Deterministic arithmetic reconstruction.
- Explicit uncertainty.
- Result verification.
- Failure containment.

It does not demonstrate:

- General-purpose reasoning reconstruction.
- Natural-language semantic verification.
- Automatic reasoning extraction.
- Actual model compression.
- Proven inference cost reduction.
- General AI memory reconstruction.

The reference implementation is a minimal
technical foundation rather than a complete
reasoning engine.

---

## 39. Core Invariants

Every conforming RZIP v0.1 implementation
MUST preserve the following invariants.

### Invariant 1 — Context before reconstruction

```text
No APPLY
    =
No Reconstruction
```

### Invariant 2 — Verification before acceptance

```text
No PASS
    =
No Acceptance
```

### Invariant 3 — Explicit uncertainty

```text
UNKNOWN
    !=
APPLY
```

### Invariant 4 — Reconstruction is not truth

```text
Reconstructed
    !=
Verified
```

### Invariant 5 — Provenance is not authorization

```text
Stored Origin
    !=
Execution Permission
```

### Invariant 6 — No arbitrary execution

```text
Declarative Structure
    !=
Executable Program
```

### Invariant 7 — Failure containment

```text
Reconstruction Error
    =
No Accepted Output
```

### Invariant 8 — Structural reuse is conditional

```text
Similarity
    !=
Applicability
```

---

## 40. Closing Principle

RZIP does not preserve intelligence as a complete
historical sequence.

It preserves reusable structures through which
reasoning may emerge again under appropriate
conditions.

```text
Fact
  +
Rule
  +
Skeleton
  +
Context
  +
Verification
  =
Conditionally Reusable Reasoning
```

The purpose of reconstruction is not to reproduce
the past.

The purpose is to generate and verify reasoning
appropriate to the present.

> Preserve the structure.
> Reconstruct the reasoning.
> Verify before acceptance.

---

**End of RZIP Technical Specification v0.1**
