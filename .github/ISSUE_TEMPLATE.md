# GitHub Issue Template

## Summary
<!-- Brief, clear description of the issue/feature -->

## Type
<!-- One of: bug, enhancement, documentation, question -->

## Description
<!-- Detailed explanation of the issue or feature request -->

## Context
<!-- Why is this needed? What problem does it solve? -->

## Acceptance Criteria
<!-- What constitutes a successful implementation? -->
- [ ] 
- [ ] 
- [ ] 

## Technical Details
<!-- Implementation notes, technical requirements, or relevant code -->

## Resources
<!-- Links, references, or examples -->

## Environment
<!-- For bugs: OS, browser, version info. For features: target environment -->

## Priority
<!-- One of: low, medium, high, critical -->

## Labels
<!-- Suggested labels: bug, enhancement, documentation, good first issue, help wanted -->

## Additional Notes
<!-- Any other relevant information -->

---

## Template Variables for Automation
```
{{TITLE}}           - Issue title
{{TYPE}}            - Issue type (bug/enhancement/documentation/question)
{{DESCRIPTION}}     - Main description
{{CONTEXT}}         - Background/reasoning
{{ACCEPTANCE_CRITERIA}} - Success criteria as bullet points
{{TECHNICAL_DETAILS}}  - Implementation details
{{RESOURCES}}       - Links/references
{{ENVIRONMENT}}     - Environment details
{{PRIORITY}}        - Priority level
{{LABELS}}          - Comma-separated labels
{{ADDITIONAL_NOTES}} - Extra context
```

## Example Usage Patterns

### Bug Report Pattern
```markdown
# {{TITLE}}

## Summary
{{DESCRIPTION}}

## Type
bug

## Description
{{DESCRIPTION}}

## Steps to Reproduce
{{TECHNICAL_DETAILS}}

## Expected vs Actual Behavior
{{CONTEXT}}

## Environment
{{ENVIRONMENT}}

## Priority
{{PRIORITY}}

## Labels
bug, {{LABELS}}
```

### Feature Request Pattern
```markdown
# {{TITLE}}

## Summary
{{DESCRIPTION}}

## Type
enhancement

## Description
{{DESCRIPTION}}

## Use Case
{{CONTEXT}}

## Acceptance Criteria
{{ACCEPTANCE_CRITERIA}}

## Technical Approach
{{TECHNICAL_DETAILS}}

## Resources
{{RESOURCES}}

## Priority
{{PRIORITY}}

## Labels
enhancement, {{LABELS}}
```