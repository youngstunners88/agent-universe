---
name: china-pension-reclaim
description: Help someone recover the social-insurance money left behind in China after they stopped working there — estimate the personal-account balance, determine whether they were ever enrolled, and generate the bilingual power of attorney and statement of circumstances needed to claim it from abroad. Use when a former expat worker in China asks about pension refunds, social insurance withdrawal, 社保退费, claiming money after leaving China, or when an employer has dissolved and they have no termination letter.
---

# China Pension Reclaim

Former foreign workers in China routinely leave behind money that is still theirs. This
skill turns "I think there might be something" into a filed claim.

## The one fact that drives everything

Chinese pension contributions split into two buckets:

| Pot | Rate | Whose | Recoverable |
|---|---|---|---|
| Pension personal account 个人账户 | **8%** employee | Yours, by name | **Yes**, lump sum |
| Medical personal account 医保个人账户 | **2%** employee | Yours | **Yes**, but liquidated at a *different* office |
| Pension pooling fund 统筹账户 | 16% employer | The city's | No, ever |
| Housing fund 住房公积金 | ~7% + ~7% | **Both shares yours** | **Yes** — different institution again (12329) |

The housing fund is the one people miss and it is frequently the largest of the four. It was
voluntary for foreigners in Shanghai, so it must be checked, never assumed.

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
2. **Make them call — but set the expectation honestly.** 12333 will not read personal account
   data to an unverified caller, and 12345's English desk mostly opens a ticket. **A refusal to
   give a figure is not evidence that no account exists** — claimants read it that way and quit.
   What the call reliably delivers: whether a record exists, the **district branch** holding it,
   the document list, and the payout-account rule. Shanghai: **12345** daily 08:00–20:00 (ask
   for English immediately); **12333** weekdays; **12329** for the housing fund. From abroad,
   +86 21 prefix.
   For the balance itself, better route: register at **si.12333.gov.cn** or the 电子社保卡
   mini-programme in WeChat/Alipay (证件类型 → 外国护照) and screenshot the 参保缴费明细.
   Registration usually needs a Chinese mobile for the SMS code — often a job for the agent.
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

## The two questions that actually decide the case

Everything else is paperwork. Ask these first.

**1. Was an account ever opened?** See step 1 below. In Shanghai this turns on 16 Aug 2021.

**2. Can they still be paid?** The payout lands in RMB in a Chinese bank account **in the
claimant's own name** — never the agent's. Banks restrict foreigners' accounts when the
residence permit on file expires, so "I had one in 2022" is not "it works". Some branches will
pay an account named in a notarised power of attorney; the template must therefore carry a
payee clause. And a credit to a Chinese account is still not money in hand — repatriation
(UnionPay ATM limits, mobile banking that needs a live Chinese SIM, the USD 50k annual quota)
is its own step. **Have them test the card and the banking app before spending a cent on a
notary.** If neither works and the branch will not remit overseas, the claim may not be worth
starting.

## Dates: three of them, never one

Conflating these overstates the balance and, worse, produces a sworn statement that contradicts
the passport stamp — in a document that invites the branch to check 出入境记录.

- **Employment start** — when the job began.
- **Departure from China** — the last month physically working in-country on a valid permit.
  Social insurance attaches to employment *within* China, so this normally ends the contributing
  window.
- **Employment end** — may be months later if they stayed on the payroll remotely from abroad.
  Those remote months are almost certainly **not** contributing months.

Exception: some employers kept paying for remote staff. Verify against the record rather than
assuming either way.

## Blockers that stop a filing dead

- **Account status.** A termination cannot process while the record reads 正常参保. If the
  vanished employer never filed 减员, that must be fixed first.
- **Arrears (欠费).** Months declared but never paid block everything. The remedy is 欠费剔除
  against the company's deregistration record — not the claimant's own statement.
- **Blanks in a notarised document.** An apostilled instrument with fields completed after the
  seal is refused as 涂改. Never generate a power of attorney with the agent's name or the
  branch left blank.
- **A renewed passport.** The record is keyed to the passport number held at enrolment. Search
  the old number too; a nil result on the new one reads exactly like never having been enrolled.
