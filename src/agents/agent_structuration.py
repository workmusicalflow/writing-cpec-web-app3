from typing import Dict, List
import openai
from src.utils.anthropic_client import AnthropicClient
from datetime import datetime

class StructureAgent:
    """
    Agent de structuration initiale pour les spécifications techniques
    
    Cet agent utilise GPT-3.5-turbo pour générer une structure de base
    à partir d'une description de projet.
    
    Exemple d'utilisation :
    ```python
    agent = StructureAgent()
    structure = agent.generate_structure("Description du projet")
    ```
    
    Attributes:
        model (str): Modèle GPT utilisé (gpt-3.5-turbo)
        temperature (float): Créativité des réponses (0.0 à 1.0)
        max_tokens (int): Nombre maximum de tokens générés
        system_prompt (str): Prompt système pour guider le modèle
    """
    def __init__(self):
        """Initialise l'agent de structuration"""
        self.model = "gpt-3.5-turbo"
        self.temperature = 0.7
        self.max_tokens = 1000
        self.system_prompt = """
        Vous êtes un expert en création de structures de spécifications techniques.
        Votre rôle est de générer une structure de base pour des documents de spécifications
        à partir d'une brève description de projet.
        """

    def validate_input(self, project_description: str) -> bool:
        """Valide la description du projet"""
        if not isinstance(project_description, str):
            return False
        return len(project_description.strip()) > 10

    def generate_structure(self, project_description: str) -> Dict:
        """Génère la structure de spécification"""
        if not self.validate_input(project_description):
            raise ValueError("Description de projet invalide")

        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": project_description}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            return self.format_output(response.choices[0].message.content)
            
        except Exception as e:
            raise RuntimeError(f"Erreur lors de la génération de structure : {str(e)}")

    def format_output(self, raw_output: str) -> Dict:
        """Formate la sortie en structure standardisée"""
        sections = raw_output.split("\n\n")
        structured_output = {
            "version": "1.0",
            "sections": [],
            "metadata": {
                "model": self.model,
                "timestamp": datetime.now().isoformat()
            }
        }
        
        for section in sections:
            if ":" in section:
                title, content = section.split(":", 1)
                structured_output["sections"].append({
                    "title": title.strip(),
                    "content": content.strip()
                })
        
        return structured_output

    def __str__(self):
        return f"StructureAgent(model={self.model})"
