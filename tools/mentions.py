import re
from tools import read_file

def expand_mentions(text):
	paths = re.findall(r"@([\w./~\\-]+)", text)

	if not paths:
		return text 

	chunks = [text]

	for path in paths:
		chunks.append(read_file(path))

	return "\n\n".join(chunks)