import sys
from pathlib import Path

# Ensure repository root is on sys.path so package imports work when running from this folder
ROOT = Path(__file__).parent.parent.resolve()
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from llm import OllamaClient


client = OllamaClient()

prompt = """
Return JSON only:
{
  "score": 5,
  "reason": "Test"
}
"""

response = client.generate(prompt)
print(response)

