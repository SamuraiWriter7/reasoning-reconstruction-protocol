from __future__ import annotations

import copy
import json
import math
import operator
import sys

from fractions import Fraction
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker


# ============================================================
# RZIP v0.1 Reference Validator
# Reasoning Reconstruction and Compression Protocol
# ============================================================

ROOT = Path(__file__).resolve().parents[1]

SCHEMA_PATH = (
    ROOT
    / "schemas"
    / "reasoning-skeleton.schema.json"
)

EXAMPLES_DIR = ROOT / "examples"

PROTOCOL = "RZIP"
VERSION = "0.1.0"

APPLY = "APPLY"
REJECT = "REJECT"
UNKNOWN = "UNKNOWN"

SUCCESS = "SUCCESS"
ERROR = "ERROR"

PASS = "PASS"
FAIL = "FAIL"
NOT_RUN = "NOT_RUN"

MAX_DOCUMENT_BYTES = 1_000_000
MAX_RULES = 100
MAX_STEPS = 100
MAX_CHECKS = 100
MAX_INTEGER_BITS = 256
MAX_FRACTION_BITS = 4096

MISSING = object()


# ============================================================
# Exceptions
# ============================================================

class DocumentValidationError(Exception):
    """Invalid RZIP document."""


class ReconstructionError(Exception):
    """Reasoning reconstruction failed."""


# ============================================================
# JSON Loading
# ============================================================

def reject_duplicate_keys(
    pairs: list[tuple[str, Any]],
) -> dict[str, Any]:

    result = {}

    for key, value in pairs:

        if key in result:
            raise DocumentValidationError(
                f"Duplicate JSON key: {key}"
            )

        result[key] = value

    return result


def reject_json_constant(value: str) -> Any:

    raise DocumentValidationError(
        f"Unsupported JSON constant: {value}"
    )


def load_json(path: Path) -> dict[str, Any]:

    if not path.is_file():
        raise DocumentValidationError(
            f"File not found: {path}"
        )

    try:

        with path.open("rb") as handle:
            raw = handle.read(MAX_DOCUMENT_BYTES + 1)

        if len(raw) > MAX_DOCUMENT_BYTES:
            raise DocumentValidationError(
                f"Document exceeds size limit: {path}"
            )

        document = json.loads(
            raw.decode("utf-8"),
            object_pairs_hook=reject_duplicate_keys,
            parse_constant=reject_json_constant,
        )

    except (
        OSError,
        UnicodeError,
        ValueError,
        RecursionError,
    ) as exc:

        raise DocumentValidationError(
            f"Unable to load JSON: {path}: {exc}"
        ) from exc

    if not isinstance(document, dict):
        raise DocumentValidationError(
            f"JSON root must be an object: {path}"
        )

    return document


# ============================================================
# Schema Validation
# ============================================================

def create_schema_validator() -> Draft202012Validator:

    schema = load_json(SCHEMA_PATH)

    Draft202012Validator.check_schema(schema)

    return Draft202012Validator(
        schema,
        format_checker=FormatChecker(),
    )


def validate_schema(
    document: dict[str, Any],
    validator: Draft202012Validator,
) -> None:

    errors = sorted(
        validator.iter_errors(document),
        key=lambda error: tuple(
            str(item)
            for item in error.absolute_path
        ),
    )

    if not errors:
        return

    messages = []

    for error in errors:

        path = ".".join(
            str(item)
            for item in error.absolute_path
        )

        messages.append(
            f"{path or '<root>'}: {error.message}"
        )

    raise DocumentValidationError(
        "Schema validation failed:\n"
        + "\n".join(messages)
    )


# ============================================================
# Numeric Domain
# ============================================================

def validate_integer(
    value: Any,
    location: str,
    max_bits: int = MAX_INTEGER_BITS,
) -> None:

    # bool is a subclass of int in Python.
    # Exact type checking is intentional.

    if type(value) is not int:
        raise DocumentValidationError(
            f"{location}: expected an integer"
        )

    if value.bit_length() > max_bits:
        raise DocumentValidationError(
            f"{location}: integer magnitude exceeds limit"
        )


