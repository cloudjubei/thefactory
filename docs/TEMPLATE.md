# Specification Template

Use this template to author new specifications. See docs/SPECIFICATION_GUIDE.md for detailed guidance.

## 1. Problem Statement
Describe the problem the specification addresses in one or two paragraphs.
Example:
Authenticate users to access a protected API using username/password.

## 2. Inputs and Outputs
Inputs:
- input_name: type, constraints
- ...

Outputs:
- Success: format and fields
- Failure: error codes and messages
Example:
Inputs:
- username: string, 3-50 chars, alphanumeric + underscore
- password: string, 8-128 chars
Outputs:
- 200: {"token": "string", "expires_at": "ISO8601"}
- 401: Invalid credentials

## 3. Constraints
List hard constraints (performance, resources, compatibility).
Example:
- 95th percentile response time < 200ms
- Bcrypt or stronger hashing

## 4. Success Criteria
Measurable, testable conditions for completion.
Example:
1) Valid credentials return token within 200ms
2) Invalid credentials return 401
3) 6th attempt within 5 minutes returns 429

## 5. Edge Cases
Explicitly list edge cases and expected handling.
Example:
- Unicode passwords handled correctly
- Username case-insensitive

## 6. Glossary [Optional]
Define domain-specific terms if needed.

## 7. Dependencies [Optional]
List related specs or systems this depends on.

## 8. Revision History [Optional]
- v1.0: Initial version
- v1.1: Updated constraints
