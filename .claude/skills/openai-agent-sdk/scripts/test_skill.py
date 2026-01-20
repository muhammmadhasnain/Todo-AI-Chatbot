# Test script for OpenAI Agent SDK skill
# This script demonstrates the basic usage patterns described in the skill

def test_skill_structure():
    """Test that the skill files exist and are properly structured"""
    import os

    skill_path = ".claude/skills/openai-agent-sdk"

    # Check if main skill file exists
    assert os.path.exists(f"{skill_path}/SKILL.md"), "SKILL.md file not found"

    # Check if references exist
    assert os.path.exists(f"{skill_path}/references/documentation.md"), "Documentation reference file not found"

    # Check directories
    assert os.path.exists(f"{skill_path}/scripts"), "Scripts directory not found"
    assert os.path.exists(f"{skill_path}/references"), "References directory not found"
    assert os.path.exists(f"{skill_path}/assets"), "Assets directory not found"

    print("[PASS] Skill structure is correct")

    # Read the skill file to verify content
    with open(f"{skill_path}/SKILL.md", 'r') as f:
        content = f.read()
        assert "OpenAI Agent SDK" in content, "OpenAI Agent SDK not found in skill content"
        assert "function_tool" in content, "function_tool example not found in skill content"
        assert "handoffs" in content, "handoffs example not found in skill content"

    print("[PASS] Skill content is valid")

    return True

if __name__ == "__main__":
    test_skill_structure()
    print("All tests passed! The OpenAI Agent SDK skill is properly structured and ready to use.")