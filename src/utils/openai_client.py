import openai
import os
from typing import Optional, Literal
import logging
from functools import lru_cache

logger = logging.getLogger(__name__)

class OpenAIClient:
    MODELS = Literal["gpt-4o-mini", "gpt-4o"]

    def __init__(self, default_model: MODELS = "gpt-4o-mini"):
        """Initialise le client OpenAI avec gestion des erreurs et support des modèles GPT-4o mini et GPT-4o

        Args:
            default_model: Le modèle OpenAI à utiliser par défaut (gpt-4o-mini ou gpt-4o)
        """
        self.api_key = self._get_api_key()
        self.client = openai.OpenAI(api_key=self.api_key)
        self.default_model = default_model
        logger.info(f"Client OpenAI initialisé avec succès (modèle par défaut: {default_model})")

    @staticmethod
    @lru_cache(maxsize=1)
    def _get_api_key() -> str:
        """Récupère et met en cache la clé API OpenAI"""
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY manquant dans les variables d'environnement")
        return api_key

    def generate(self, prompt: str, system_prompt: Optional[str] = None, model: Optional[MODELS] = None) -> str:
        """
        Génère une réponse à partir du modèle GPT spécifié avec gestion robuste des erreurs.

        Args:
            prompt: Le prompt principal
            system_prompt: Le prompt système optionnel
            model: Le modèle à utiliser (gpt-4o-mini ou gpt-4o, utilise le modèle par défaut si non spécifié)

        Returns:
            La réponse générée par le modèle
        """
        try:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})

            selected_model = model or self.default_model
            max_tokens = 4096 if selected_model == "gpt-4o" else 2048  # GPT-4o mini a une limite de 2048 tokens

            response = self.client.chat.completions.create(
                model=selected_model,
                messages=messages,
                max_tokens=max_tokens
            )

            if not response.choices:
                raise ValueError("Aucune réponse générée")

            return response.choices[0].message.content

        except openai.APIError as e:
            logger.error(f"Erreur API OpenAI : {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Erreur inattendue lors de la génération : {str(e)}")
            raise

    @classmethod
    def get_available_models(cls) -> list[MODELS]:
        """Renvoie la liste des modèles disponibles"""
        return list(cls.MODELS.__args__)

    def estimate_cost(self, prompt: str, system_prompt: Optional[str] = None, model: Optional[MODELS] = None) -> float:
        """
        Estime le coût de la génération en fonction du modèle et du nombre de tokens.

        Args:
            prompt: Le prompt principal
            system_prompt: Le prompt système optionnel
            model: Le modèle à utiliser (gpt-4o-mini ou gpt-4o, utilise le modèle par défaut si non spécifié)

        Returns:
            Le coût estimé en dollars
        """
        selected_model = model or self.default_model
        total_tokens = len(prompt.split()) + (len(system_prompt.split()) if system_prompt else 0)

        if selected_model == "gpt-4o-mini":
            input_cost = 0.15 / 1_000_000  # $0.15 par million de tokens en entrée
            output_cost = 0.60 / 1_000_000  # $0.60 par million de tokens en sortie
        else:  # gpt-4o
            input_cost = 2.50 / 1_000_000  # $2.50 par million de tokens en entrée
            output_cost = 10.0 / 1_000_000  # $10.00 par million de tokens en sortie

        estimated_input_cost = total_tokens * input_cost
        estimated_output_cost = total_tokens * output_cost  # Estimation grossière, peut varier

        return estimated_input_cost + estimated_output_cost