def ensure_fraction_limit(
    value: Fraction,
) -> Fraction:

    numerator_bits = value.numerator.bit_length()
    denominator_bits = value.denominator.bit_length()

    if (
        numerator_bits > MAX_FRACTION_BITS
        or denominator_bits > MAX_FRACTION_BITS
    ):
        raise ReconstructionError(
            "Intermediate arithmetic exceeds resource limit"
        )

    return value


def validate_output_value(
    value: Any,
    location: str,
) -> None:

    if type(value) is int:

        validate_integer(
            value,
            location,
            MAX_FRACTION_BITS,
        )

        return

    if not isinstance(value, dict):

        raise DocumentValidationError(
            f"{location}: invalid output representation"
        )

    if set(value) != {"numerator", "denominator"}:

        raise DocumentValidationError(
            f"{location}: invalid rational representation"
        )

    numerator = value["numerator"]
    denominator = value["denominator"]

    validate_integer(
        numerator,
        f"{location}.numerator",
        MAX_FRACTION_BITS,
    )

    validate_integer(
        denominator,
        f"{location}.denominator",
        MAX_FRACTION_BITS,
    )

    if denominator < 2:

        raise DocumentValidationError(
            f"{location}: denominator must be at least 2"
        )

    if math.gcd(numerator, denominator) != 1:

        raise DocumentValidationError(
            f"{location}: rational value must be reduced"
        )


def serialize_fraction(
    value: Fraction,
) -> int | dict[str, int]:

    if value.denominator == 1:
        return value.numerator

    return {
        "numerator": value.numerator,
        "denominator": value.denominator,
    }


# ============================================================
# Operation Vocabulary
# ============================================================

ARITHMETIC_OPERATIONS = {
    "add": operator.add,
    "subtract": operator.sub,
    "multiply": operator.mul,
    "divide": operator.truediv,
}

COMPARISON_OPERATORS = {
    "eq": operator.eq,
    "ne": operator.ne,
    "gt": operator.gt,
    "gte": operator.ge,
    "lt": operator.lt,
    "lte": operator.le,
}


def execute_operation(
    operation: str,
    values: list[Fraction],
    *,
    allow_identity: bool = False,
) -> Fraction:

    if operation == "identity":

        if not allow_identity or len(values) != 1:

            raise ReconstructionError(
                "Invalid identity operation"
            )

        return ensure_fraction_limit(values[0])

    if operation not in ARITHMETIC_OPERATIONS:

        raise ReconstructionError(
            f"Unsupported operation: {operation}"
        )

    if len(values) != 2:

        raise ReconstructionError(
            f"Invalid operation arity: {operation}"
        )

    if operation == "divide" and values[1] == 0:

        raise ReconstructionError(
            "Division by zero"
        )

    try:

        result = ARITHMETIC_OPERATIONS[operation](
            values[0],
            values[1],
        )

    except ArithmeticError as exc:

        raise ReconstructionError(
            f"Arithmetic failure: {exc}"
        ) from exc

    return ensure_fraction_limit(result)


# ============================================================
# Identifier Integrity
# ============================================================

def validate_identifiers(
    document: dict[str, Any],
) -> None:

    identifiers = set()

    objects = [
        *document["facts"],
        *document["rules"],
        document["skeleton"],
        *document["verification"]["checks"],
        *document["claims"],
    ]

    for item in objects:

        identifier = item["id"]

        if identifier in identifiers:

            raise DocumentValidationError(
                f"Duplicate identifier: {identifier}"
            )

        identifiers.add(identifier)


# ============================================================
# Resource Limits
# ============================================================

def validate_resource_limits(
    document: dict[str, Any],
) -> None:

    if len(document["rules"]) > MAX_RULES:

        raise DocumentValidationError(
            "Rule count exceeds resource limit"
        )

    if len(document["skeleton"]["steps"]) > MAX_STEPS:

        raise DocumentValidationError(
            "Skeleton step count exceeds resource limit"
        )

    if (
        len(document["verification"]["checks"])
        > MAX_CHECKS
    ):

        raise DocumentValidationError(
            "Verification check count exceeds resource limit"
        )


