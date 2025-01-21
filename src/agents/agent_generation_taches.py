from utils.openai_client import OpenAIClient
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class AgentGenerationTaches:
    def __init__(self):
        self.client = OpenAIClient()
        
    def _valider_specification(self, specification: Dict) -> bool:
        """Valide que la spécification contient les champs requis"""
        required_fields = ['titre', 'description', 'exigences']
        return all(field in specification for field in required_fields)

    def _formater_prompt(self, specification: Dict) -> str:
        """Formate le prompt pour la génération des tâches"""
        return f"""Transforme cette spécification en une liste de tâches Markdown :
        
# Titre: {specification['titre']}
## Description: {specification['description']}
## Exigences: {', '.join(specification['exigences'])}

Génère une liste de tâches Markdown avec des cases à cocher, organisée par catégories.
Chaque tâche doit être spécifique, mesurable et réalisable.
Utilise ce format :

## [Catégorie]
- [ ] Tâche 1
- [ ] Tâche 2
"""

    def generer_taches(self, specification: Dict) -> Optional[str]:
        """Génère une liste de tâches à partir d'une spécification
        
        Args:
            specification: Dictionnaire contenant les informations de spécification
                - titre: str
                - description: str 
                - exigences: List[str]
                
        Returns:
            str: Liste de tâches au format Markdown ou None en cas d'erreur
        """
        try:
            if not self._valider_specification(specification):
                logger.error("Spécification invalide : champs manquants")
                return None
                
            prompt = self._formater_prompt(specification)
            response = self.client.generate(prompt)
            
            if not response:
                logger.error("Erreur lors de la génération des tâches")
                return None
                
            return response
            
        except Exception as e:
            logger.error(f"Erreur dans generer_taches : {str(e)}")
            return None
