# Veriq Licence and Asset Register

**Review date:** 14 July 2026  
**Purpose:** identify distribution rights and unresolved release decisions before repository publication or commercial use.

## Project-owned assets

| Asset | Origin/owner | Current permission | Release action |
|---|---|---|---|
| Veriq application source, prompts and documentation | Copyright 2026 Praisegod Chaparika and Veriq contributors; team contribution ownership still requires internal confirmation. | Challenge Evaluation Licence: authorised challenge inspection/execution only; all other rights reserved. | Keep `LICENSE` with every review copy and obtain written IP assignments before commercial contracting. |
| Veriq name, wordmark and SVG mark | Project-created UI asset. Trademark ownership/search not completed. | Challenge demonstration. | Confirm owner and conduct name/trademark review before commercial launch. |
| Inline interface icons | Project-authored SVG path components in `components/app-icons.tsx`. | Included with application source. | Confirm authorship in team IP assignment. |
| UI styling and layouts | Project-created CSS/React implementation. | Challenge demonstration. | Retain design-source evidence and team IP assignment. |
| Judge CSVs and workbook | Deterministically generated fictional dataset. | Project may reproduce and submit for evaluation; see dataset provenance. | Publish only with the synthetic-data notice and generator. |
| Screenshots/proposal/demo video | To be produced from the project. | Challenge submission. | Check that no real learner data, private key or unlicensed media appears. |

The UI requests `Inter` first but ships no font file and makes no external font request; it falls back to system UI fonts. If a font is bundled later, its licence file must be added here.

## Runtime and development dependencies

Versions below follow the committed direct manifests/lockfile or, where labelled, the current tested environment. Licence files in the distributed packages remain authoritative.

| Component | Version | Licence | Use |
|---|---:|---|---|
| Next.js | 15.5.20 | MIT | Frontend framework |
| React / React DOM | 18.3.1 | MIT | UI runtime |
| TypeScript | 5.7.2 | Apache-2.0 | Build/development |
| ESLint | 8.57.1 | MIT | Development linting |
| eslint-config-next | 15.5.20 | MIT | Development lint rules |
| FastAPI | 0.115.6 | MIT (project licence; verify packaged notice) | API framework |
| Pydantic | 2.12.5 in tested environment (transitive) | MIT | Validation and response schemas |
| Uvicorn | 0.34.0 | BSD-3-Clause | ASGI server |
| Google Gen AI Python SDK | 2.11.0 | Apache-2.0 | Gemini API client |
| HTTPX | 0.28.1 | BSD-3-Clause | HTTP client dependency |
| python-multipart | 0.0.20 | Apache-2.0 | CSV multipart uploads |
| python-dotenv | 1.1.1 | BSD-3-Clause | Local environment loading |

Transitive dependencies must be captured in a generated SBOM or lockfile-derived notice before a public binary/container release. Open-source licences govern the libraries; they do not grant rights to the Veriq name, project code or data.

## External services and terms

| Service | Governing material | Current use / action |
|---|---|---|
| Google Gemini API | Google API/service terms, data-use terms and [Gemini pricing](https://ai.google.dev/gemini-api/docs/pricing) | Server-side grounded explanations. Confirm organisation account, retention/data-use configuration, subprocessor and cross-border position before a real-data pilot. |
| ZCHPC CCE | Challenge allocation and CCE acceptable-use/service conditions | Target deployment environment. Obtain account, quotas, ingress, backup and support conditions. |
| Zimbabwe legal/regulatory materials | Public official/legal sources cited for analysis | May be linked/quoted within applicable limits; do not imply POTRAZ or ZIMSEC endorsement. |

## Release blockers

1. Every team member/contractor must confirm IP assignment or permission for contributed assets.
2. Generate a dependency/SBOM notice from the final release images.
3. Record Gemini and CCE terms accepted by the responsible organisation.
4. Review the final proposal, screenshots and demo video for real personal data and third-party media.
5. Review the custom Challenge Evaluation Licence with qualified counsel before commercial contracting.
