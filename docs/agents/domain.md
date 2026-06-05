# Domain Docs

This project follows a **Multi-context** documentation layout.

## Layout Structure

- **Root level**: A `CONTEXT-MAP.md` file exists at the repository root. This file serves as the central registry, mapping specific areas of the codebase to their respective context files.
- **Context files**: Individual `CONTEXT.md` files are located within specific subdirectories (e.g., `backend/CONTEXT.md`, `frontend/CONTEXT.md`). These files contain the domain-specific language, business logic, and core concepts for that area.
- **Architectural Decisions**: Past decisions are recorded in `docs/adr/` (or per-context `adr/` directories) to provide historical context for architectural choices.

## Usage for Agents

When using skills like `improve-codebase-architecture`, `diagnose`, or `tdd`:

1. **Consult the Map**: Always check `CONTEXT-MAP.md` first to determine which context files are relevant to the current task.
2. **Load Relevant Context**: Read the specific `CONTEXT.md` files identified by the map to ensure you are using the correct domain terminology and understand the local constraints.
3. **Trace ADRs**: Reference the ADRs to avoid re-introducing architectural patterns that have already been intentionally superseded.
