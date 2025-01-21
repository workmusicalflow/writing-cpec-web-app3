import unittest
from unittest.mock import MagicMock
from src.agents.agent_generation_taches import AgentGenerationTaches
from src.utils.openai_client import OpenAIClient

class TestAgentGenerationTaches(unittest.TestCase):
    def setUp(self):
        self.mock_client = MagicMock(spec=OpenAIClient)
        self.mock_client.generate.return_value = """# Liste des tâches
- [ ] Créer la page d'accueil
- [ ] Implémenter le formulaire d'inscription
- [ ] Développer la page de contact"""

    def test_generation_taches(self):
        spec = {
            "titre": "Site web événementiel",
            "description": "Création d'un site web pour un événement",
            "exigences": [
                "Page d'accueil avec présentation",
                "Formulaire d'inscription",
                "Page de contact"
            ]
        }
        
        agent = AgentGenerationTaches()
        agent.client = self.mock_client
        resultat = agent.generer_taches(spec)
        
        self.mock_client.generate.assert_called_once()
        self.assertIsInstance(resultat, str)
        self.assertIn("# Liste des tâches", resultat)
        self.assertIn("- [ ] Créer la page d'accueil", resultat)
        self.assertIn("- [ ] Implémenter le formulaire d'inscription", resultat)
        self.assertIn("- [ ] Développer la page de contact", resultat)

if __name__ == '__main__':
    unittest.main()
