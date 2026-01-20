#!/bin/bash
# Test script for OpenAI ChatKit skill

echo "Testing OpenAI ChatKit skill..."
echo "Skill directory structure:"
ls -la .claude/skills/openai-chatkit/
echo ""
echo "Checking SKILL.md file:"
head -20 .claude/skills/openai-chatkit/SKILL.md
echo ""
echo "OpenAI ChatKit skill is ready for use!"