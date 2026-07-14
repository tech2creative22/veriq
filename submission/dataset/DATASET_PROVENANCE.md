# Dataset Provenance and Synthetic Validation Statement

**Dataset:** Veriq Zimbabwe Secondary Judge Dataset  
**Version:** 1.0.0  
**Validation date:** 14 July 2026  
**Intended use:** AI4I Development-track demonstration and testing only

## Provenance and rights

Every learner, identifier, event and score in this dataset is fictional and programmatically generated. No record was copied from a school, EMIS, examination body or real learner. `Prince High` is used only as a fictional scenario label. The Veriq project team owns the generated dataset and may submit it with the MVP.

Only first names are included to keep the judge narrative readable. The names are common fictional examples and must not be interpreted as identifying real people. Student IDs encode only the fictional school, Form and row sequence.

## Zimbabwe secondary-school alignment

The dataset models four classes named Form 1A through Form 4A and uses five Ordinary Level-aligned subject labels: Mathematics, English Language, Combined Science, Heritage Studies and Shona Language. ZIMSEC publishes these as Ordinary Level subjects or papers. Sources:

- https://www5.zimsec.co.zw/download-category/o-level/page/11/
- https://www5.zimsec.co.zw/examinations-administration/

ZIMSEC reports Ordinary Level pass-rate context using candidates who obtain Grade C or better in five or more subjects. Veriq's values are internal continuous-assessment percentages only; they are not ZIMSEC grades and cannot establish an official pass rate. Source:

- https://www5.zimsec.co.zw/2026/02/06/release-of-2025-ordinary-level-results/

## Files and schema

### `attendance.csv`

| Field | Type | Rule |
|---|---|---|
| `student_id` | text | Required fictional stable learner ID. |
| `first_name` | text | Optional to the API, included for judge readability. |
| `class_name` | text | Required; one of Form 1A-Form 4A. |
| `date` | ISO date | Required `YYYY-MM-DD`. |
| `status` | category | Required; `present`, `absent`, `late` or `excused`. |

### `behaviour.csv`

| Field | Type | Rule |
|---|---|---|
| `student_id` | text | Required fictional stable learner ID. |
| `first_name` | text | Included for judge readability. |
| `class_name` | text | Required and shared with the other files. |
| `date` | ISO date | Required `YYYY-MM-DD`. |
| `incident_type` | text | Required contextual incident label. |
| `severity` | category | Required; `low`, `medium` or `high`. |

### `assessments.csv`

| Field | Type | Rule |
|---|---|---|
| `student_id` | text | Required fictional stable learner ID. |
| `first_name` | text | Included for judge readability. |
| `class_name` | text | Required and shared with the other files. |
| `subject` | text | Required internal assessment subject. |
| `date` | ISO date | Required `YYYY-MM-DD`. |
| `score` | number | Required internal percentage from 0 to 100. |

## Deterministic generation method

Run from the repository root:

```powershell
node scripts/generate_judge_dataset.mjs
python scripts/validate_judge_dataset.py
```

The generator contains no random-number calls and produces byte-stable CSV files. It defines 20 fictional learners, two ten-day attendance periods, period-specific incidents, five subjects and four internal assessment dates. SHA-256 hashes in `dataset_manifest.json` and the validation report prove which bytes were tested.

The validator imports the CSV bytes through the same `backend/app/services/imports.py` evidence path used by the live API. It therefore tests both dataset integrity and the actual MVP interpretation.

## Designed scenarios

| Scenario | Learners | Intended evidence |
|---|---|---|
| Connected high attention | Chipo, Tendai, Nyasha | Attendance decline, behaviour increase and internal assessment decline occur together. |
| Single-signal watch | Tapiwa | Attendance decline without behaviour or assessment decline. |
| Single-signal watch | Tanaka | Internal assessment decline without attendance or behaviour deterioration. |
| Stable controls | 15 other learners | Stable or improving indicators prevent a dataset containing only negative cases. |

These are scenario labels, not learned ground-truth diagnoses. They test whether Veriq detects intended evidence patterns without claiming that a learner will fail or that an intervention is automatically required.

## Validation result

The committed validation report proves:

- 20 unique learners across four shared classes.
- 400 attendance, 34 behaviour and 400 assessment records.
- Five expected subjects and valid domain values.
- No duplicate attendance, behaviour or assessment composite keys.
- All scores are within 0-100.
- Exactly three connected high-attention learners, two single-signal watch learners and fifteen stable controls.
- No official grade, pass-rate or final-result fields.

Machine-readable evidence: `submission/dataset/SYNTHETIC_VALIDATION_RESULTS.json`.

The accompanying workbook was imported with the submission spreadsheet runtime, all four sheets were rendered for visual review, the Demo Guide counts reconciled to the CSV files and the formula-error scan returned zero matches.

## Limitations

- Twenty learners and four classes are deliberately small for a reliable live demonstration.
- Patterns are constructed and should not be used to estimate real prevalence, fairness or intervention effectiveness.
- The dataset does not include disability, socioeconomic, health or protected-attribute data.
- Behaviour events are simplified and do not contain narrative context or adjudication outcomes.
- Internal scores do not model ZIMSEC grading, subject entry rules or examination uncertainty.
- Model accuracy on this dataset does not constitute production validation on real schools.

Real-school piloting requires lawful authority, school data agreements, de-identification, access controls, retention limits, bias review and separate validation with representative data.