# ============================================================
# Operand Validation
# ============================================================

def validate_operand(
    operand: dict[str, Any],
    allowed_variables: set[str],
    location: str,
) -> None:

    if set(operand) == {"ref"}:

        reference = operand["ref"]

        if reference not in allowed_variables:

            raise DocumentValidationError(
                f"{location}: undeclared reference "
                f"{reference}"
            )

        return

    if set(operand) == {"value"}:

        validate_integer(
            operand["value"],
            f"{location}.value",
        )

        return

    raise DocumentValidationError(
        f"{location}: invalid operand"
    )


# ============================================================
# Context Validation
# ============================================================

def validate_context(
    document: dict[str, Any],
) -> set[str]:

    context = document["context"]

    declared_inputs = set(
        context["required_inputs"]
    )

    for name, value in context["inputs"].items():

        if name not in declared_inputs:

            raise DocumentValidationError(
                f"Undeclared context input: {name}"
            )

        validate_integer(
            value,
            f"context.inputs.{name}",
        )

    condition_groups = (
        "required_conditions",
        "prohibited_conditions",
    )

    for group in condition_groups:

        for index, condition in enumerate(
            context[group]
        ):

            location = f"context.{group}[{index}]"

            if (
                condition["operator"]
                not in COMPARISON_OPERATORS
            ):

                raise DocumentValidationError(
                    f"{location}: unsupported comparison"
                )

            validate_operand(
                condition["left"],
                declared_inputs,
                f"{location}.left",
            )

            validate_operand(
                condition["right"],
                declared_inputs,
                f"{location}.right",
            )

    return declared_inputs


# ============================================================
# Rule and Skeleton Validation
# ============================================================

def validate_rules_and_skeleton(
    document: dict[str, Any],
    declared_inputs: set[str],
) -> set[str]:

    rules = {
        rule["id"]: rule
        for rule in document["rules"]
    }

    steps = document["skeleton"]["steps"]

    available_variables = set(declared_inputs)

    declared_outputs = set()
    reconstructed_outputs = set()
    visited_rules = set()

    all_declared_variables = (
        declared_inputs
        | {
            rule["output"]
            for rule in rules.values()
        }
    )

    # Validate every stored rule.

    for rule in rules.values():

        rule_id = rule["id"]
        output = rule["output"]

        if (
            rule["operation"]
            not in ARITHMETIC_OPERATIONS
        ):

            raise DocumentValidationError(
                f"{rule_id}: unsupported operation"
            )

        if len(rule["inputs"]) != 2:

            raise DocumentValidationError(
                f"{rule_id}: invalid operation arity"
            )

        if output in declared_inputs:

            raise DocumentValidationError(
                f"{rule_id}: cannot overwrite context input"
            )

        if output in declared_outputs:

            raise DocumentValidationError(
                f"{rule_id}: duplicate rule output {output}"
            )

        if output in rule["inputs"]:

            raise DocumentValidationError(
                f"{rule_id}: self-dependent rule"
            )

        for reference in rule["inputs"]:

            if reference not in all_declared_variables:

                raise DocumentValidationError(
                    f"{rule_id}: undeclared variable "
                    f"{reference}"
                )

        declared_outputs.add(output)

    # Require all rules to belong to the active skeleton.
    # This keeps the v0.1 reference profile bounded.

    if set(steps) != set(rules):

        raise DocumentValidationError(
            "Every rule must occur in the skeleton "
            "and every skeleton step must reference a rule"
        )

    # Validate execution order.

    for rule_id in steps:

        if rule_id in visited_rules:

            raise DocumentValidationError(
                f"Repeated skeleton step: {rule_id}"
            )

        if rule_id not in rules:

            raise DocumentValidationError(
                f"Unknown skeleton rule: {rule_id}"
            )

        rule = rules[rule_id]

        for reference in rule["inputs"]:

            if reference not in available_variables:

                raise DocumentValidationError(
                    f"{rule_id}: unavailable or forward "
                    f"dependency {reference}"
                )

        output = rule["output"]

        available_variables.add(output)
        reconstructed_outputs.add(output)
        visited_rules.add(rule_id)

    return reconstructed_outputs


