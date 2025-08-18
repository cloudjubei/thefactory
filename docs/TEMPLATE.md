# [PROJECT NAME] Specification

## Problem Statement
[Describe the specific problem this project solves. Be clear and concise. Example: "Convert CSV files to JSON format while preserving data types and handling errors gracefully."]

## Inputs
[Define all inputs with their types, formats, and constraints]

### Input 1: [Name]
- Type: [string/number/file/etc.]
- Format: [specific format requirements]
- Constraints: [size limits, valid ranges, required/optional]
- Example: `[provide example]`

### Input 2: [Name]
- Type: [type]
- Format: [format]
- Constraints: [constraints]
- Example: `[example]`

## Outputs
[Define all outputs with their types and formats]

### Success Output
- Type: [type]
- Format: [exact format specification]
- Example:
```
[example output]
```

### Error Outputs
- Condition: [when this error occurs]
  - Type: [type]
  - Format: [format]
  - Example: `[example]`

- Condition: [another error condition]
  - Type: [type]
  - Format: [format]
  - Example: `[example]`

## Constraints
[List hard requirements that cannot be violated]

- Performance: [e.g., "Process 1MB file in <1 second"]
- Resource: [e.g., "Memory usage <100MB"]
- Compatibility: [e.g., "Must work with Node.js 16+"]
- Security: [e.g., "No execution of user-provided code"]

## Success Criteria
[Numbered list of testable conditions that verify correct implementation]

1. [First testable criterion. Example: "Given valid input X, produces output Y in format Z"]
2. [Second criterion. Example: "Rejects invalid input with appropriate error message"]
3. [Third criterion. Example: "Processes 1000 records in under 10 seconds"]
4. [Continue numbering all criteria...]

## Edge Cases
[Explicitly define behavior for boundary conditions]

- Empty input: [what happens]
- Maximum size input: [what happens]
- Invalid format: [what happens]
- Concurrent access: [what happens if applicable]
- [Other edge cases specific to the problem]

## Examples

### Example 1: [Normal Case]
**Input:**
```
[example input]
```

**Output:**
```
[expected output]
```

### Example 2: [Edge Case]
**Input:**
```
[edge case input]
```

**Output:**
```
[expected output or error]
```

### Example 3: [Error Case]
**Input:**
```
[invalid input]
```

**Output:**
```
[expected error response]
```

## Non-Requirements
[Optional: Explicitly state what is NOT required to avoid scope creep]

- This specification does NOT require: [example: "GUI interface"]
- Out of scope: [example: "Authentication or user management"]

## Notes
[Optional: Additional context or clarifications]

- [Any additional notes that help understand the specification]
- [References to related specifications or standards]