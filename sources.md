# Sources

Research used to build this crash course, in roughly the order consulted.
Note: several of these are secondary/blog write-ups summarizing TypeSafe's
own docs and announcement — where this course states something as verified
fact (API shapes, pricing, response formats), it's because it was tested
directly against the live API on 2026-09-21, not just quoted from a source.

- [What is Jev AI? — Data Science in Your Pocket (Medium)](https://medium.com/data-science-in-your-pocket/what-is-jev-ai-b8294d980001)
- [Jev by TypeSafe: A Decision Model for AI Agents — Beam AI](https://beam.ai/agentic-insights/jev-typesafe-ai-agents)
- [What Is Jev? A Guide to TypeSafe AI's System One Model — LangChain Blog](https://www.langchain.com/blog/building-a-harness-with-jev)
- [Jev AI Review: Decision Models for Agent Workflows — Wavect](https://wavect.io/blog/jev-ai-decision-model-review/)
- [Where does Jev fit in an AI agent loop? — Vercel](https://vercel.com/i/jev-agent-control)
- [awesome-jev (yibie) — GitHub](https://github.com/yibie/awesome-jev)
- [awesome-jev (fatwang2) — GitHub](https://github.com/fatwang2/awesome-jev)
- [Open-Jev — GitHub](https://github.com/Zefan-Cai/Open-Jev)
- [System One — TypeSafe AI Docs](https://docs.typesafe.ai/concepts/system-one)
- [What Is Jev? TypeSafe AI's System One Model Explained — You.com](https://you.com/resources/what-is-jev)
- [A deep dive into Jev, TypeSafe's System One model — Flavio Copes](https://flaviocopes.com/jev/)
- [How to Use Jev: A practical guide — DEV Community](https://dev.to/valyuai/how-to-use-jev-a-practical-guide-to-typesafes-system-one-model-g5e)
- [TypeSafe AI's Jev offers an alternative to LLMs — Tom's Hardware](https://www.tomshardware.com/tech-industry/artificial-intelligence/typesafe-ais-jev-offers-an-alternative-to-llms-that-claims-to-be-193x-faster-and-445x-cheaper-system-one-type-model-is-bespoke-for-probabilistic-decision-making)
- [TypeSafe AI Home](https://typesafe.ai/)
- [Introducing System One Models & Jev — TypeSafe AI Blog](https://typesafe.ai/blog/introducing-system-one-models-and-jev)
- [Jev API — jevapi.org](https://jevapi.org/)
- [TypeSafe exits stealth with $40M seed — Dealroom News](https://dealroom.co/news/151032-typesafe-exits-stealth-with-40m-seed-to-build-ai-for-software-not-people/)
- [TypeSafe AI Emerges From Stealth With $40M — Yahoo Finance](https://finance.yahoo.com/technology/ai/articles/typesafe-ai-emerges-stealth-40m-190000776.html)
- [TypeSafe AI Emerges From Stealth With $40M — AIwire/HPCwire](https://www.hpcwire.com/aiwire/2026/09/16/typesafe-ai-emerges-from-stealth-with-40m-in-funding-with-new-model-for-composable-ai/)
- [TypeSafe raises $40M for Jev, its AI model built to skip chat — Runtimewire](https://runtimewire.com/article/diogo-almeida-typesafe-jev-40m-seed-pong)
- [TypeSafe AI Raises $40 Million for Jev, but Its 445x Cost Claim Is Still Self-Tested — TS2.tech](https://ts2.tech/en/typesafe-ai-raises-40-million-for-jev-but-its-445x-cost-claim-is-still-self-tested/)
- [TypeSafe AI, an AI startup founded by ChatGPT co-inventor... — TechStartups](https://techstartups.com/2026/09/16/typesafe-ai-an-ai-startup-founded-by-chatgpt-co-inventor-emerges-from-stealth-with-40m-to-build-ai-thats-100x-faster-and-cheaper/)

## Verified directly against the live API (2026-09-21)

- `POST https://api.typesafe.ai/v1/systemone` request/response shapes for
  all three question types (`noul`, `choice`, `score`), including the
  `score.criteria` must-be-a-list requirement (several secondary sources
  show this incorrectly as a dict).
- Real round-trip latency figures shown in `examples/05_raw_jev_call.py` and
  `examples/06_llm_vs_jev_timing.py` output.