# ============================================================
# Verification Structure Validation
# ============================================================

def validate_verification(
    document: dict[str, Any],
    declared_inputs: set[str],
    reconstructed_outputs: set[str],
) -> None:

    allowed_variables = (
        declared_inputs
        | reconstructed_outputs
    )

    covered_outputs = set()

    for check in document["verification"]["checks"]:

        check_id = check["id"]
        operation = check["operation"]
        inputs = check["inputs"]

        if operation == "identity":

            expected_arity = 1

        elif operation in ARITHMETIC_OPERATIONS:

            expected_arity = 2

        else:

            raise DocumentValidationError(
                f"{check_id}: unsupported verification operation"
            )

        if len(inputs) != expected_arity:

            raise DocumentValidationError(
                f"{check_id}: invalid verification arity"
            )

        if (
            check["operator"]
            not in COMPARISON_OPERATORS
        ):

            raise DocumentValidationError(
                f"{check_id}: unsupported comparison"
            )

        for reference in inputs:

            if reference not in allowed_variables:

                raise DocumentValidationError(
                    f"{check_id}: unknown verification "
                    f"reference {reference}"
                )

            if reference in reconstructed_outputs:

                covered_outputs.add(reference)

        validate_operand(
            check["expected"],
            allowed_variables,
            f"verification.{check_id}.expected",
        )

        expected_reference = check["expected"].get("ref")

        if expected_reference in reconstructed_outputs:

            covered_outputs.add(expected_reference)

    missing_coverage = (
        reconstructed_outputs
        - covered_outputs
    )

    if missing_coverage:

        raise DocumentValidationError(
            "Missing verification coverage: "
            + ", ".join(sorted(missing_coverage))
        )


# ============================================================
# Claim Reference Validation
# ============================================================

def validate_claims(
    document: dict[str, Any],
) -> None:

    allowed_sources = {
        item["id"]
        for item in document["facts"]
    }

    allowed_sources.update(
        item["id"]
        for item in document["rules"]
    )

    allowed_sources.add(
        document["skeleton"]["id"]
    )

    allowed_sources.update(
        item["id"]
        for item in document["verification"]["checks"]
    )

    for claim in document["claims"]:

        if claim["source"] not in allowed_sources:

            raise DocumentValidationError(
                f"{claim['id']}: unknown claim source "
                f"{claim['source']}"
            )


# ============================================================
# Expected Result Validation
# ============================================================

def validate_expected_result(
    document: dict[str, Any],
    reconstructed_outputs: set[str],
) -> None:

    if "expected" not in document:
        return

    outputs = document["expected"]["outputs"]

    for name, value in outputs.items():

        if name not in reconstructed_outputs:

            raise DocumentValidationError(
                f"Unexpected output variable: {name}"
            )

        validate_output_value(
            value,
            f"expected.outputs.{name}",
        )

    if document["expected"]["accepted"]:

        if set(outputs) != reconstructed_outputs:

            raise DocumentValidationError(
                "Accepted expected result must include "
                "all reconstructed outputs"
            )


# ============================================================
# Complete Document Validation
# ============================================================

def validate_document(
    document: dict[str, Any],
    validator: Draft202012Validator,
) -> None:

    validate_schema(
        document,
        validator,
    )

    if document["protocol"] != PROTOCOL:

        raise DocumentValidationError(
            "Unsupported protocol"
        )

    if document["version"] != VERSION:

        raise DocumentValidationError(
            "Unsupported protocol version"
        )

    validate_resource_limits(document)

    validate_identifiers(document)

    declared_inputs = validate_context(document)

    reconstructed_outputs = (
        validate_rules_and_skeleton(
            document,
            declared_inputs,
        )
    )

    validate_verification(
        document,
        declared_inputs,
        reconstructed_outputs,
    )

    validate_claims(document)

    validate_expected_result(
        document,
        reconstructed_outputs,
    )


# ============================================================
# Operand Resolution
# ============================================================

