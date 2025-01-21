from anthropic import Anthropic
import os
from typing import Optional

class AnthropicClient:
    def __init__(self):
        self.client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
        self.default_model = "claude-3-5-sonnet-20241022"

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        model: Optional[str] = None
    ) -> str:
        """
        Génère une réponse à partir du modèle Claude.

        Args:
        prompt: Le prompt principal
        system_prompt: Le prompt système optionnel
        model: Le modèle à utiliser (utilise le modèle par défaut si non spécifié)

        Returns:
        La réponse générée par le modèle
        """
        messages = [{
            "role": "user",
            "content": prompt
        }]

        response = self.client.messages.create(
            model=model or self.default_model,
            messages=messages,
            system=system_prompt,
            max_tokens=4096
        )

        return response.content[0].text
