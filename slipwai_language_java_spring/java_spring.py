"""The Java/Spring Boot backend: `apps/service`, its Maven build, and this project's own package name."""
from __future__ import annotations

from ... import registry as protocol
from ...assets import LANGUAGE_ROOT, asset_tree
from ...images import IMAGE, MAVEN
from ...probes import HEALTH_PATH
from ...selection import Selection
from ...services import App
from ..backing_services import backing_service_service_files
from ..flag_route import Resource, flag_resource
from ..flags import flag_reader
from .java import JAVA_PORTS, rename_java_sources, verify_script
from .java_toolchain import MAVEN as MVNW
from .java_toolchain import maven_dev_command, maven_native_commands


def service_files(event: bool, selection: Selection, target: str = "none") -> dict[str, str]:
    """What this backend puts in a service's directory, keyed relative to it.

    Nothing is decided here by the selection: the pom and `application.properties` carry a marked region
    per feature and are emitted whole, then cut down by the pruner — the same mechanism `docker-compose.yml`
    uses, and for the same reason. A feature's dependency block and its configuration have to disappear
    together, and a marker is the one spelling that survives a later `./init` too.

    There is deliberately no `event-port/` fallback tree. That exists for a backend whose event-store axis
    offers nothing yet; this one answers all three of its options, so the port arrives from
    `backing_service_service_files` with adapters behind it, and emitting both would define it twice.

    Two trees, not one, and the split is by who decides the file. `java/build/` is the *family's*: the
    Maven wrapper and the three analyser configurations are the same files whatever owns startup, so they
    are read by both Java backends rather than copied into each. `java-spring/app/` is this backend's: the
    pom, the properties, `ServiceApplication` and the walking skeleton, all of which name the framework.
    """
    files = asset_tree(LANGUAGE_ROOT / "java/build")
    files.update(asset_tree(LANGUAGE_ROOT / "java-spring/app"))
    files.update(backing_service_service_files(selection, "java-spring"))
    # The flag reader, from the family's tree for the reason every `../java/` source is: it names no
    # framework type. Only where there is somewhere to deploy — see `flags.py`.
    files.update(flag_reader(target, "java-spring"))
    # And the route that serves them to the browser app, which this framework discovers rather than
    # having registered. Absent without both a target and a transport. See `flag_route`.
    files.update(flag_resource(target, "java-spring", selection))
    return files


def name_service(project_name: str, service: App, files: dict[str, str]) -> dict[str, str]:
    """One service's files under this project's own package — the family's rename, see `java.py`."""
    return rename_java_sources(project_name, service, files)


def repository_files(
    project_name: str, files: dict[str, str], services: list[App], verify: str
) -> dict[str, str]:
    """`scripts/verify` above the services, and nothing else.

    There is no aggregator pom above them: each service is a Maven project of its own, and one pom that
    exists only to list them is a file to keep in step for nothing — `scripts/verify` and the Makefile are
    the loop. Compare `go.work`, which Go genuinely requires.
    """
    files[verify] = verify_script(services)
    return files


