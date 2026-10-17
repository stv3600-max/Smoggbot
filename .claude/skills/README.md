# Installed skills

Third-party Claude skills vendored into this repo. Each subdirectory is a copy of
an upstream GitHub repo at the commit noted below.

| Skill | Upstream | Commit | License |
|---|---|---|---|
| `resume-tailoring` | https://github.com/amanattar/resume-tailoring-skill | `998ee7e` (2026-03-18) | MIT |
| `job-description-skill` | https://github.com/yanliudesign/job-description-skill | `ae4c050` (2026-07-23) | none stated upstream |

Installed 2026-10-17.

## Notes

- `job-description-skill`: the upstream `docs/` directory (34 MB of demo videos and
  GIFs) was not copied — it is documentation media, not used at runtime.
- `job-description-skill` writes its HTML report to `~/Desktop/Claude skills/` and
  opens it with `open`; that path and command assume macOS.
- `resume-tailoring`: upstream ships only `SKILL.md`, but that file points to
  `research-prompts.md`, `matching-strategies.md`, `branching-questions.md` and
  `multi-job-workflow.md`, which do not exist in the upstream repo.

To update either skill, re-clone the upstream repo and copy the files over.