def resolve_operand(
    operand: dict[str, Any],
    environment: dict[str, Fraction],
) -> Any:

    if "value" in operand:

        return Fraction(operand["value"])

    return environment.get(
        operand["ref"],
        MISSING,
    )


# ============================================================
# Three-Valued Condition Evaluation
# ============================================================

def evaluate_condition(
    condition: dict[str, Any],
    environment: dict[str, Fraction],
) -> bool | None:

    left = resolve_operand(
        condition["left"],
        environment,
    )

    right = resolve_operand(
        condition["right"],
        environment,
    )

    if left is MISSING or right is MISSING:

        return None

    comparison = COMPARISON_OPERATORS[
        condition["operator"]
    ]

    return bool(
        comparison(left, right)
    )


# ============================================================
# Context Decision
# ============================================================

def evaluate_context(
    document: dict[str, Any],
) -> str:

    context = document["context"]

    environment = {
        name: Fraction(value)
        for name, value in context["inputs"].items()
    }

    required_results = [
        evaluate_condition(
            condition,
            environment,
        )
        for condition in context["required_conditions"]
    ]

    prohibited_results = [
        evaluate_condition(
            condition,
            environment,
        )
        for condition in context["prohibited_conditions"]
    ]

    # Priority 1: REJECT

    if any(
        result is False
        for result in required_results
    ):

        return REJECT

    if any(
        result is True
        for result in prohibited_results
    ):

        return REJECT

    # Priority 2: UNKNOWN

    missing_inputs = (
        set(context["required_inputs"])
        - set(environment)
    )

    if missing_inputs:

        return UNKNOWN

    if any(
        result is None
        for result in required_results
    ):

        return UNKNOWN

    if any(
        result is None
        for result in prohibited_results
    ):

        return UNKNOWN

    # Priority 3: APPLY

    return APPLY


# ============================================================
# Reasoning Reconstruction
# ============================================================

def reconstruct_reasoning(
    document: dict[str, Any],
) -> tuple[
    dict[str, Fraction],
    dict[str, Fraction],
]:

    if evaluate_context(document) != APPLY:

        raise ReconstructionError(
            "Reconstruction requires APPLY"
        )

    environment = {
        name: Fraction(value)
        for name, value in (
            document["context"]["inputs"].items()
        )
    }

    rules = {
        rule["id"]: rule
        for rule in document["rules"]
    }

    outputs = {}

    for rule_id in document["skeleton"]["steps"]:

        rule = rules[rule_id]

        try:

            values = [
                environment[reference]
                for reference in rule["inputs"]
            ]

        except KeyError as exc:

            raise ReconstructionError(
                f"Unavailable rule input: {exc}"
            ) from exc

        result = execute_operation(
            rule["operation"],
            values,
        )

        output = rule["output"]

        if output in environment:

            raise ReconstructionError(
                f"Output overwrite prohibited: {output}"
            )

        environment[output] = result
        outputs[output] = result

    return environment, outputs


# ============================================================
# Result Verification
# ============================================================

def verify_reasoning(
    document: dict[str, Any],
    environment: dict[str, Fraction],
) -> str:

    all_checks_passed = True

    for check in document["verification"]["checks"]:

        try:

            values = [
                environment[reference]
                for reference in check["inputs"]
            ]

            actual = execute_operation(
                check["operation"],
                values,
                allow_identity=True,
            )

            expected = resolve_operand(
                check["expected"],
                environment,
            )

            if expected is MISSING:

                all_checks_passed = False
                continue

            comparison = COMPARISON_OPERATORS[
                check["operator"]
            ]

            if not comparison(actual, expected):

                all_checks_passed = False

        except (
            KeyError,
            ArithmeticError,
            ReconstructionError,
        ):

            all_checks_passed = False

    return PASS if all_checks_passed else FAIL


# ============================================================
# Runtime Result
# ============================================================

def make_result(
    decision: str,
    reconstruction: str,
    verification: str,
    outputs: dict[str, Fraction] | None = None,
) -> dict[str, Any]:

    accepted = (
        decision == APPLY
        and reconstruction == SUCCESS
        and verification == PASS
    )

    serialized_outputs = {}

    if accepted and outputs is not None:

        serialized_outputs = {
            name: serialize_fraction(value)
            for name, value in outputs.items()
        }

    return {
        "decision": decision,
        "reconstruction": reconstruction,
        "verification": verification,
        "accepted": accepted,
        "outputs": serialized_outputs,
    }


