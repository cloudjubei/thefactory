# Problem Statement
Describe the core problem the specification addresses. State the goal in simple, precise terms and define the stakeholders.

Key elements:
- What is being built and why
- Who benefits and how
- Scope and non-goals

# Inputs and Outputs
List all inputs the system consumes and the outputs it produces. Be explicit and unambiguous.

Include for each input/output:
- Name
- Type/format
- Source/Destination
- Validation rules
- Example value(s)

# Constraints
List limitations and rules that shape the solution.

Consider:
- Technical constraints (APIs, libraries, environment)
- Performance and scalability targets
- Security, privacy, and compliance
- Operational constraints (deployment, runtime)
- Compatibility and interoperability

# Success Criteria
Define how success is measured. These become acceptance tests and KPIs.

Examples:
- Files created/updated with specific sections
- Scripts executable with zero exit code
- Deterministic outputs based on inputs
- Quantitative SLAs (latency, throughput, uptime)

# Edge Cases
Identify unusual but possible scenarios and how the system should behave.

Consider:
- Empty, null, or malformed inputs
- Boundary values and large sizes
- Timeouts, retries, and partial failures
- Conflicts and race conditions

# Examples
Provide concrete, end-to-end examples illustrating expected behavior.

Example structure:
- Context: Short narrative of the scenario
- Input(s): Sample input payload(s)
- Steps: What the system does
- Output(s): Expected outputs with sample content
- Notes: Any caveats or clarifications