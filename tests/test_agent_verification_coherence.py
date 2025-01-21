import unittest
from unittest.mock import patch, MagicMock
from src.agents.agent_verification_coherence import AgentVerificationCoherence

class TestAgentVerificationCoherence(unittest.TestCase):
    def setUp(self):
        # Création d'un mock complet pour le client OpenAI
        self.mock_client = MagicMock()
        self.agent = AgentVerificationCoherence(client=self.mock_client)

    def test_verify_coherence_empty_spec(self):
        """Teste la vérification d'une spécification vide"""
        errors = self.agent.verify_coherence({})
        self.assertEqual(errors, ["La spécification est vide"])

    def test_verify_coherence_basic_errors(self):
        """Teste la détection des erreurs structurelles de base"""
        # Spécification sans titre
        spec_no_title = {"sections": [{"title": "Section 1"}]}
        errors = self.agent.verify_coherence(spec_no_title)
        self.assertIn("Titre manquant", errors)

        # Spécification sans sections
        spec_no_sections = {"title": "Document Title"}
        errors = self.agent.verify_coherence(spec_no_sections)
        self.assertIn("Sections manquantes", errors)

    def test_verify_coherence_with_openai(self):
        """Teste l'analyse de cohérence avec OpenAI"""
        # Configuration du mock
        mock_response = """- Incohérence : Section 2 manque de détails
- Suggestion : Ajouter des spécifications techniques détaillées"""
        self.mock_client.generate.return_value = mock_response

        # Spécification de test
        spec = {
            "title": "Document Title",
            "sections": [
                {"title": "Section 1", "content": "..."},
                {"title": "Section 2", "content": "..."}
            ]
        }

        # Exécution du test
        errors = self.agent.verify_coherence(spec)
        self.assertIn("- Incohérence : Section 2 manque de détails", errors)
        self.assertIn("- Suggestion : Ajouter des spécifications techniques détaillées", errors)

if __name__ == '__main__':
    unittest.main()
