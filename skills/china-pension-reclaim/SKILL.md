---
name: china-pension-reclaim
description: Help someone recover the social-insurance money left behind in China after they stopped working there — estimate the personal-account balance, determine whether they were ever enrolled, and generate the bilingual power of attorney and statement of circumstances needed to claim it from abroad. Use when a former expat worker in China asks about pension refunds, social insurance withdrawal, 社保退费, claiming money after leaving China, or when an employer has dissolved and they have no termination letter.
---

# China Pension Reclaim

Former foreign workers in China routinely leave behind money that is still theirs. This
skill turns "I think there might be something" into a filed claim.

## The one fact that drives everything

Chinese pension contributions split into two buckets:

| Bucket | Rate | Whose | Recoverable |
|---|---|---|---|
| Personal account 个人账户 | **8%** of the contribution base, from the employee | Yours, by name | **Yes**, as a lump sum |
| Pooling fund 统筹账户 | 16% of the base, from the employer | The city's | No, ever |

Plus a **medical personal account** (employee 2%) that liquidates separately.

The personal account **has no claim deadline** and **accrues interest**. A balance from 2015 is
still there. This is why "I left years ago" is never a reason not to try.

Legal basis: *Interim Measures for the Participation in Social Insurance of Foreigners Employed
in China* (MOHRSS Order No. 16, 2011), Art. 5 — a foreigner leaving China before statutory
pension age may either keep the account dormant for a future return, or terminate the
relationship on written application and take the personal-account balance as a lump sum.

## Run the intake in this order

Do not let the person spend money on notarisation before step 2 resolves.

1. **Establish the enrolment window, not the employment window.** These differ, and the gap is
   where most claims die. See `references/jurisdictions.md`. The critical case: **Shanghai only
   made social insurance compulsory for foreigners on 16 August 2021** — before that, employers
   could opt them out, and most did. An ESL teacher whose training centre closed in the July 2021
   双减 crackdown may have an enrolment window of a few months, or zero.
2. **Make them call before anything else.** The counter can look the person up on passport
   number alone and state the balance. One call replaces every guide. Shanghai: **12345** daily
   08:00–20:00 (routes to an English desk on request — say so immediately); **12333** weekdays
   for specialists. From abroad: +86 21 12333.
   Get four things: the balance, the **district branch** holding the file, their document list,
   and whether that branch will remit overseas.
3. **Check the treaty position.** Nationals of Germany, South Korea, Denmark, Canada, Finland,
   Switzerland, the Netherlands, Spain, Luxembourg, Japan, Serbia and Kyrgyzstan may have been
   lawfully exempt from pension contributions — so there may be no account. Everyone else,
   South Africa included, was compulsorily enrolled with no exemption available.
4. **Solve the agent problem.** Most cities process this at the counter only. The agent must
   present their **own PRC resident ID card** with the power of attorney — so a foreign friend
   still in-country cannot act. A Chinese friend or ex-colleague costs nothing; an agency
   charges ¥2,000–6,000.
5. **Build the document pack** (below), get it notarised and apostilled, courier the originals.
6. **File and wait** — statutory limit is 20 working days for review and result.

## Two documents carry the claim

Generate both, pre-filled, using `assets/reclaim-app.html` or by writing them directly:

- **授权委托书 / Power of attorney** — removes the need to fly. Must be signed *in front of* a
  notary, never pre-signed, then apostilled, then translated into Chinese by an agency that
  applies its chop.
- **情况说明 / Statement of circumstances** — replaces the termination letter when the employer
  has dissolved. It asks the branch to verify against the company deregistration record, the
  expired work permit and the exit records — all of which the state already holds.

### Apostille, not legalisation

China joined the Hague Apostille Convention on **7 November 2023**. Chinese embassies stopped
legalising documents on that date. A private document such as a power of attorney must still be
notarised first to become a public document, then receives an apostille from the issuing
country's competent authority (South Africa: **DIRCO Legalisation Section, Pretoria**).

## Failure modes to raise unprompted

- **The closed Chinese bank account.** The payout lands in RMB in an account in the claimant's
  *own* name — not the agent's. If theirs was closed, reopening it often requires them in person,
  which defeats the plan. Ask about overseas remittance on the very first call.
- **Withdrawal is one-way.** It zeroes the contribution history. If they might work in China
  again, leaving the account dormant may be worth more — only 15 years of contributions ever
  unlocks a monthly pension.
- **The housing fund is a separate institution.** 住房公积金 is not social insurance and is
  claimed elsewhere. Voluntary for foreigners in Shanghai, but where an employer paid it, it is
  frequently the larger sum. Always ask.
- **Under-declared contribution bases** are common, so any estimate is a ceiling until the
  operator reads out the real figure.

## Assets

- `assets/reclaim-app.html` — the claim kit: balance estimator using each period's official
  contribution floor and ceiling, live hotline-hours clock, bilingual call script, and both
  documents auto-filled from the intake. Publishable as an artifact; state persists locally.
- `references/jurisdictions.md` — enrolment start dates, contribution bases, treaty countries,
  and per-city counter practice.

## Tone

The person on the other end has usually written this money off. Lead with the number, then the
single next action — the phone call — and keep the paperwork out of sight until they know
whether there is anything to claim.
