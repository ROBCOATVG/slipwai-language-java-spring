# slipwai-language-java-spring

slipwai 2.0 language addon: slipwai-language-java-spring

The `java-spring` backend of the `java` family: Spring Boot owns the service's startup. It requires the
`slipwai-language-java` package beside it in the language directory.

## Write models

`--write-model events` and `--write-model state` are both answered, over `--persistence memory|sqlite|postgres`.
The state rung takes the family's repository port and adapters (see `slipwai-language-java`), this framework's
`DATABASE_URL` wiring and `PostgresRepositoryIT`, a `@SpringBootTest` that runs the shared contract on the
application's pool and races two independent pools for one row. Against a real database:

    make services-up migrate test-integration
