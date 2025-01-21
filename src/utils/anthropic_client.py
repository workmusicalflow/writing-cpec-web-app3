from anthropic import Anthropic, APIError, APIConnectionError, RateLimitError
import os
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

class AnthropicClient:
    def __init__(self):
        """Initialise le client Anthropic avec gestion des erreurs"""
        try:
            api_key = os.environ.get("ANTHROPIC_API_KEY")
            if not api_key:
                raise ValueError("ANTHROPIC_API_KEY manquant dans les variables d'environnement")
            
            self.client = Anthropic(api_key=api_key)
            self.default_model = "claude-3-5-sonnet-20241022"
            logger.info("Client Anthropic initialisé avec succès")
            
        except Exception as e:
            logger.error(f"Erreur d'initialisation du client Anthropic : {str(e)}")
            raise

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        model: Optional[str] = None
    ) -> str:
        """
        Génère une réponse à partir du modèle Claude avec gestion robuste des erreurs.

        Args:
            prompt: Le prompt principal (doit contenir au moins 10 caractères)
            system_prompt: Le prompt système optionnel
            model: Le modèle à utiliser (utilise le modèle par défaut si non spécifié)

        Returns:
            La réponse générée par le modèle

        Raises:
            ValueError: Si le prompt est invalide
            APIError: En cas d'erreur de l'API Anthropic
            Exception: Pour les autres erreurs inattendues
        """
        # Validation des entrées
        if not isinstance(prompt, str) or len(prompt.strip()) < 10:
            error_msg = "Le prompt doit être une chaîne de caractères d'au moins 10 caractères"
            logger.error(error_msg)
            raise ValueError(error_msg)

        try:
            messages = [{
                "role": "user",
                "content": prompt
            }]

            logger.info(f"Génération de réponse avec le modèle {model or self.default_model}")
            
            response = self.client.messages.create(
                model=model or self.default_model,
                messages=messages,
                system=system_prompt,
                max_tokens=4096
            )

            if not response.content:
                error_msg = "Aucun contenu dans la réponse de l'API"
                logger.error(error_msg)
                raise APIError(error_msg)

            return response.content[0].text

        except RateLimitError as e:
            error_msg = "Limite de taux d'API dépassée. Veuillez réessayer plus tard."
            logger.error(f"{error_msg} Détails : {str(e)}")
            raise APIError(error_msg) from e
            
        except APIConnectionError as e:
            error_msg = "Erreur de connexion à l'API Anthropic. Vérifiez votre connexion internet."
            logger.error(f"{error_msg} Détails : {str(e)}")
            raise APIConnectionError(error_msg) from e
            
        except APIError as e:
            error_msg = f"Erreur de l'API Anthropic : {str(e)}"
            logger.error(error_msg)
            raise APIError(error_msg) from e
            
        except Exception as e:
            error_msg = f"Erreur inattendue : {str(e)}"
            logger.error(error_msg)
            raise Exception(error_msg) from e
