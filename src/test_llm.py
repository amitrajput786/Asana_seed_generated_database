from dotenv import load_dotenv
from utils.llm import LLMClient

load_dotenv()

try:
    llm = LLMClient()
    result = llm.generate("Say hello in one sentence")
    print("✓ LLM works!")
    print(f"Response: {result}")
except Exception as e:
    print(f"✗ LLM failed: {e}")