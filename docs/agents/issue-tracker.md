# Issue Tracker

This project uses a **Local Markdown** issue tracker.

## Workflow

- Issues are stored as markdown files within the `.scratch/` directory.
- Each major feature or epic should have its own subdirectory: `.scratch/<feature-name>/`.
- Individual issues within a feature are represented by separate `.md` files.

## Usage for Agents

When creating or managing issues:
- Use the `create_issue` or similar logic to write files to the appropriate `.scratch/` path.
- Update existing issue files to reflect progress or state changes.
- Ensure file names are descriptive and easy to reference.
