"""LLM client for Groq API"""

import os
import json
import logging
from typing import Optional
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LLMClient:
    """Groq LLM client for text generation"""
    
    def __init__(self):
        api_key = os.getenv('GROQ_API_KEY')
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        
        self.client = Groq(api_key=api_key)
        self.model = "llama-3.1-8b-instant"  # Fast and efficient
        self.cache = {}  # Simple cache to reduce API calls
        
    def generate(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 500
    ) -> str:
        """Generate text using Groq API"""
        # Check cache
        cache_key = f"{prompt[:100]}_{temperature}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that generates realistic business data for a B2B SaaS company."
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            result = response.choices[0].message.content.strip()
            self.cache[cache_key] = result
            return result
            
        except Exception as e:
            logger.error(f"LLM generation failed: {e}")
            return ""
    
    def generate_task_names(
        self,
        project_type: str,
        project_context: str,
        team_name: str,
        count: int = 10
    ) -> list[str]:
        """Generate realistic task names"""
        prompt = self._load_prompt('task_names.txt').format(
            project_type=project_type,
            project_context=project_context,
            team_name=team_name
        )
        
        response = self.generate(prompt, temperature=0.8)
        
        try:
            # Try to parse JSON array
            tasks = json.loads(response)
            if isinstance(tasks, list):
                return tasks[:count]
        except json.JSONDecodeError:
            # Fallback: split by newlines
            lines = [l.strip().strip('-').strip('•').strip() 
                    for l in response.split('\n') if l.strip()]
            return lines[:count]
        
        return []
    
    def generate_description(
        self,
        task_name: str,
        project_type: str,
        team_name: str,
        length: str = 'short'
    ) -> str:
        """Generate task description"""
        if length == 'empty':
            return ""
            
        prompt = self._load_prompt('descriptions.txt').format(
            task_name=task_name,
            project_type=project_type,
            team_name=team_name,
            empty_chance=0
        )
        
        return self.generate(prompt, temperature=0.7, max_tokens=150)
    
    def generate_comment(
        self,
        task_name: str,
        comment_type: str,
        author_role: str
    ) -> str:
        """Generate task comment"""
        prompt = self._load_prompt('comments.txt').format(
            task_name=task_name,
            comment_type=comment_type,
            author_role=author_role
        )
        
        return self.generate(prompt, temperature=0.8, max_tokens=100)
    
    def _load_prompt(self, filename: str) -> str:
        """Load prompt template from file"""
        prompt_path = os.path.join('prompts', filename)
        try:
            with open(prompt_path, 'r') as f:
                return f.read()
        except FileNotFoundError:
            logger.warning(f"Prompt file not found: {prompt_path}")
            return ""
