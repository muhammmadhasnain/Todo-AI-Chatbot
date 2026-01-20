#!/usr/bin/env python3
"""
Simple script to package the MCP SDK skill into a distributable format
"""

import os
import zipfile
from pathlib import Path


def package_skill(skill_dir: str, output_path: str = None):
    """
    Package the skill directory into a .skill file
    """
    skill_path = Path(skill_dir)

    if not skill_path.exists():
        raise FileNotFoundError(f"Skill directory does not exist: {skill_path}")

    if not output_path:
        output_path = f"{skill_path.name}.skill"

    # Create the zip file
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(skill_path):
            for file in files:
                file_path = Path(root) / file
                # Add file to zip with relative path
                zipf.write(file_path, file_path.relative_to(skill_path.parent))

    print(f"SUCCESS: Skill packaged successfully: {output_path}")
    print(f"SIZE: {Path(output_path).stat().st_size} bytes")


if __name__ == "__main__":
    import sys

    skill_dir = "mcp-sdk-skill"
    output_path = "mcp-sdk.skill"

    if len(sys.argv) > 1:
        skill_dir = sys.argv[1]

    if len(sys.argv) > 2:
        output_path = sys.argv[2]

    try:
        package_skill(skill_dir, output_path)
        print(f"\nTo use this skill, install it with Claude Code:")
        print(f"  Claude Code will recognize the .skill file format")
    except Exception as e:
        print(f"ERROR: Error packaging skill: {e}")
        sys.exit(1)