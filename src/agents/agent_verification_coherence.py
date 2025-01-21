from typing import List, Dict, Optional
from src.utils.openai_client import OpenAIClient

class AgentVerificationCoherence:
    def __init__(self, client: Optional[OpenAIClient] = None):
        self.client = client if client is not None else OpenAIClient()
        
    def verify_coherence(self, specification: Dict) -> List[str]:
        """Vérifie la cohérence de la spécification complète"""
        if not specification:
            return ["La spécification est vide"]
            
        # Vérification structurelle de base
        basic_errors = self._check_basic_structure(specification)
        if basic_errors:
            return basic_errors
            
        # Analyse approfondie avec Claude
        prompt = self._create_coherence_prompt(specification)
        response = self.client.generate(prompt)
        return self._parse_coherence_response(response)

    def _check_basic_structure(self, spec: Dict) -> List[str]:
        """Vérifie la structure minimale requise"""
        errors = []
        if not spec.get("title"):
            errors.append("Titre manquant")
        if not spec.get("sections"):
            errors.append("Sections manquantes")
        return errors

    def _create_coherence_prompt(self, spec: Dict) -> str:
        """Crée le prompt pour l'analyse de cohérence"""
        return f"""Analysez cette spécification et identifiez les incohérences :
{spec}

Listez les incohérences trouvées avec des suggestions de correction, en suivant ce format :
- Incohérence : [description]
  Suggestion : [correction proposée]
"""

    def _parse_coherence_response(self, response: str) -> List[str]:
        """Parse la réponse de Claude en liste d'incohérences"""
        return [line.strip() for line in response.splitlines() if line.strip() and not line.startswith("  ")]
