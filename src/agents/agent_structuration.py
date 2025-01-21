from typing import Dict, List
from dataclasses import dataclass
import structlog

logger = structlog.get_logger(__name__)

@dataclass
class Specification:
    title: str
    description: str
    requirements: List[str]
    constraints: List[str]

class StructurationAgent:
    def __init__(self):
        self.logger = logger.bind(agent="structuration")
        
    def analyze_specification(self, spec: Specification) -> Dict:
        """Analyse une spécification technique et retourne un rapport structuré"""
        self.logger.info("Analyzing specification", title=spec.title)
        
        analysis = {
            "title": spec.title,
            "quality_score": self._calculate_quality_score(spec.description),
            "requirements_analysis": self._analyze_requirements(spec.requirements),
            "constraints_analysis": self._analyze_constraints(spec.constraints),
            "recommendations": self._generate_recommendations(spec)
        }
        
        self.logger.info("Specification analysis completed", title=spec.title)
        return analysis

    def _calculate_quality_score(self, description: str) -> float:
        """Calcule un score de qualité combinant clarté et complétude"""
        if not description:
            return 0.0
            
        # Score de clarté basé sur la longueur des phrases
        sentences = [s.strip() for s in description.split('.') if s.strip()]
        avg_sentence_length = sum(len(s.split()) for s in sentences) / len(sentences) if sentences else 0
        clarity = 1.0 if avg_sentence_length <= 15 else 0.5
        
        # Score de complétude basé sur les sections clés
        sections = {'objectif', 'fonctionnalité', 'contrainte'}
        completeness = min(1.0, sum(0.5 for section in sections if section in description.lower()))
        
        return (clarity * 0.6) + (completeness * 0.4)
        
    def _analyze_requirements(self, requirements: List[str]) -> Dict:
        """Analyse la liste des exigences"""
        return {
            "count": len(requirements),
            "specificity": any(char.isdigit() for r in requirements for char in r)
        }

    def _analyze_constraints(self, constraints: List[str]) -> Dict:
        """Analyse la liste des contraintes"""
        return {
            "count": len(constraints),
            "has_legal": any(
                any(term in c.lower() for term in ['legal', 'regulation', 'gdpr', 'compliance', 'légal', 'réglementation'])
                for c in constraints
            )
        }

    def _generate_recommendations(self, spec: Specification) -> List[str]:
        """Génère des recommandations d'amélioration"""
        recommendations = []
        
        if len(spec.description) < 100:
            recommendations.append("Enrichir la description avec plus de détails")
            
        if len(spec.requirements) < 3:
            recommendations.append("Ajouter plus d'exigences fonctionnelles")
            
        return recommendations
