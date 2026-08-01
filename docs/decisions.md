# Decision log

Use this log for small durable decisions. Use an ADR for choices that substantially affect architecture or future work.

| Date | Decision | Reason |
| --- | --- | --- |
| 2026-08-01 | Build a web app instead of continuing the Discord bot. | The game requires visual, mobile-friendly habit and collection interfaces. |
| 2026-08-01 | Use FastAPI and React with TypeScript. | Python remains the backend language while React provides a rich, responsive client. |
| 2026-08-01 | Start with a fishing vertical slice before habits and items. | It validates authentication, persistence, daily state, API boundaries, and the core collection loop. |
