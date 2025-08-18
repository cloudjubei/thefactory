# Feature Format

Follows exactly the same format as a task defined in the [TASK_FORMAT.md](TASK_FORMAT.md), with the extra fields defined below:

```
   Dependencies: [Optional] Features that must be completed first. This might be used to define a placeholder feature to group a set of features together, so that other features can depend on the group as a whole.
```

## Field Definitions

### Dependencies
Lists feature IDs that must be completed before this feature can begin. Format, comma and space separate list of IDs: `2, 5`

## Examples

### Simple Feature
```
4) + Create specification template
   Description: Create a reusable template for writing new specifications
   Acceptance: TEMPLATE.md exists and includes all sections from SPECIFICATION_GUIDE.md. Each section holds a placeholder example.
```

### Complex Feature
```
5) - Implement specification validation
   Description: Create a tool that validates specifications against our guide
   Acceptance: Script can identify at least 3 issues in a bad spec and passes a good spec
   Dependencies: 4
   Output: validate_spec.js script
```

### Group Feature
```
6) ~ Specification Features
   Description: Feature group
   Acceptance: All dependencies are done
   Dependencies: 4, 5
```