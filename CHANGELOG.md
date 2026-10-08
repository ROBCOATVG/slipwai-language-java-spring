# Changelog

No releases yet. Release notes are recorded here newest first, one entry per released version; the entry being
written is `changelog.d/`.

## 1.0.0

**The Spring Boot backend is now a framework package of the `java` family.** The `java-spring` backend that was
built into slipwai — its pom and properties, `ServiceApplication` and its walking skeleton, its Spring adapters
(the datasource's address, Actuator's probe, the 404 handler, Spring Security's resource server and group mapping,
the scheduler, transactions), its own Keycloak paragraph and its working PIT target — lives here, with the history
it had there. Everything Java shares comes from the `java` package, which this one requires
(`requires: {"java": ">=1.0,<2"}`); without it, or with a `java` outside that range, slipwai refuses this package
alone. The projects it generates are byte for byte those slipwai generated with Java built in. It declares the
catalog schema it loads on, `core >=9.0,<10`.