- **A photocopied 社保卡.** The medical liquidation surrenders the *original* card. Courier it.

## Notarise once

The most expensive avoidable mistake is notarising the power of attorney alone, then learning
the counter wants more. One sitting, four documents: the power of attorney, certified copies of
the passport bio page **and the page bearing the last exit stamp**, the statement of
circumstances, and the Centre's own application form. Apostille as one set, translate as one set.

In South Africa the apostille comes from the Registrar of any High Court division **or** DIRCO
in Pretoria — the Registrar is usually faster.

## Two documents carry the claim

Generate both, pre-filled, using `assets/reclaim-app.html` or by writing them directly:

- **授权委托书 / Power of attorney** — removes the need to fly. Must be signed *in front of* a
  notary, never pre-signed, then apostilled, then translated into Chinese by an agency that
  applies its chop.
- **情况说明 / Statement of circumstances** — replaces the termination letter when the employer
  has dissolved. It asks the branch to verify against the company deregistration record, the
  expired work permit and the exit records — all of which the state already holds.

### Where the claimant lives changes nothing about the claim

The qualifying event is having left China and ended the employment — not residence in any
particular country. What their location *does* change is the authentication chain, the cost of
the phone call, and how realistic a trip to the counter is.

| Signing in | Notary | Apostille authority |
|---|---|---|
| South Africa | Any notary public | High Court Registrar, or DIRCO Pretoria |
| South Korea | A Korean notary (공증인) | **Ministry of Justice** — the competent authority for notarial acts, not Foreign Affairs |
| UK | Notary or solicitor | FCDO Legalisation Office |
| US | Notary public | Secretary of State **of the state where notarised** |
| Australia | Notary public | DFAT |

A claimant somewhere in East Asia is in a much stronger position than one in Europe or Africa:
same time zone as the hotlines, a cheap short flight to the counter, and — critically — going in
person removes the agent, the power of attorney, and the notarisation chain entirely, and lets
them reopen a frozen bank account. When the payout account is the blocker, always price a trip
against the paperwork before assuming remote filing is cheaper.

Watch for a false lead: several countries have social-security treaties with China, but those
cover a country's *own nationals*. A South African living in Seoul gets nothing from the
China–Korea agreement.

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
- **A flat salary is usually wrong.** Contributions are calculated on what the person earned at
  the time, so a career with annual raises needs a year-by-year figure, not an average. Using
  the final salary throughout overstates the balance.
- **Under-declared contribution bases** are common, so any estimate is a ceiling until the
  operator reads out the real figure. Note that while the *account balance* has no claim
  deadline, a complaint about under-declaration or non-enrolment generally expires two years
  from when the worker knew — long gone for most people. Claim what is in the account; do not
  build a plan around recovering what should have been there.
- **The 15-year threshold.** Fifteen years of contributions unlocks a monthly pension for life,
  payable abroad. Anyone at or near it should not withdraw — flag this before generating any
  termination paperwork.
- **Never let an agent be paid from the proceeds.** The money cannot legitimately reach their
  account. Anyone proposing to collect and forward is describing something the counter will not
  do. Flat fee, paid separately.

## Assets

- `assets/reclaim-app.html` — the claim kit: balance estimator using each period's official
  contribution floor and ceiling, live hotline-hours clock, bilingual call script, and both
  documents auto-filled from the intake. Publishable as an artifact; state persists locally.
- `references/jurisdictions.md` — enrolment start dates, contribution bases, treaty countries,
  and per-city counter practice.
- `scripts/optimize.py` — adversarial review pass over the claim kit on Claude Fable 5.1 via
  OpenRouter. Four reviewers with different incentives (counter caseworker, the claimant,
  compliance, product) read the artifact in parallel, then a synthesis pass dedupes and ranks
  by value recovered per unit of build effort. See `scripts/README.md`. Re-run it after any
  substantive change to the kit — most of what is in this skill came out of it.

## Tone

The person on the other end has usually written this money off. Lead with the number, then the
single next action — the phone call — and keep the paperwork out of sight until they know
whether there is anything to claim.
