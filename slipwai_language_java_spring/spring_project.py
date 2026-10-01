"""What the Spring Boot framework decides about the project around its service: the build output git ignores, the
gate's test harness, and what its working `make mutation` target mutates.

Moved from the `java` family's `java_project.py` (S05's answers), because they are this framework's and not the
family's: a framework author changes them in this package."""
from __future__ import annotations

from typing import Any

from slipwai import registry as protocol

# What `make mutation` does on the Spring backend, where it is a working target rather than a placeholder.
#
# Emitted above the target for the same reason its sibling's note is: the next person to read a mutation
# score needs to know what was mutated before they trust it. Make comments do not match the `help` grep, so
# this stays out of `make help`.
JAVA_SPRING_MUTATION_NOTE = """\
# Wired up and scoped, and the scope is the part to read before trusting a score.
#
# PIT mutates the packages named in `pitest-maven`'s `targetClasses` in `__APP__/pom.xml` — the
# domain, the ports, the URL parser and the group mapping — and runs the plain `*Test` classes over them.
# That is deliberate on both sides:
#
#   1. Those packages are framework-free by construction, which is the whole reason the hexagon puts them
#      there, and they are where a surviving mutant means a rule nothing checks.
#   2. `*IT` is excluded. PIT runs the tests once per mutant, so a database suite in scope would turn a
#      minutes-long run into an hours-long one, for coverage of wiring rather than of rules.
#   3. Two classes inside those packages are excluded by name — `SecurityConfig` and the
#      `EnvironmentPostProcessor`. They are how a decision gets plugged into Spring rather than the
#      decision, so their mutants survive by nature: killing one would mean asserting Spring's own wiring.
#
# The report lands in `target/pit-reports/`. It fails rather than passes when it finds nothing to mutate,
# which is deliberate: `failWhenNoMutations` is `true` in the pom because "0 mutations" here can only mean
# a misconfigured run, and a silent pass on a target no gate runs is worse than a red one.
#
# So a clean run here does NOT mean the adapters are well tested; it means the rules are. Widen
# `targetClasses` as use cases arrive, and leave the adapters out — their tests are about wiring, and
# mutating wiring mostly produces survivors nobody should act on.
#
# No threshold is set. A score nobody has looked at yet is not a gate, and this target is run by no gate at
# either level (docs/backend-obligations.md section 2) — so read the survivors, then decide.
"""

SPRING: dict[protocol.Member[Any], object] = {
    # `target/` for the same reason, and nothing else: Spring Boot's plugin writes the repackaged jar
    # and the `build-info` inside it rather than beside the pom, so there is no second file to ignore.
    protocol.GITIGNORE: "target/\n",
    protocol.GATE_DESCRIPTION: (
        "Checkstyle, PMD and SpotBugs for lint; `javac` with Error Prone and NullAway for the type check; "
        "JUnit 5 with Spring Boot's test harness and MockMvc, coverage through JaCoCo"
    ),
    protocol.MUTATION_NOTE: JAVA_SPRING_MUTATION_NOTE,
}
