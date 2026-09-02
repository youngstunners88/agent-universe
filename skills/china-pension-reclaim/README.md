# China Pension Reclaim

Recover the social-insurance money left behind in China after a foreign worker stops working there.

The employee's **8% pension contribution** sits in a personal account under their own name. It is
refundable as a lump sum, from anywhere in the world, with **no claim deadline**, and it accrues
interest in the meantime. The employer's 16% goes to the city pooling fund and is not recoverable.
Most former expat workers never find out the account exists.

## Contents

| Path | What it is |
|---|---|
| `SKILL.md` | The agent skill — intake order, failure modes, document requirements |
| `references/jurisdictions.md` | Enrolment start dates, contribution bases, treaty countries, counter practice |
| `assets/reclaim-app.html` | The claim kit — balance estimator, bilingual call script, auto-filled power of attorney |

## The claim kit

`assets/reclaim-app.html` is a self-contained page, publishable as an artifact. It:

- estimates the recoverable balance month by month against each period's official contribution
  floor and ceiling, and shows the employer's non-recoverable 16% alongside so the split is honest;
- flags the enrolment gap — most importantly, that **Shanghai only made social insurance compulsory
  for foreigners on 16 August 2021**;
- shows whether the 12333 and 12345 hotlines are open right now in Shanghai time;
- gives a line-by-line bilingual phone script, opening with the request for an English desk;
- generates a bilingual 授权委托书 (power of attorney) and 情况说明 (statement of circumstances
  for a dissolved employer), filled from the intake;
- tracks progress through the four filing steps, persisted in the browser.

Nothing leaves the browser.