# Its sibling's twin, and the `../java/` sources are the point: the event port, all three store
# adapters, the URL parser, the migration entry point, the 400 body and the group mapping are the same
# files here, not copies of them. They name no framework type, so there is nothing for a second copy to
# say differently — and an event-log adapter kept in two places is one this factory could watch drift
# without noticing. What is genuinely this backend's is what touches Spring: how the datasource learns
# its address, what serves the probe, what answers a 404, how a validated token becomes authorities, and
# the two tests that need an application context.
WRITE_SIDE: dict[str, dict[str, str]] = {
    "memory": {
        f"{JAVA_PORTS}/events/Actor.java": "../java/actor.java",
        f"{JAVA_PORTS}/events/AppendResult.java": "../java/append_result.java",
        f"{JAVA_PORTS}/events/CausationId.java": "../java/causation_id.java",
        f"{JAVA_PORTS}/events/CommittedEvent.java": "../java/committed_event.java",
        f"{JAVA_PORTS}/events/CorrelationId.java": "../java/correlation_id.java",
        f"{JAVA_PORTS}/events/DomainEvent.java": "../java/domain_event.java",
        f"{JAVA_PORTS}/events/EventStore.java": "../java/event_store.java",
        f"{JAVA_PORTS}/events/EventStoreException.java": "../java/event_store_exception.java",
        f"{JAVA_PORTS}/events/EventVisitor.java": "../java/event_visitor.java",
        "src/main/java/com/example/deliverystarter/adapters/driven/eventstorememory/"
        "InMemoryEventStore.java": "../java/event_store_memory.java",
        "src/test/java/com/example/deliverystarter/eventstorecontract/EventStoreContract.java": (
            "../java/tests/event_store_contract.java"
        ),
        "src/test/java/com/example/deliverystarter/adapters/driven/eventstorememory/"
        "InMemoryEventStoreTest.java": "../java/tests/event_store_memory_test.java",
    },
    "sqlite": {
        "src/main/java/com/example/deliverystarter/adapters/driven/eventstoresqlite/"
        "SqliteEventStore.java": "../java/event_store_sqlite.java",
        "src/test/java/com/example/deliverystarter/adapters/driven/eventstoresqlite/"
        "SqliteEventStoreTest.java": "../java/tests/event_store_sqlite_test.java",
    },
    "postgres": {
        "src/main/java/com/example/deliverystarter/adapters/driven/eventstorepostgres/"
        "PostgresEventStore.java": "../java/event_store_postgres.java",
        "src/main/java/com/example/deliverystarter/config/DatabaseUrl.java": "../java/database_url.java",
        "src/main/java/com/example/deliverystarter/config/"
        "DatabaseUrlEnvironmentPostProcessor.java": "database_url_environment_post_processor.java",
        # Spring Boot's own registration file, which is how a post-processor is found before any bean
        # exists. The filename is the interface's own, so it cannot be anything else.
        "src/main/resources/META-INF/spring/"
        "org.springframework.boot.env.EnvironmentPostProcessor.imports": "environment_post_processor_registration",
        "src/main/java/com/example/deliverystarter/migrations/MigrateMain.java": "../java/migrate_main.java",
        # Flyway's own naming convention, `V<version>__<description>.sql`, from the same shared `.sql`
        # files every other SQL backend here reads. See the note in the sibling's block.
        "src/main/resources/db/migration/V1__events.sql": "../sql/001_events.sql",
        "src/main/resources/db/migration/V2__events_append_only.sql": "../sql/002_events_append_only.sql",
        "src/test/java/com/example/deliverystarter/adapters/driven/eventstorepostgres/"
        "PostgresEventStoreIT.java": "tests/event_store_postgres_it.java",
        "src/test/java/com/example/deliverystarter/config/DatabaseUrlTest.java": (
            "../java/tests/database_url_test.java"
        ),
    },
    "spring-web": {
        "src/main/java/com/example/deliverystarter/adapters/driving/http/SchemaFailure.java": (
            "../java/http_schema_failure.java"
        ),
        "src/main/java/com/example/deliverystarter/adapters/driving/http/NotFoundAdvice.java": (
            "http_not_found_advice.java"
        ),
        # The readiness contributor, not the endpoint: Actuator owns the route, and this is what the
        # application contributes to it. The composition root is not here either — `ServiceApplication`
        # in the skeleton is the whole of it, because the framework owns startup.
        "src/main/java/com/example/deliverystarter/adapters/driving/http/"
        "ServiceHealthIndicator.java": "http_health_indicator.java",
        "src/test/java/com/example/deliverystarter/adapters/driving/http/HttpAppTest.java": (
            "tests/http_app_test.java"
        ),
    },
    "keycloak": {
        "src/main/java/com/example/deliverystarter/adapters/driving/http/auth/"
        "KeycloakRoles.java": "../java/oidc_keycloak.java",
        "src/main/java/com/example/deliverystarter/adapters/driving/http/auth/"
        "SecurityConfig.java": "oidc_keycloak_security.java",
        "src/test/java/com/example/deliverystarter/adapters/driving/http/auth/"
        "KeycloakRolesTest.java": "../java/tests/oidc_keycloak_test.java",
    },
    "users-keycloak": {
        "src/main/java/com/example/deliverystarter/adapters/driving/http/users/"
        "CustomerIdentity.java": "../java/users_oidc_keycloak.java",
        "src/main/java/com/example/deliverystarter/adapters/driving/http/users/"
        "CustomerSecurityConfig.java": "users_security.java",
        "src/test/java/com/example/deliverystarter/adapters/driving/http/users/"
        "CustomerIdentityTest.java": "../java/tests/users_oidc_keycloak_test.java",
    },
}

