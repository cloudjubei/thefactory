# Specification Guide

## What is a Specification?
A specification is a complete description of WHAT needs to be achieved, independent of HOW it will be implemented. It defines the problem, constraints, and success criteria so precisely that multiple implementations would produce functionally identical results.

## Core Components of a Specification

### 1. Problem Statement
Clear description of what problem is being solved.

### 2. Inputs and Outputs
- What goes in (data, parameters, conditions)
- What comes out (results, side effects, state changes)

### 3. Constraints
Hard boundaries that cannot be violated (performance, resources, compatibility).

### 4. Success Criteria
Measurable conditions that determine if the specification has been correctly implemented.

### 5. Edge Cases
Explicit handling of boundary conditions and exceptional scenarios.

## Success Criteria Explained
Success criteria are testable statements that can be objectively verified. They answer: "How do we know this works?"

Good success criteria are:
- **Binary**: Either met or not met, no ambiguity
- **Measurable**: Can be tested programmatically or manually
- **Complete**: Cover all critical aspects of the problem
- **Independent**: Each criterion can be tested separately

## Example: Good vs Bad Specification

### ❌ Bad Specification: "User Login System"
```
Create a login system where users can log in with their credentials.
It should be secure and fast.
Users should be able to reset their password if they forget it.
```

**Why it's bad:**
- "Secure" and "fast" are undefined
- No input/output formats specified
- No error handling defined
- Success criteria are implicit and untestable

### ✅ Good Specification: "User Authentication Endpoint"
```
PROBLEM: Authenticate users via username/password combination

INPUTS:
- username: string, 3-50 characters, alphanumeric + underscore
- password: string, 8-128 characters, any UTF-8

OUTPUTS:
Success: 
- HTTP 200
- JSON: {"token": "string", "expires_at": "ISO8601 timestamp"}
- Token valid for 24 hours

Failure:
- HTTP 401: Invalid credentials
- HTTP 429: Too many attempts (>5 in 5 minutes)
- HTTP 400: Malformed request

CONSTRAINTS:
- Response time < 200ms for 95th percentile
- Bcrypt or stronger for password hashing
- Constant-time comparison for credentials

SUCCESS CRITERIA:
1. Valid credentials return token within 200ms
2. Invalid credentials return 401 within 200ms
3. 6th attempt within 5 minutes returns 429
4. Token expires exactly 24 hours after creation
5. Malformed JSON returns 400
6. Empty username or password returns 401
7. SQL injection attempts return 401 (not 500)

EDGE CASES:
- Unicode passwords handled correctly
- Username case-insensitive
- Leading/trailing spaces in username trimmed
- Password spaces preserved
```

**Why it's good:**
- Every behavior is explicitly defined
- Success can be tested automatically
- Multiple implementations would behave identically
- No ambiguity in requirements

## Common Pitfalls

1. **Using implementation details**: "Store in MySQL" vs "Persist data"
2. **Vague requirements**: "Should be user-friendly" vs "Complete in ≤3 clicks"
3. **Missing error cases**: Not specifying what happens when things go wrong
4. **Implicit assumptions**: Assuming behaviors that aren't written
5. **Untestable criteria**: "Should feel fast" vs "Response time <100ms"

## Checklist for a Complete Specification

- [ ] Can someone unfamiliar with the project understand what needs to be built?
- [ ] Are all inputs and their valid ranges defined?
- [ ] Are all outputs and their formats defined?
- [ ] Is every error condition handled?
- [ ] Can each success criterion be tested?
- [ ] Would two different implementations produce the same results?
- [ ] Are edge cases explicitly addressed?