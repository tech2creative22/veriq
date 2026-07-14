# Veriq Cost and Pricing Model

**Currency:** USD  
**Model date:** 14 July 2026  
**Status:** planning assumptions for judge review; replace with CCE allocation and supplier quotations before contracting.

## AI cost assumption

The current configured model is Gemini 3.5 Flash. The official Gemini pricing page lists paid-tier rates of USD 1.50 per million input tokens and USD 9.00 per million output/thinking tokens for the relevant standard context tier at the time of review. Pricing can change and must be refreshed before deployment: [Google Gemini API pricing](https://ai.google.dev/gemini-api/docs/pricing).

Planning request size:

- 2,000 input tokens: `2,000 / 1,000,000 x $1.50 = $0.0030`
- 500 output/thinking tokens: `500 / 1,000,000 x $9.00 = $0.0045`
- Planned cost per Beacon interaction: **$0.0075**

| Beacon use | Estimated monthly model cost per school | Annual |
|---:|---:|---:|
| 300 interactions/month | $2.25 | $27.00 |
| 500 interactions/month | $3.75 | $45.00 |
| 1,000 interactions/month | $7.50 | $90.00 |

This is a token-budget calculation, not a measured invoice. Actual prompt caching, output length, retries, taxes, exchange and provider changes can alter cost. Usage caps and cost alerts are required.

## School Core unit economics hypothesis

Assume 10 properly isolated schools share managed application infrastructure and each uses 500 Beacon interactions/month.

| Annual cost per school | Assumption | Amount |
|---|---|---:|
| Gemini | 500 interactions/month at $0.0075 | $45 |
| Hosting allocation | $30/month shared by 10 schools | $36 |
| Monitoring/backups allocation | Shared service allowance | $12 |
| Onboarding/support labour | 8 hours/year at $10/hour | $80 |
| **Estimated variable/allocated cost** |  | **$173** |
| Proposed annual price | School Core hypothesis | **$300** |
| **Contribution before central overhead/tax** |  | **$127 (42%)** |

At 1,000 interactions/month, the contribution falls by $45 to $82 (27%) unless price, usage or support changes. A fair-use cap and transparent overage/upgrade policy are therefore necessary.

## Minimum 12-month cash planning envelope

This scenario ramps from a synthetic demo to 1-3 validation schools and up to 10 paid-equivalent schools. It is not a funding quote.

| Cost category | Planning assumption | 12-month amount |
|---|---|---:|
| Application hosting | Average $50/month while usage grows | $600 |
| Gemini usage | Ramp within 500-request planning allowance | $300 |
| Monitoring and backups | $20/month | $240 |
| Domain, email and operational tools | Allowance | $100 |
| Onboarding and first-line support | 120 hours at $10/hour | $1,200 |
| **Known planning subtotal** |  | **$2,440** |
| Legal, POTRAZ, security testing and insurance | Obtain Zimbabwe-specific quotations | **TBD / excluded** |
| Product development salaries and hardware | Founder/investment decision | **TBD / excluded** |

Ten School Core licences would produce $3,000 annual revenue, leaving $560 before the excluded compliance, tax, development and contingency costs. That is not yet a durable company margin; either more schools, a higher validated price, lower support cost, sponsorship or authority-level procurement is required.

## Cost controls

- Keep all metrics deterministic and call Gemini only when a user requests explanation or a brief.
- Limit question length, response schema and output size.
- Add per-school monthly quotas, alerts and an explicit provider-failure state.
- Cache only where privacy, freshness and analysis identity are preserved.
- Recalculate costs from actual token and support logs after every pilot month.
- Do not use a larger model unless measured quality gain justifies the cost.

## CCE and edge position

Veriq is a browser/cloud decision-support product, so on-device edge inference is not required for the current use case. CCE can host the Next.js, FastAPI and persistence components; Gemini still requires outbound internet. A future local/open-weight model could reduce external dependency but would add GPU/RAM, model-operations and evaluation costs and is not presented as implemented.
