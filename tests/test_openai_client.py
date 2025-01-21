import unittest
from unittest.mock import patch, MagicMock
from src.utils.openai_client import OpenAIClient

class TestOpenAIClient(unittest.TestCase):
    def setUp(self):
        self.client = OpenAIClient()

    @patch('os.environ.get')
    def test_missing_api_key(self, mock_env):
        """Teste la gestion d'une clé API manquante"""
        mock_env.return_value = None
        with self.assertRaises(ValueError):
            OpenAIClient()

    @patch('openai.OpenAI')
    def test_generate_success(self, mock_openai):
        """Teste la génération réussie"""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock(message=MagicMock(content="Réponse test"))]
        mock_openai.return_value.chat.completions.create.return_value = mock_response

        response = self.client.generate("Test prompt")
        self.assertEqual(response, "Réponse test")

    @patch('openai.OpenAI')
    def test_generate_error(self, mock_openai):
        """Teste la gestion des erreurs API"""
        mock_openai.return_value.chat.completions.create.side_effect = Exception("Erreur test")
        with self.assertRaises(Exception):
            self.client.generate("Test prompt")

    def test_estimate_cost(self):
        """Teste l'estimation des coûts"""
        cost = self.client.estimate_cost("Test prompt", model="gpt-4o-mini")
        self.assertGreater(cost, 0)

    def test_get_available_models(self):
        """Teste la récupération des modèles disponibles"""
        models = self.client.get_available_models()
        self.assertEqual(len(models), 2)
        self.assertIn("gpt-4o-mini", models)
        self.assertIn("gpt-4o", models)

if __name__ == '__main__':
    unittest.main()
