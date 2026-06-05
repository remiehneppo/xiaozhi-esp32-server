# Triage Labels

The `triage` skill uses the following label vocabulary to manage the lifecycle of issues.

## Canonical Roles

- `needs-triage`: The issue has been created or updated and requires a maintainer's evaluation to define scope, priority, or next steps.
- `needs-info`: The issue is actionable but lacks sufficient information from the reporter to proceed.
- `ready-for-agent`: The issue is fully specified, contains all necessary context, and is ready for an automated agent to implement or investigate.
- `ready-for-human`: The issue is well-defined but requires manual human implementation or high-level decision-making.
- `wontfix`: The issue has been evaluated and will not be actioned (e.g., duplicate, out of scope, or intentional behavior).

## Usage

When processing or updating an issue, the `triage` skill will append or update these identifiers in the issue's metadata/frontmatter to reflect its current state.
