import pytest
from src.agents.agent_structuration import StructureAgent
from unittest.mock import patch

class TestStructureAgent:
    @pytest.fixture
    def agent(self):
        return StructureAgent()

    def test_validate_input_valid(self, agent):
        """Teste la validation d'une entrée valide"""
        assert agent.validate_input("Description de projet valide") is True

    def test_validate_input_invalid(self, agent):
        """Teste la validation d'une entrée invalide"""
        assert agent.validate_input("") is False
        assert agent.validate_input(123) is False

    @patch('openai.ChatCompletion.create')
    def test_generate_structure_success(self, mock_openai, agent):
        """Teste la génération de structure avec succès"""
        mock_openai.return_value = {
            'choices': [
                {
                    'message': {
                        'content': "Titre: Contenu"
                    }
                }
            ],
            'usage': {
                'total_tokens': 100
            }
        }
        
        result = agent.generate_structure("Description de projet")
        assert isinstance(result, dict)
        assert "sections" in result
        assert len(result["sections"]) > 0

    def test_generate_structure_invalid_input(self, agent):
        """Teste la génération avec une entrée invalide"""
        with pytest.raises(ValueError):
            agent.generate_structure("")

    @patch('openai.ChatCompletion.create')
    def test_generate_structure_api_error(self, mock_openai, agent):
        """Teste la gestion des erreurs de l'API"""
        mock_openai.side_effect = Exception("API Error")
        
        with pytest.raises(RuntimeError):
            agent.generate_structure("Description valide")

    def test_format_output(self, agent):
        """Teste le formatage de la sortie"""
        raw_output = "Titre1: Contenu1\n\nTitre2: Contenu2"
        result = agent.format_output(raw_output)
        
        assert len(result["sections"]) == 2
        assert result["sections"][0]["title"] == "Titre1"
        assert result["sections"][0]["content"] == "Contenu1"
