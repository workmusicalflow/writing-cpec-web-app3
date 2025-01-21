from typing import Dict, List
import structlog
from src.utils.openai_client import OpenAIClient

logger = structlog.get_logger(__name__)

class BonnesPratiquesAgent:
    def __init__(self, client: OpenAIClient = None):
        self.logger = logger.bind(agent="bonnes_pratiques")
        self.client = client or OpenAIClient()

    def rechercher(self, spec: Dict) -> List[Dict]:
        """Recherche des bonnes pratiques correspondant à la spécification"""
        self.logger.info("Recherche de bonnes pratiques", spec=spec)
        
        prompt = f"""
        En tant qu'expert en bonnes pratiques de développement logiciel, recommande des bonnes pratiques pour :
        - Technologies : {', '.join(spec['technologies'])}
        - Domaine : {spec['domaine']}
        - Contraintes : {', '.join(spec['contraintes']) if spec['contraintes'] else 'Aucune'}
        
        Format de réponse attendu (JSON) :
        {{
            "pratiques": [
                {{
                    "titre": "Titre de la bonne pratique",
                    "description": "Description détaillée",
                    "technologies": ["liste", "des", "technologies"],
                    "domaines": ["liste", "des", "domaines"],
                    "tags": ["liste", "des", "tags"],
                    "source": "Source de la bonne pratique"
                }}
            ]
        }}
        """
        
        response = self.client.generate(prompt, model="gpt-4")
        try:
            resultats = response["pratiques"]
            self.logger.info("Bonnes pratiques trouvées", count=len(resultats))
            return resultats
        except (KeyError, TypeError) as e:
            self.logger.error("Erreur lors de la récupération des bonnes pratiques", error=str(e))
            return []