# java-spring: the read side is the same set of files as its sibling framework's, because the
# event store and everything derived from it are framework-agnostic by construction — the port is
# what makes the framework's own datasource, migrations and health check a driven adapter's problem.
READ_SIDE: dict[str, dict[str, str]] = {
    "memory": {
        f"{JAVA_PORTS}/events/TagsOf.java": "../java/tags_of.java",
        f"{JAVA_PORTS}/events/TagQuery.java": "../java/tag_query.java",
        f"{JAVA_PORTS}/events/TaggedRead.java": "../java/tagged_read.java",
        f"{JAVA_PORTS}/events/Condition.java": "../java/condition.java",
        f"{JAVA_PORTS}/events/ConditionalAppendResult.java": "../java/conditional_append_result.java",
        f"{JAVA_PORTS}/readmodels/CheckpointStore.java": "../java/read_models.java",
        f"{JAVA_PORTS}/readmodels/Projection.java": "../java/projection.java",
        "src/main/java/com/example/deliverystarter/projections/Projections.java": "../java/projections.java",
        "src/main/java/com/example/deliverystarter/adapters/driven/eventstorememory/"
        "InMemoryDatabase.java": "../java/event_store_memory_database.java",
        "src/main/java/com/example/deliverystarter/adapters/driven/checkpointstorememory/"
        "InMemoryCheckpointStore.java": "../java/checkpoint_store_memory.java",
        "src/test/java/com/example/deliverystarter/checkpointstorecontract/"
        "CheckpointStoreContract.java": "../java/tests/checkpoint_store_contract.java",
        "src/test/java/com/example/deliverystarter/adapters/driven/checkpointstorememory/"
        "InMemoryCheckpointStoreTest.java": "../java/tests/checkpoint_store_memory_test.java",
        # What runs an async projection: the framework's own scheduler, ticking a catch-up pass.
        # One per framework, because `@Scheduled` is the framework's and so is how it finds the
        # project's `Projection` beans — and a hand-written worker loop is the thing this
        # replaces. Beside the runner rather than under `adapters/driving/`, because it ships with
        # the read side and everything under `adapters/driving/` goes with its transport.
        "src/main/java/com/example/deliverystarter/adapters/driving/projections/"
        "ScheduledProjections.java": "scheduled_projections.java",
        # The runner has no I/O of its own, so its suite runs whatever the store is — which is why
        # it is here under the feature every project has rather than beside an adapter.
        "src/test/java/com/example/deliverystarter/projections/ProjectionsTest.java": (
            "../java/tests/projections_test.java"
        ),
    },
    "sqlite": {
        "src/main/java/com/example/deliverystarter/adapters/driven/checkpointstoresqlite/"
        "SqliteCheckpointStore.java": "../java/checkpoint_store_sqlite.java",
        "src/test/java/com/example/deliverystarter/adapters/driven/checkpointstoresqlite/"
        "SqliteCheckpointStoreTest.java": "../java/tests/checkpoint_store_sqlite_test.java",
    },
    "postgres": {
        # The unit of work, delegated to the framework that owns transactions. The port is
        # shared with the sibling framework; `SpringTransactions` is the one class in the project that
        # names a transaction API, which is why there is one per framework and no `ThreadLocal`
        # anywhere. It is here rather than in the write-side table because the seam exists for
        # the read side: an inline view and an async checkpoint both have to commit inside
        # somebody else's transaction, and the framework is what binds a connection to one.
        "src/main/java/com/example/deliverystarter/adapters/driven/sql/Transactions.java": (
            "../java/transactions.java"
        ),
        "src/main/java/com/example/deliverystarter/adapters/driven/sql/SpringTransactions.java": (
            "spring_transactions.java"
        ),
        "src/main/java/com/example/deliverystarter/adapters/driven/checkpointstorepostgres/"
        "PostgresCheckpointStore.java": "../java/checkpoint_store_postgres.java",
        # Flyway orders by the version in the name, so the shared `.sql` files arrive under its
        # convention rather than the numeric one the other backends' runners read.
        "src/main/resources/db/migration/V3__projection_checkpoints.sql": "../sql/003_projection_checkpoints.sql",
        "src/main/resources/db/migration/V4__event_tags.sql": "../sql/004_event_tags.sql",
        "src/test/java/com/example/deliverystarter/adapters/driven/checkpointstorepostgres/"
        "PostgresCheckpointStoreIT.java": "tests/checkpoint_store_postgres_it.java",
    },
}