# ============================================================
# Reference Runtime
# ============================================================

def run_document(
    document: dict[str, Any],
    validator: Draft202012Validator,
) -> dict[str, Any]:

    validate_document(
        document,
        validator,
    )

    decision = evaluate_context(document)

    if decision != APPLY:

        return make_result(
            decision,
            NOT_RUN,
            NOT_RUN,
        )

    try:

        environment, outputs = (
            reconstruct_reasoning(document)
        )

    except ReconstructionError:

        return make_result(
            APPLY,
            ERROR,
            NOT_RUN,
        )

    verification = verify_reasoning(
        document,
        environment,
    )

    return make_result(
        APPLY,
        SUCCESS,
        verification,
        outputs,
    )


# ============================================================
# Fixture Assertions
# ============================================================

def assert_result(
    actual: dict[str, Any],
    expected: dict[str, Any],
    name: str,
) -> None:

    if actual != expected:

        actual_text = json.dumps(
            actual,
            indent=2,
            sort_keys=True,
        )

        expected_text = json.dumps(
            expected,
            indent=2,
            sort_keys=True,
        )

        raise AssertionError(
            f"{name}: runtime result mismatch\n"
            f"Expected:\n{expected_text}\n"
            f"Actual:\n{actual_text}"
        )


def validate_fixture(
    path: Path,
    validator: Draft202012Validator,
) -> dict[str, Any]:

    document = load_json(path)

    original = copy.deepcopy(document)

    if "expected" not in document:

        raise DocumentValidationError(
            f"Missing expected result: {path.name}"
        )

    actual = run_document(
        document,
        validator,
    )

    assert_result(
        actual,
        document["expected"],
        path.name,
    )

    if document != original:

        raise AssertionError(
            f"{path.name}: runtime modified document"
        )

    print(
        f"[PASS] {path.name}: "
        f"{actual['decision']} / "
        f"{actual['reconstruction']} / "
        f"{actual['verification']}"
    )

    return document


# ============================================================
# Internal Test Helpers
# ============================================================

def clone_without_expected(
    document: dict[str, Any],
) -> dict[str, Any]:

    cloned = copy.deepcopy(document)

    cloned.pop("expected", None)

    return cloned


def expect_invalid(
    name: str,
    document: dict[str, Any],
    validator: Draft202012Validator,
) -> None:

    try:

        run_document(
            document,
            validator,
        )

    except DocumentValidationError:

        print(f"[PASS] {name}")

        return

    raise AssertionError(
        f"{name}: invalid document was accepted"
    )


# ============================================================
# Internal Test 1
# Incorrect Reconstructed Result
# ============================================================

def test_verification_failure(
    base: dict[str, Any],
    validator: Draft202012Validator,
) -> None:

    document = clone_without_expected(base)

    validate_document(
        document,
        validator,
    )

    decision = evaluate_context(document)

    if decision != APPLY:

        raise AssertionError(
            "Verification failure test requires APPLY"
        )

    environment, outputs = reconstruct_reasoning(
        document
    )

    # Internal test only.
    # Candidate overrides are not exposed by the runtime.

    environment["x"] = Fraction(7)
    outputs["x"] = Fraction(7)

    verification = verify_reasoning(
        document,
        environment,
    )

    actual = make_result(
        decision,
        SUCCESS,
        verification,
        outputs,
    )

    expected = {
        "decision": APPLY,
        "reconstruction": SUCCESS,
        "verification": FAIL,
        "accepted": False,
        "outputs": {},
    }

    assert_result(
        actual,
        expected,
        "verification_failure",
    )

    print("[PASS] verification_failure")


# ============================================================
# Internal Test 2
# Rejection Precedence
# ============================================================

