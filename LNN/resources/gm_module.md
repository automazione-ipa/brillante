## LNN Grounding Management Module (\_gm) Reference Guide

This document describes the internal grounding management utilities in the IBM LNN library (`lnn.symbolic._gm`). Grounding management is the process of handling first-order logic (FOL) groundings—assignments of variables to constant symbols—during inference.

---

### 1. Overview

* **Purpose**: Coordinate upward and downward propagation of truth bounds over formulas with variable groundings in FOL.
* **Key Concepts**:

  * **Grounding**: A specific assignment of variables (e.g., `('Alice',)` or `('Alice', 'Bob')`).
  * **Operator / Formula**: A logical connective or predicate node, with an associated set of groundings and data.
  * **Operand**: Sub-formula or child node.
  * **Upward pass**: Compute operator output bounds from operand bounds.
  * **Downward pass**: Propagate operator output bounds back to operands.

---

### 2. Main Functions

#### 2.1 `upward_bounds(operator, operands, groundings=None)`

```python
def upward_bounds(
    operator: Formula,
    operands: Tuple[Formula],
    groundings: Set[Union[str, Tuple[str, ...]]] = None,
) -> Union[
    None,
    Tuple[torch.Tensor, None],
    Tuple[torch.Tensor, Set[tuple[str]]]
]:
```

* **Description**: Performs the upward inference pass for `operator` given its `operands` and optional existing `groundings`.
* **Returns**:

  * `None` if no update or full contradiction.
  * `(input_bounds, None)` when no new groundings.
  * `(input_bounds, groundings)` when new groundings discovered.
* **Key Steps**:

  1. Skip if operator is propositional and contradictory.
  2. Call `_operational_bounds(..., Direction.UPWARD, ...)` to compute raw bounds.
  3. Filter out fully contradictory groundings.

#### 2.2 `downward_bounds(operator, operands, groundings=None)`

```python
def downward_bounds(
    operator: Formula,
    operands: Tuple[Formula],
    groundings: Set[Union[str, Tuple[str, ...]]] = None,
) -> Union[
    None,
    Tuple[torch.Tensor, torch.Tensor, None],
    Tuple[torch.Tensor, torch.Tensor, Set[tuple[str]]]
]:
```

* **Description**: Performs the downward inference pass, propagating operator output bounds to operands.
* **Returns**:

  * `None` if nothing to propagate.
  * `(output_bounds, input_bounds, None)` when no new groundings.
  * `(output_bounds, input_bounds, groundings)` when new groundings discovered.
* **Key Steps**:

  1. Check for propositional contradictions.
  2. Call `_operational_bounds(..., Direction.DOWNWARD, ...)`.
  3. Remove contradictory groundings and bounds.

---

### 3. Helper Routines

#### 3.1 `_operational_bounds(operator, direction, operands, groundings)`

* **Dispatches** to either propositional or FOL bounds computation.
* For **propositional** formulas, calls `_propositional_bounds`.
* For **FOL** formulas:

  1. Determine homogeneity and binding structure.
  2. Gather operand grounding tables into DataFrames.
  3. Perform outer joins (`_outer_join`, `_full_outer_join`) to align groundings.
  4. Use `_operator_groundings` and `_operand_groundings` to map to actual objects.
  5. Stack operand data to form input bounds tensor.
  6. For downward pass, also compute output bounds.

#### 3.2 `_is_contradiction(formula, operands)`

* Tests whether any operand or the formula itself is in a contradictory state.

### 4. Dataframe and Join Utilities

* **Grounding DataFrames**: Represent sets of groundings for each operand as pandas DataFrames with columns matching variable slots.
* **Join Functions**:

  * `_outer_join`, `_full_outer_join`: merge DataFrames to combine groundings across operands, preserving all combinations and handling empty cases.
  * `_hash_join`: efficient set-based intersection of groundings across operands.

---

### 5. Grounding Extraction

#### 5.1 `_operator_groundings(joined_df, operator)`

* Converts DataFrame rows into grounded formula objects via `operator._ground(...)`.
* Returns a list of grounding objects for the operator.

#### 5.2 `_operand_groundings(joined_df, operator, bindings)`

* Generates grounding objects for each operand, respecting fixed bindings.
* Ensures each operand node’s grounding table is updated.

---

### 6. Propositional vs FOL Branches

* **Propositional** (*no variables*): simple stacking of operand data tensors.
* **FOL**: involves dynamic introduction of new groundings, DataFrame merges, and per-grounding tensor extraction.

---

### 7. Usage in Model Inference

* Called internally by `Model.infer()` during upward/downward propagation.
* Not typically invoked directly by end-users.
* Ensures scalable handling of FOL predicates with many groundings.

---

### 8. Errors & Warnings

* **FutureWarning** from pandas concatenation: benign, pending upstream fix.
* Ensure operand grounding tables are maintained before inference.

---

### 9. Summary

The `_gm` module is crucial for correctly propagating belief bounds over FOL formulas in LNN. It leverages DataFrame joins to manage groundings, then uses tensor operations for neural bounds computation. Understanding these internals can aid in debugging complex FOL reasoning tasks.

---

*Document auto-generated for reference.*
