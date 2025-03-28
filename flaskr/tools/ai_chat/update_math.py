import re

# Replace with your actual file name
filename = "./flaskr/tools/ai_chat/ex5.md"

# Read the file content
with open(filename, "r", encoding="utf-8") as file:
    content = file.read()

# Pattern 1: Replace '\( something\)' with '$something$'
#   - r'\\\(' matches the literal "\("
#   - \s* allows for optional whitespace after "\(" and before "\)"
#   - (.*?) non-greedily captures any content
#   - r'\\\)' matches the literal "\)"
content = re.sub(
    r'\\\(\s*(.*?)\s*\\\)',
    lambda match: f"${match.group(1)}$",
    content,
)

# Pattern 2: Replace '\[something\]' with '$$something$$'
#   - r'\\\[' matches the literal "\["
#   - similar structure is used as above for the content capture
content = re.sub(
    r'\\\[\s*(.*?)\s*\\\]',
    lambda match: f"$${match.group(1)}$$",
    content,
)


filename = "./flaskr/tools/ai_chat/ex6.md"
# Write the modified content back to the same file
with open(filename, "w", encoding="utf-8") as file:
    file.write(content)
