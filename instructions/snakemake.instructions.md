---
name: Snakemake workflow authoring
description: Stable guidance for authoring and validating Snakemake workflow sources.
applyTo: "**/Snakefile,**/snakefile,**/*.smk"
---

# Snakemake Workflow Authoring

These instructions apply to Snakemake workflow sources only: `Snakefile`, `snakefile`, and
`*.smk` files. They do not apply to generic YAML or unrelated Python files.

## Establish the Workflow Context

- Inspect the workflow's declared and installed Snakemake versions before relying on syntax,
  built-in behavior, or plugin interfaces. Check the project's environment/lock files and CI
  configuration as well as `snakemake --version` in the environment intended to run the workflow.
- The documentation and plugin catalog evolve. For uncertain or version-sensitive behavior,
  consult the official documentation for the target version and the current plugin catalog;
  do not infer support from remembered syntax.

## Rules, DAGs, and Wildcards

- Design from the requested targets: each rule should declare the files it consumes and produces,
  so dependencies and the resulting DAG are explicit and inspectable.
- Keep rule inputs, outputs, parameters, logs, benchmarks, threads, and resources clear. Use
  wildcards only where a rule genuinely represents multiple related jobs; constrain them when
  needed to prevent ambiguous matches or accidental capture of unrelated files.
- Keep shell commands and helper logic deterministic and understandable. Avoid hidden file
  discovery, implicit dependencies, and mutable global state that make the DAG difficult to
  reason about or reproduce.
- Make the intended targets and configuration discoverable. Split a large workflow into focused
  modules or included files when that improves navigation, without fragmenting simple workflows.

## Configuration and Reproducibility

- Put changeable data paths, sample sets, and analysis choices in declarative configuration
  rather than embedding them in rules.
- Validate configuration against a schema when the project supports one. Give required fields,
  types, and allowed values meaningful constraints and fail early on invalid input.
- Declare software environments with workflow rules where appropriate. Pin or constrain relevant
  software versions and keep environment definitions under version control so jobs can be
  reproduced.
- Reuse maintained Snakemake wrappers or modules when they fit the task and target version;
  check their documented inputs, outputs, and compatibility before adopting them.

## Resources and Execution

- Declare realistic per-rule threads and resource requirements. Avoid assuming that a local
  machine's capacity or scheduler configuration is universal.
- Keep execution-specific settings in the project's profiles or executor configuration where
  appropriate, separating workflow logic from site- or cloud-specific policy.
- Check the target Snakemake version's official CLI and executor documentation before changing
  profile, executor, or plugin configuration.

## Validation

- Validate changes at the smallest useful scope. Use a dry-run to check job selection and missing
  inputs, and inspect the DAG when dependencies or targets change.
- Run the version-appropriate Snakemake linter and formatter when available. Resolve or explain
  relevant findings rather than assuming a clean parse proves workflow quality.
- Add or update a small, representative test fixture for meaningful workflow behavior where
  practical; validate its expected outputs or invariants without requiring a production dataset.
- A full workflow run may be costly or require external resources; assess scope and obtain
  confirmation before expensive execution.
- TDD is context-dependent: use it when the change benefits from a test-first loop, but it is not
  a mandatory workflow-authoring rule.

## Official References

- [Rules](https://snakemake.readthedocs.io/en/stable/snakefiles/rules.html)
- [Configuration](https://snakemake.readthedocs.io/en/stable/snakefiles/configuration.html)
- [CLI and profiles](https://snakemake.readthedocs.io/en/stable/executing/cli.html)
- [Executors](https://snakemake.readthedocs.io/en/stable/executing/executors.html)
- [Best practices](https://snakemake.readthedocs.io/en/stable/snakefiles/best_practices.html)
- [Deployment](https://snakemake.readthedocs.io/en/stable/snakefiles/deployment.html)
- [Plugin catalog](https://snakemake.github.io/snakemake-plugin-catalog/)