def test_rejection_precedence(
    base: dict[str, Any],
    validator: Draft202012Validator,
) -> None:

    document = clone_without_expected(base)

    document["context"]["inputs"] = {
        "a": 0,
    }

    actual = run_document(
        document,
        validator,
    )

    expected = {
        "decision": REJECT,
        "reconstruction": NOT_RUN,
        "verification": NOT_RUN,
        "accepted": False,
        "outputs": {},
    }

    assert_result(
        actual,
        expected,
        "rejection_precedence",
    )

    print("[PASS] rejection_precedence")


# ============================================================
# Internal Test 3
# Exact Rational Reconstruction
# ============================================================

def test_rational_reconstruction(
    base: dict[str, Any],
    validator: Draft202012Validator,
) -> None:

    document = clone_without_expected(base)

    document["context"]["inputs"] = {
        "a": 3,
        "b": 1,
    }

    actual = run_document(
        document,
        validator,
    )

    expected = {
        "decision": APPLY,
        "reconstruction": SUCCESS,
        "verification": PASS,
        "accepted": True,
        "outputs": {
            "x": {
                "numerator": 1,
                "denominator": 3,
            }
        },
    }

    assert_result(
        actual,
        expected,
        "rational_reconstruction",
    )

    print("[PASS] rational_reconstruction")


# ============================================================
# Internal Test 4
# Reconstruction Error
# ============================================================

def test_reconstruction_error(
    base: dict[str, Any],
    validator: Draft202012Validator,
) -> None:

    document = clone_without_expected(base)

    document["context"]["inputs"] = {
        "a": 0,
        "b": 10,
    }

    # Deliberately remove contextual protection
    # to test arithmetic failure containment.

    document["context"]["required_conditions"] = []
    document["context"]["prohibited_conditions"] = []

    actual = run_document(
        document,
        validator,
    )

    expected = {
        "decision": APPLY,
        "reconstruction": ERROR,
        "verification": NOT_RUN,
        "accepted": False,
        "outputs": {},
    }

    assert_result(
        actual,
        expected,
        "reconstruction_error",
    )

    print("[PASS] reconstruction_error")


# ============================================================
# Internal Test 5
# Expected Result Independence
# ============================================================

def test_expected_independence(
    base: dict[str, Any],
    validator: Draft202012Validator,
) -> None:

    document = copy.deepcopy(base)

    document["expected"]["outputs"]["x"] = 7

    actual = run_document(
        document,
        validator,
    )

    correct = {
        "decision": APPLY,
        "reconstruction": SUCCESS,
        "verification": PASS,
        "accepted": True,
        "outputs": {
            "x": 5,
        },
    }

    assert_result(
        actual,
        correct,
        "expected_independence",
    )

    if actual == document["expected"]:

        raise AssertionError(
            "Runtime incorrectly used expected output"
        )

    print("[PASS] expected_independence")


# ============================================================
# Structural Safety Tests
# ============================================================

