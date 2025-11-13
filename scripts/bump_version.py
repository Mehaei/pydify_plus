# -*- coding: utf-8 -*-

# @Author: 胖胖很瘦
# @Date: 2025-11-11 18:26:30
# @LastEditors: 胖胖很瘦
# @LastEditTime: 2025-11-12 16:50:16

#!/usr/bin/env python3
"""Script to automatically bump version numbers."""

import re
import sys
from pathlib import Path


def get_current_version() -> str:
    """Get current version from pyproject.toml."""
    pyproject_path = Path("pyproject.toml")
    content = pyproject_path.read_text()

    match = re.search(r'version\s*=\s*["\']([^"\']+)["\']', content)
    if match:
        return match.group(1)
    raise ValueError("Could not find version in pyproject.toml")


def bump_version(version: str, bump_type: str) -> str:
    """Bump version number based on type."""
    parts = version.split('.')

    if len(parts) != 3:
        raise ValueError(f"Invalid version format: {version}")

    major, minor, patch = map(int, parts)

    if bump_type == "major":
        return f"{major + 1}.0.0"
    elif bump_type == "minor":
        return f"{major}.{minor + 1}.0"
    elif bump_type == "patch":
        return f"{major}.{minor}.{patch + 1}"
    else:
        raise ValueError(f"Invalid bump type: {bump_type}")


def update_version(new_version: str):
    """Update version in all relevant files."""
    # Update pyproject.toml
    pyproject_path = Path("pyproject.toml")
    content = pyproject_path.read_text()
    content = re.sub(
        r'(version\s*=\s*["\'])[^"\']+(["\'])',
        f'\\g<1>{new_version}\\g<2>',
        content
    )
    pyproject_path.write_text(content)

    # Update __init__.py if it contains version
    init_path = Path("pydify_plus/__init__.py")
    if init_path.exists():
        content = init_path.read_text()
        content = re.sub(
            r'(__version__\s*=\s*["\'])[^"\']+(["\'])',
            f'\\g<1>{new_version}\\g<2>',
            content
        )
        init_path.write_text(content)

    print(f"✅ Updated version to {new_version}")


def main():
    """Main entry point."""
    if len(sys.argv) != 2:
        print("Usage: python bump_version.py <major|minor|patch>")
        sys.exit(1)

    bump_type = sys.argv[1]

    if bump_type not in ["major", "minor", "patch"]:
        print("Error: bump_type must be one of: major, minor, patch")
        sys.exit(1)

    try:
        current_version = get_current_version()
        new_version = bump_version(current_version, bump_type)

        print(f"Current version: {current_version}")
        print(f"New version: {new_version}")

        confirm = input("Confirm version bump? (y/N): ")
        if confirm.lower() in ['y', 'yes']:
            update_version(new_version)
            print(f"\nNext steps:")
            print(f"1. git add pyproject.toml pydify_plus/__init__.py")
            print(f"2. git commit -m 'Bump version to {new_version}'")
            print(f"3. git tag v{new_version}")
            print(f"4. git push origin main --tags")
        else:
            print("Version bump cancelled.")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