# The route that serves the flags to a browser app, as a file this framework discovers, keyed by the HTTP
# option it belongs to (`flag_route.flag_resource`). No `entry_wiring`: the framework owns the entry point.
FLAG_ROUTE = {
    "spring-web": Resource(
        destination=(
            "src/main/java/com/example/deliverystarter/adapters/driving/http/FeatureFlagsController.java"
        ),
        source="http_flags_controller.java",
    ),
}


# Readiness as `java_quarkus.py` says: the path the framework serves, which is `HEALTH_PATH`. The body is
# Actuator's, and shorter than its sibling's for a reason worth stating: MicroProfile Health always reports
# the per-check breakdown, while Actuator hides it unless `show-details` says otherwise — and this project
# leaves that at `never`, because which dependencies a service has is not something an unauthenticated
# caller needs. Same status vocabulary, one fewer disclosure.
#
# The rest of its toolchain is Maven's and the family's (`java_toolchain.py`). Its own, first: the Spring Boot
# plugin's run goal, which compiles first and then runs the application from the exploded classes — so
# `./mvnw compile` in a second terminal is picked up. That is a weaker reload than its sibling's, and honestly
# so: Quarkus recompiles on the next request by itself, whereas this is Spring Boot without
# `spring-boot-devtools`, which is not a dependency here because it also restarts on every classpath change a
# container mount produces. Reads HOST and PORT through `application.properties`, so the container and the
# laptop are configured the same way.
#
# And a `make mutation` that is a real target, not a placeholder: this is the one backend in this factory where
# that is true. PIT is configured in the pom over the domain packages with `*IT` excluded; pitest issue #1287 —
# the timeouts that make the Quarkus sibling ship a documented gap instead — reports the same setup working
# under Spring Boot.
#
# No `-DskipTests`, and that is not an oversight to tidy up. It reads like the right flag — PIT runs the tests
# itself, once per mutant, so Surefire running them first buys nothing — and `test-compile` does not run tests
# anyway, so it buys nothing either. What it *does* do is make pitest skip the entire project: "Skipping project
# because: Test execution should be skipped (-DskipTests)", exit 0, no report. Combined with a target no gate
# runs, that is a mutation score nobody has that looks exactly like one everybody passed.
LANGUAGE = protocol.Language(backends=(protocol.Backend("java-spring", "java", {
    protocol.SERVICE_FILES: service_files,
    protocol.NAME_SERVICE: name_service,
    protocol.REPOSITORY_FILES: repository_files,
    protocol.READY_PATH: HEALTH_PATH,
    protocol.WRITE_SIDE_FILES: WRITE_SIDE,
    protocol.READ_SIDE_FILES: READ_SIDE,
    protocol.ENTRY_WIRING: {},
    protocol.FLAG_RESOURCE: FLAG_ROUTE,
    # The framework opens its own store, so the entry point has nothing to wire (`composition.wire_store`).
    protocol.ENTRY_STORE: None,
    protocol.HEALTH_BODY: '{"status":"UP"}',
    protocol.DEV_COMMAND: maven_dev_command("spring-boot:run"),
    protocol.NATIVE_COMMANDS: maven_native_commands(f"{MVNW} test-compile org.pitest:pitest-maven:mutationCoverage"),
    protocol.IMAGE_BUILDER: {
        "tool": "",
        # Spring Boot's own buildpack build, into the daemon; the builder is pinned in the pom.
        "build": (
            f"{MAVEN} spring-boot:build-image -Dspring-boot.build-image.imageName={IMAGE} "
            "-Dspring-boot.build-image.imagePlatform=$(PLATFORM)"
        ),
    },
    # Flyway migrates as the service starts, switched on in production only.
    protocol.MIGRATIONS_IN_PRODUCTION: {"environment": {"SPRING_FLYWAY_ENABLED": "true"}},
    # Nothing, deliberately: pgjdbc does not read `PGSSLMODE`, and that was checked, so `None` is written out.
    # Per managed-database kind; `images.py`, above `POSTGRES_SSLMODE_KINDS`, says how each was measured.
    protocol.POSTGRES_SSLMODE: {"rds": None, "flexible-server": None},
    protocol.SERVICE_DESCRIPTORS: {},
}),))
