# Changelog

No releases yet. Release notes are recorded here newest first, one entry per released version; the entry being
written is `changelog.d/`.

## 1.2.0 — MINOR

**`java-spring` services on the durable event store get the family's seed door.** The event rung's `postgres` row
takes `SEED_DOOR` from `java` and the pom's exec plugin gains a `seed` execution naming `SeedMain`, so `make
seed-<service> FILE=<json>` appends a slice's given events through the event-store port, at the stream's current
version, as the system actor `systems/seed-door` under one correlation id per run, with an identity hashed from
stream, type and canonical data so a re-run appends nothing. With no `DATABASE_URL` it says so and exits 2. Never
an HTTP route: the door is a process with the store's credentials. `language.json` now requires `java` >=1.2,
which carries the door.

**Catch-up:** `slipwai language upgrade java-spring` beside `slipwai language upgrade java`, then `slipwai
migrate`.

**A Spring service's datasource honours `DATABASE_URL`.** `DatabaseUrlEnvironmentPostProcessor` was registered in
`META-INF/spring/org.springframework.boot.env.EnvironmentPostProcessor.imports`, a file Spring Boot 4 never reads,
so the datasource always fell back to `localhost:5433` whatever `DATABASE_URL` said. It now implements Boot 4's
`org.springframework.boot.EnvironmentPostProcessor` and is registered under that key in
`META-INF/spring.factories`, the file Boot 4 loads post-processors from. Reaching the real database surfaced a
second fault: a SERIALIZABLE conditional append refused at commit arrived as Spring's `CannotAcquireLockException`
instead of the port's exception, so `appendIf` threw where it should have answered a condition conflict;
`SpringTransactions` now hands the driver's exception back in the port's shape.

**Catch-up:** `slipwai language upgrade java-spring`, then `slipwai migrate`; a service generated earlier gains
`spring.factories` and should delete `src/main/resources/META-INF/spring/`. Until then set
`SPRING_DATASOURCE_URL`, `SPRING_DATASOURCE_USERNAME` and `SPRING_DATASOURCE_PASSWORD` directly.

## 1.1.0 — MINOR

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

## 1.0.0

**The Spring Boot backend is now a framework package of the `java` family.** The `java-spring` backend that was
built into slipwai — its pom and properties, `ServiceApplication` and its walking skeleton, its Spring adapters
(the datasource's address, Actuator's probe, the 404 handler, Spring Security's resource server and group mapping,
the scheduler, transactions), its own Keycloak paragraph and its working PIT target — lives here, with the history
it had there. Everything Java shares comes from the `java` package, which this one requires
(`requires: {"java": ">=1.0,<2"}`); without it, or with a `java` outside that range, slipwai refuses this package
alone. The projects it generates are byte for byte those slipwai generated with Java built in. It declares the
catalog schema it loads on, `core >=9.0,<10`.

