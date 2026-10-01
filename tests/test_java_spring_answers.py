"""What the Spring Boot framework answers for itself, in a project generated from this package beside its family.

The family's files arrive too (the Maven wrapper), read from the `java` package this one requires; what is Spring
Boot's own — the buildpack image build, the working PIT target — is this package's.
"""
from __future__ import annotations

import tempfile

from support import FactoryTestCase


class SpringAnswersTest(FactoryTestCase):
    def test_a_spring_project_builds_its_image_with_buildpacks_and_runs_pit(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo = self.generate(directory, "spring-own", language="java-spring", target="aws")
            self.assertIn("paketobuildpacks/builder-noble-java-tiny", (repo / "apps/service/pom.xml").read_text())
            makefile = (repo / "Makefile").read_text()
            self.assertIn("spring-boot:build-image", makefile)
            self.assertIn("org.pitest:pitest-maven:mutationCoverage", makefile)
            self.assertTrue((repo / "apps/service/mvnw").is_file())
