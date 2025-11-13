#!/usr/bin/env python3
"""Release script for Dify Client."""

import argparse
import subprocess
import sys
from pathlib import Path


class ReleaseManager:
    """Manages the release process for Dify Client."""

    def __init__(self):
        self.project_root = Path(__file__).parent.parent

    def run_command(self, cmd: str, check: bool = True) -> str:
        """Run a shell command and return its output."""
        print(f"Running: {cmd}")
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=self.project_root)

        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)

        if check and result.returncode != 0:
            raise RuntimeError(f"Command failed with exit code {result.returncode}: {cmd}")

        return result.stdout

    def check_clean_working_directory(self):
        """Ensure the working directory is clean."""
        status = self.run_command("git status --porcelain")
        if status.strip():
            raise RuntimeError("Working directory is not clean. Please commit or stash changes.")

    def run_tests(self):
        """Run the test suite."""
        print("\nRunning tests...")
        self.run_command("pytest --cov=pydify_plus --cov-report=html --cov-report=xml")

    def run_linters(self):
        """Run code quality checks."""
        print("\nRunning linters...")
        self.run_command("black --check pydify_plus tests")
        self.run_command("flake8 pydify_plus tests")
        self.run_command("mypy pydify_plus")

    def build_package(self):
        """Build the package."""
        print("\nBuilding package...")
        self.run_command("python -m build")

    def check_package(self):
        """Check the built package."""
        print("\nChecking package...")
        self.run_command("twine check dist/*")

    def get_current_version(self) -> str:
        """Get the current version from pyproject.toml."""
        pyproject_path = self.project_root / "pyproject.toml"
        content = pyproject_path.read_text()

        for line in content.split('\n'):
            if line.strip().startswith('version ='):
                return line.split('=')[1].strip().strip('"\'')

        raise RuntimeError("Could not find version in pyproject.toml")

    def update_version(self, new_version: str):
        """Update version in pyproject.toml."""
        pyproject_path = self.project_root / "pyproject.toml"
        content = pyproject_path.read_text()

        lines = []
        for line in content.split('\n'):
            if line.strip().startswith('version ='):
                lines.append(f'version = "{new_version}"')
            else:
                lines.append(line)

        pyproject_path.write_text('\n'.join(lines))
        print(f"Updated version to {new_version}")

    def create_tag(self, version: str):
        """Create a git tag for the release."""
        print(f"\nCreating tag v{version}...")
        self.run_command(f"git tag -a v{version} -m 'Release v{version}'")

    def push_changes(self):
        """Push changes and tags to remote."""
        print("\nPushing changes...")
        self.run_command("git push origin main")
        self.run_command("git push --tags")

    def publish_to_pypi(self, test: bool = False):
        """Publish package to PyPI."""
        print(f"\nPublishing to {'Test PyPI' if test else 'PyPI'}...")

        if test:
            # Use Test PyPI for testing
            repository_url = "--repository-url https://test.pypi.org/legacy/"
        else:
            repository_url = ""

        self.run_command(f"twine upload {repository_url} dist/*")

        print(f"✅ Package published to {'Test PyPI' if test else 'PyPI'}!")

    def release(self, version: str, skip_tests: bool = False, test_pypi: bool = False):
        """Perform a full release."""
        print(f"Starting release process for version {version}...")

        try:
            # Pre-release checks
            self.check_clean_working_directory()

            if not skip_tests:
                self.run_tests()
                self.run_linters()

            # Update version
            self.update_version(version)

            # Build and check package
            self.build_package()
            self.check_package()

            # Commit version change
            self.run_command(f'git add pyproject.toml')
            self.run_command(f'git commit -m "Bump version to {version}"')

            # Create tag
            self.create_tag(version)

            # Push changes
            self.push_changes()

            # Publish to PyPI
            self.publish_to_pypi(test=test_pypi)

            print(f"\n✅ Release v{version} completed successfully!")
            print(f"\n📦 Package published to: {'Test PyPI' if test_pypi else 'PyPI'}")
            print(f"🏷️  Git tag: v{version}")

        except Exception as e:
            print(f"\n❌ Release failed: {e}")
            sys.exit(1)


def main():
    """Main entry point for the release script."""
    parser = argparse.ArgumentParser(description="Release Dify Client package")
    parser.add_argument("version", help="New version number (e.g., 1.0.0)")
    parser.add_argument("--skip-tests", action="store_true", help="Skip running tests")
    parser.add_argument("--test-pypi", action="store_true", help="Publish to Test PyPI instead of production")

    args = parser.parse_args()

    manager = ReleaseManager()
    manager.release(
        version=args.version,
        skip_tests=args.skip_tests,
        test_pypi=args.test_pypi
    )


if __name__ == "__main__":
    main()
