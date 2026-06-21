"""DeepSeek API service with letter-by-letter streaming, table generation, numbering"""

import httpx
import asyncio
from typing import AsyncGenerator, Tuple
from app.config import settings


class DeepSeekService:
    """Service for DeepSeek API with full educational formatting"""
    
    def __init__(self):
        self.api_key = settings.DEEPSEEK_API_KEY
        self.timeout = 60.0
    
    def _build_system_prompt(self, language: str, grade: str, subject: str, reasoning: bool) -> str:
        """Build system prompt with full formatting instructions"""
        
        language_prompts = {
            "english": "Respond in English.",
            "zulu": "Respond in isiZulu.",
            "xhosa": "Respond in isiXhosa.",
            "shona": "Respond in chiShona."
        }
        
        prompt = f"""
You are Luvuno, the quantum AI assistant for Tshaka M Academy — Africa's premier home-schooling platform.

{language_prompts.get(language, language_prompts['english'])}

Grade Level: {grade}
Subject: {subject}

FORMATTING RULES (STRICT):
1. NEVER use asterisks (*) for emphasis. Use **bold** for emphasis.
2. For paragraphs, use double line breaks (\\n\\n) between paragraphs.
3. For numbered lists, use numbers with periods (1., 2., 3.).
4. For bullet lists, use dashes (-) with line breaks.
5. For tables, use the following format:
   | Header 1 | Header 2 | Header 3 |
   |----------|----------|----------|
   | Row 1    | Data     | Data     |
   | Row 2    | Data     | Data     |

6. For code blocks, use ```language and ```.
7. Use proper heading levels (### for subheadings).
8. Use emojis where appropriate to make learning engaging.
9. For mathematical equations, use standard notation.

RESPONSE STYLE:
- Be educational, clear, and encouraging
- Break down complex topics step by step
- Use examples relevant to African context
- Include practical applications
- Adapt to {grade} level understanding
- For university level, be rigorous and detailed
- For younger grades, be simple and engaging
"""
        
        if reasoning:
            prompt += """
QUANTUM REASONING MODE ACTIVATED:
Break down your response into 4 clear steps:
Step 1: Problem Decomposition — Analyse the question
Step 2: Pattern Recognition — Identify key concepts
Step 3: Quantum-Inspired Optimization — Apply principles
Step 4: Synthesis — Combine into clear answer
"""
        
        return prompt
    
    async def stream_response(
        self,
        message: str,
        language: str = "english",
        grade: str = "university",
        subject: str = "general",
        reasoning: bool = False,
        speed: int = 35
    ) -> AsyncGenerator[str, None]:
        """Stream response letter-by-letter with adjustable speed"""
        
        if not self.api_key:
            yield self._get_offline_response(message, language)
            return
        
        system_prompt = self._build_system_prompt(language, grade, subject, reasoning)
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    "https://api.deepseek.com/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "deepseek-chat",
                        "messages": [
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": message}
                        ],
                        "temperature": 0.7,
                        "max_tokens": 4096,
                        "stream": True
                    }
                )
                
                # Process streaming response
                buffer = ""
                async for chunk in response.aiter_text():
                    buffer += chunk
                    # Yield complete words/characters for letter-by-letter effect
                    for char in chunk:
                        yield char
                        await asyncio.sleep(1 / speed)
                
        except Exception as e:
            yield f"[System error: {str(e)}]"
    
    def _get_offline_response(self, message: str, language: str) -> str:
        """Offline fallback response (simplified)"""
        responses = {
            "english": "I am Luvuno, your quantum AI assistant. Tshaka M Academy is currently offline. Please connect to the internet for full quantum-powered responses.",
            "zulu": "NginguLuvuno, umsizi wakho we-AI. I-Tshaka M Academy ayixhunyiwe. Sicela uxhume ku-inthanethi ukuze uthole izimpendulo ezigcwele.",
            "xhosa": "NdinguLuvuno, umncedisi wakho we-AI. I-Tshaka M Academy ayixhunyiwe. Nceda uxhume kwi-inthanethi ukuze ufumane iimpendulo ezigcweleyo.",
            "shona": "Ndini Luvuno, mubatsiri wako we-AI. Tshaka M Academy haina kubatana. Ndapota batana ne-internet kuti uwane mhinduro dzakazara."
        }
        return responses.get(language, responses["english"])
    
    def format_with_tables(self, text: str) -> str:
        """Ensure tables are properly formatted"""
        # This is a placeholder — the actual formatting is handled by the prompt
        return text


deepseek_service = DeepSeekService()
