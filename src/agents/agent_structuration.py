from typing import Dict, List
from dataclasses import dataclass
import structlog
from utils.openai_client import OpenAIClient

logger = structlog.get_logger(__name__)

@dataclass
class Specification:
    title: str
    description: str
    requirements: List[str]
    constraints: List[str]

class StructurationAgent:
    def __init__(self, client: OpenAIClient = None):
        self.logger = logger.bind(agent="structuration")
        self.client = client or OpenAIClient(model="gpt-4o-mini")
        
    def analyze_specification(self, spec: Specification) -> Dict:
        """Analyse une spécification technique et retourne un rapport structuré"""
        self.logger.info("Analyzing specification", title=spec.title)
        
        prompt = f"""
        Analyse cette spécification technique et génère un rapport structuré :
        Titre : {spec.title}
        Description : {spec.description}
        Exigences : {', '.join(spec.requirements)}
        Contraintes : {', '.join(spec.constraints)}
        
        Format de réponse attendu (JSON) :
        {{
            "title": "Titre de la spécification",
            "quality_score": "Score de qualité entre 0 et 1",
            "requirements_analysis": {{
                "count": "Nombre d'exigences",
                "specificity": "Niveau de spécificité (basé sur la présence de chiffres)"
            }},
            "constraints_analysis": {{
                "count": "Nombre de contraintes",
                "has_legal": "Présence de contraintes légales"
            }},
            "recommendations": ["Liste des recommandations d'amélioration"]
        }}
        """
        
        response = self.client.generate(prompt)
        return response
