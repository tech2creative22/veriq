# Veriq Demonstration Data Notice

## What may be uploaded

This Development-track MVP is for fictional or synthetic school data only. Do not upload real learner names, IDs, contact details, health information, disciplinary records, assessment records or any information that can identify a real person.

The included Zimbabwe secondary-school judge dataset is fictional. First names, learner IDs and school scenarios were created for product validation and do not represent real people or official ZIMSEC outcomes.

## Operator acknowledgement

Before analysis, the operator must confirm that:

1. they are authorised to use the files; and
2. demonstration files contain fictional or synthetic learner data only.

The frontend prevents submission without this acknowledgement, and the backend independently rejects unacknowledged imports. This control records intent at the point of use but is not a substitute for consent, a lawful basis, a privacy notice or a Data Processing Agreement.

## What the MVP does with the files

- It validates three CSV files and stores the import in a local SQLite database.
- It calculates attendance, behaviour and internal-assessment indicators deterministically.
- Beacon may send a bounded summary of verified evidence to the configured Gemini API to explain a pattern. Raw CSV files are not sent directly to Gemini by the application workflow.
- Local data remains on the machine until the local database is deleted. This is a development behaviour, not an approved production retention policy.

## What Beacon output means

Beacon output is advisory. It may contain errors or omit context. A school leader must verify source data and use professional judgement. Veriq must not be used to make an automatic disciplinary, grading, progression or other significant decision about a learner.

## Real-data pilot status

Real learner data is prohibited until the pre-pilot controls in `COMPLIANCE_AND_DATA_GOVERNANCE.md` are approved and implemented.
