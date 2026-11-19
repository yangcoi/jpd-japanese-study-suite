import re

with open('/Users/yangcoi/Documents/jdp1.html', 'r', encoding='utf-8') as f:
    text = f.read()

# basic brace matcher
lines = text.split('\n')
stack = []
for i, line in enumerate(lines):
    # ignore lines with comments maybe?
    for j, char in enumerate(line):
        if char == '{':
            stack.append(('{', i+1))
        elif char == '}':
            if stack and stack[-1][0] == '{':
                stack.pop()
            else:
                print(f"Unmatched }} at line {i+1}")
        elif char == '(':
            stack.append(('(', i+1))
        elif char == ')':
            if stack and stack[-1][0] == '(':
                stack.pop()
            else:
                print(f"Unmatched ) at line {i+1}")
        elif char == '<':
            # Not tracking HTML tags closely, but let's see
            pass

print(f"Remaining in stack: {stack[:5]} ... (total {len(stack)})")
