MINOR

**`java-spring` answers the state-stored rung: `--write-model state` generates a service on a versioned
repository, over memory, SQLite or Postgres.** `write_side_files` gains a `state` block built from the family's
shared rows, this framework's `config/DatabaseUrlEnvironmentPostProcessor` wiring for `DATABASE_URL`, its
transport and identity rows as they are, and `PostgresRepositoryIT`: the shared contract on the application's
Hikari pool under `@SpringBootTest`, plus two independent pools racing one insert and one same-version update with
exactly one winner each. A state service has no projections and no checkpoint, so the read side answers nothing
for the rung. `language.json` offers the axis as `persistence`, its name in the core, and offers `write-model`
`events` and `state`; it now requires `java` >=1.1, which carries the shared rows.

**Catch-up:** `slipwai language upgrade java-spring` beside `slipwai language upgrade java`. An event-sourced
service is generated as before.
