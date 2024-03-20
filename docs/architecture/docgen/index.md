---
status: proposed
creation-date: "2024-02-08"
authors: [ "@pagekeystreaming" ]
coach: "n/a"
approvers: [ "@stephengrice" ]
---


# Documentation Generation

## Summary

The documentation generator takes a configuration file (`site.yaml`) as input and produces an HTML documentation site as output. It does this by reading the configuration file and replacing relevant fields in Sphinx configuration files. The generator copies these templates into a directory along with any files or folders in the directory and runs `make html` to generate the fully-rendered HTML static site.

```mermaid
flowchart TD
  %% Define nodes
  DocsMarkdown{"Docs (Markdown)"}
  SphinxSource{"Sphinx Source"}
  Config
  %% Define connections
  DocsMarkdown -->|Copy| SphinxSource
  Config -->|Parse, Inject jinja2| SphinxSource
  SphinxSource -->|Build| GeneratedHTML
```

## Motivation

We need a common documentation site generator for all of the PageKey projects that is easy to use and update.

### Goals

- Define how the sitegen works.

### Non-Goals

Out of scope:

- Anything else

## Proposal

Create a CLI. When you invoke the CLI, pass a directory. Every file in that directory is copied into an intermediate `build/sphinx` directory. The `site.yaml` file is parsed. Sphinx site templates are filled in using `jinja2`. Then, the site is generated using a system call to `make html`.

## Design and implementation details

You write code. It works.

## Alternative Solutions

Cry.

## Related Content

- Stream 1: https://www.youtube.com/watch?v=hsOAPyn1jjY
- Stream 2: https://www.youtube.com/watch?v=42bvMnXk88Q
- Stream 3: https://www.youtube.com/watch?v=nB_S41R9rx4
- Stream 4: https://www.youtube.com/watch?v=-1aUvXi-nYg
- Stream 5: https://www.youtube.com/watch?v=Sjxe_QyA2qE
- Stream 6: https://www.youtube.com/watch?v=IONxeVD4pJY
