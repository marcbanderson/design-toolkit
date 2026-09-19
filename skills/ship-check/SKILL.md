---
name: ship-check
description: Verify that what Marc is looking at is actually the work that was done, before claiming anything shipped. Use before saying a change is live or done, when Marc says he is still seeing the old version, or when he asks whether a deployed site matches his branch.
---

# Ship check

The most repeated frustration in this working relationship is not a design
failure. It is a **verification failure**: the work was described as done while
Marc was looking at something that did not contain it.

> "You say you are making these changes but they are not appearing in playground"
>
> "The updates were pushed, and I am still seeing a number of issues"
>
> "I'm still seeing the old website"
>
> "8084 still shows the old homepage not the new one"
>
> "Were you just editing locally?"

Every one of these cost a round trip that a check would have prevented. Run this
before any claim that something is done, live, fixed or shipped.

## The four questions

**1. Which artifact is Marc looking at?**

Name it explicitly, by URL or port. There are usually several in play at once:
a local server, a static preview, a deployed staging site, production, and a
Figma prototype. They do not contain the same code and they never have.

If a preview was produced by injecting styles into a running page, say so and
say it was removed. A client-side injection is a way to *look* at a change, not
a way to make one. Never let it stand in for the edit.

**2. Does that artifact contain the change?**

Trace it the whole way. Committed is not pushed. Pushed is not merged. Merged is
not built. Built is not live: a deployment can be waiting on approval, and
approval is not yours to give.

Check the actual thing, do not infer it. For a deploy, confirm the service
reports the exact commit that was pushed. For a local server, confirm it is
serving the directory you edited, and not a sibling repo. That one is real: a
server running from a neighbouring checkout looked exactly like the app under
test and contained none of the work.

**3. Is anything cached between the work and his eyes?**

Static assets, service workers, CDN, phone browsers. *"on my phone the asset is
still wrong. is there a way to hard-reset it?"* If a hard reload is needed, say
so up front rather than letting him discover it.

**4. What did you not exercise?**

Say it plainly, and be specific about which paths. "Rendered and checked against
the stylesheet, but the DELETE round trip is unexercised because the app needs a
database and will not run locally" is useful. "Should be fine" is not.

## Reporting

State the environment, the evidence, and the gap:

```
Live on the production URL: yes. The service reports commit 8441278, which
is the merge of PR #3. Checked the deploy status, not just the merge.

Not verified: the removal flow. It needs a real backend, so the DELETE is
unexercised. One click on staging would close it.
```

## The standing rule

Never say done, live, or shipped without having checked. If you cannot check,
say what you could not check and why. Marc would far rather have an honest gap
named than discover it himself in a screenshot, because discovering it himself
costs him a round trip and costs the claim its credibility.
