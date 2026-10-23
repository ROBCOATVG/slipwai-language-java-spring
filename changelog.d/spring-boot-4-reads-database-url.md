PATCH

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