def run_structural_tests(
    base: dict[str, Any],
    validator: Draft202012Validator,
) -> int:

    tests = []

    document = clone_without_expected(base)

    document["rules"][0]["id"] = (
        document["facts"][0]["id"]
    )

    tests.append(
        ("duplicate_identifier", document)
    )

    document = clone_without_expected(base)

    document["skeleton"]["steps"] = [
        "UNDECLARED_RULE"
    ]

    tests.append(
        ("unknown_rule_reference", document)
    )

    document = clone_without_expected(base)

    document["rules"][0]["inputs"] = [
        "b",
        "x",
    ]

    tests.append(
        ("self_dependency", document)
    )

    document = clone_without_expected(base)

    document["context"]["inputs"]["extra"] = 1

    tests.append(
        ("undeclared_input", document)
    )

    document = clone_without_expected(base)

    document["context"]["inputs"]["a"] = True

    tests.append(
        ("boolean_input", document)
    )

    document = clone_without_expected(base)

    document["context"]["inputs"]["a"] = 2.0

    tests.append(
        ("floating_point_input", document)
    )

    document = clone_without_expected(base)

    document["context"]["required_conditions"][0][
        "left"
    ] = {
        "ref": "undeclared",
    }

    tests.append(
        ("unknown_context_reference", document)
    )

    document = clone_without_expected(base)

    document["verification"]["checks"][0][
        "inputs"
    ] = [
        "a",
        "b",
    ]

    tests.append(
        ("missing_verification_coverage", document)
    )

    document = clone_without_expected(base)

    document["claims"][0]["source"] = (
        "UNDECLARED_SOURCE"
    )

    tests.append(
        ("unknown_claim_source", document)
    )

    document = clone_without_expected(base)

    document["rules"][0]["operation"] = (
        "execute_code"
    )

    tests.append(
        ("unsupported_operation", document)
    )

    document = clone_without_expected(base)

    document["metadata"]["created_at"] = (
        "invalid-date"
    )

    tests.append(
        ("invalid_timestamp", document)
    )

    document = clone_without_expected(base)

    document["rules"][0]["output"] = "a"

    tests.append(
        ("context_input_overwrite", document)
    )

    document = copy.deepcopy(base)

    document["expected"]["outputs"]["x"] = {
        "numerator": 2,
        "denominator": 4,
    }

    tests.append(
        ("noncanonical_rational", document)
    )

    document = copy.deepcopy(base)

    document["expected"]["verification"] = FAIL

    tests.append(
        ("invalid_acceptance_state", document)
    )

    document = clone_without_expected(base)

    document["rules"].append(
        {
            "id": "P002",
            "description": "Consume x before it exists.",
            "operation": "add",
            "inputs": ["x", "a"],
            "output": "y",
        }
    )

    document["skeleton"]["steps"] = [
        "P002",
        "P001",
    ]

    tests.append(
        ("forward_dependency", document)
    )

    for name, document in tests:

        expect_invalid(
            name,
            document,
            validator,
        )

    return len(tests)


# ============================================================
# JSON Safety Tests
# ============================================================

def run_json_safety_tests() -> int:

    malformed_inputs = [
        (
            "duplicate_json_key",
            '{"a": 1, "a": 2}',
        ),
        (
            "nonstandard_nan",
            '{"a": NaN}',
        ),
        (
            "nonstandard_infinity",
            '{"a": Infinity}',
        ),
    ]

    for name, source in malformed_inputs:

        try:

            json.loads(
                source,
                object_pairs_hook=reject_duplicate_keys,
                parse_constant=reject_json_constant,
            )

        except DocumentValidationError:

            print(f"[PASS] {name}")

            continue

        raise AssertionError(
            f"{name}: invalid JSON was accepted"
        )

    return len(malformed_inputs)


# ============================================================
# Main Validation Pipeline
# ============================================================

def main() -> int:

    print("=" * 60)
    print("RZIP v0.1 Reference Validator")
    print("=" * 60)

    try:

        validator = create_schema_validator()

        print("[PASS] JSON Schema definition")

        print()
        print("--- Example Fixtures ---")

        fixture_names = [
            "valid.json",
            "denied.json",
            "unknown.json",
        ]

        fixtures = {}

        for name in fixture_names:

            fixtures[name] = validate_fixture(
                EXAMPLES_DIR / name,
                validator,
            )

        base = fixtures["valid.json"]

        print()
        print("--- Internal Runtime Tests ---")

        runtime_tests = [
            test_verification_failure,
            test_rejection_precedence,
            test_rational_reconstruction,
            test_reconstruction_error,
            test_expected_independence,
        ]

        for test in runtime_tests:

            test(
                base,
                validator,
            )

        print()
        print("--- Structural Safety Tests ---")

        structural_count = run_structural_tests(
            base,
            validator,
        )

        print()
        print("--- JSON Safety Tests ---")

        json_count = run_json_safety_tests()

        total = (
            len(fixture_names)
            + len(runtime_tests)
            + structural_count
            + json_count
        )

        print()
        print("=" * 60)
        print(f"All {total} validation cases passed.")
        print("RZIP v0.1 reference validation successful.")
        print("=" * 60)

        return 0

    except Exception as exc:

        print(
            f"\n[FAIL] {type(exc).__name__}: {exc}",
            file=sys.stderr,
        )

        return 1


if __name__ == "__main__":
    sys.exit(main())
