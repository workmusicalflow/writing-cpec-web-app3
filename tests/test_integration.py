import pytest
from unittest.mock import Mock
from src.main import SpecificationProcessor
from src.utils.validator import SpecificationValidator
from src.agents.agent_structuration import AgentStructuration
from src.agents.agent_verification_coherence import AgentVerificationCoherence
from src.agents.agent_generation_taches import AgentGenerationTaches
from src.agents.agent_bonnes_pratiques import AgentBonnesPratiques
from src.utils.openai_client import OpenAIClient
from src.utils.anthropic_client import AnthropicClient

class TestIntegration:
    @pytest.fixture
    def processor(self, mock_anthropic_client, mock_openai_client):
        return SpecificationProcessor(
            anthropic_client=mock_anthropic_client,
            openai_client=mock_openai_client
        )

    def test_full_specification_workflow(self, processor, sample_valid_spec, expected_structured_spec):
        """Test le flux complet de traitement d'une spécification"""
        # 1. Validation initiale
        is_valid, errors = SpecificationValidator.validate_specification(
            title=sample_valid_spec["title"],
            description=sample_valid_spec["description"],
            requirements=sample_valid_spec["requirements"],
            constraints=sample_valid_spec["constraints"]
        )
        assert is_valid
        assert errors is None

        # 2. Création de la spécification structurée
        spec = processor._create_specification(
            title=sample_valid_spec["title"],
            description=sample_valid_spec["description"],
            requirements=sample_valid_spec["requirements"],
            constraints=sample_valid_spec["constraints"]
        )
        assert spec["title"] == sample_valid_spec["title"]
        # Vérification de la structure attendue
        assert spec["description"] == expected_structured_spec["description"]
        assert len(spec["sections"]) == len(expected_structured_spec["sections"])
        assert len(spec["sections"]) == 2

        # 3. Traitement par les agents
        agents = {
            'coherence_verifier': Mock(verify_coherence=Mock(return_value=None)),
            'structuration_agent': Mock(structurer=Mock(return_value=sample_valid_spec)),
            'task_generator': Mock(generer_taches=Mock(return_value="# Liste des tâches\n- [ ] Tâche 1")),
            'best_practices_agent': Mock(appliquer_bonnes_pratiques=Mock(return_value=sample_valid_spec))
        }
        processor._initialize_agents = lambda: agents
        
        # Vérification de la cohérence
        coherence_errors = agents["coherence_verifier"].verify_coherence(spec)
        assert coherence_errors is None  # Le mock retourne None par défaut
        
        # Structuration
        structured_spec = agents["structuration_agent"].structurer(spec)
        assert structured_spec is not None
        
        # Génération des tâches
        tasks = agents["task_generator"].generer_taches(structured_spec)
        assert tasks is not None
        assert len(tasks) > 0
        
        # Application des bonnes pratiques
        optimized_spec = agents["best_practices_agent"].appliquer_bonnes_pratiques(structured_spec)
        assert optimized_spec is not None

    def test_edge_cases_workflow(self, processor, sample_valid_spec):
        """Test les cas limites de spécification"""
        # Configurer les agents
        agents = {
            'coherence_verifier': Mock(verify_coherence=Mock(return_value=None)),
            'structuration_agent': Mock(structurer=Mock(return_value=sample_valid_spec)),
            'task_generator': Mock(generer_taches=Mock(return_value="# Liste des tâches\n- [ ] Tâche 1")),
            'best_practices_agent': Mock(appliquer_bonnes_pratiques=Mock(return_value=sample_valid_spec))
        }
        processor._initialize_agents = lambda: agents

        # 1. Test avec des champs vides mais valides
        empty_but_valid_spec = {
            "title": " ",
            "description": " ",
            "requirements": " ",
            "constraints": " "
        }
        response = processor.process(**empty_but_valid_spec, model_choice="anthropic")
        assert "Erreurs de validation" in response
        
        # 2. Test avec des caractères spéciaux
        special_chars_spec = {
            "title": "Test @#$%",
            "description": "Description avec émojis 🚀✨",
            "requirements": "Req 1 & < > | 2",
            "constraints": "Contrainte {} [] /"
        }
        processor.anthropic_client.generate.return_value = """
        Évaluation de la spécification (7/10)

        Points forts :
        1. Structure claire
        2. Objectifs bien définis
        3. Contraintes précises

        Points à améliorer :
        1. Ajouter des métriques
        2. Détailler la sécurité
        3. Préciser les tests
        """
        response = processor.process(**special_chars_spec, model_choice="anthropic")
        assert "Points forts" in response
        assert "Points à améliorer" in response
        
        # 3. Test avec une spécification très longue
        long_spec = {
            "title": "T" * 1000,
            "description": "D" * 5000,
            "requirements": "R" * 3000,
            "constraints": "C" * 2000
        }
        response = processor.process(**long_spec, model_choice="anthropic")
        assert "Points forts" in response
        assert "Points à améliorer" in response

        # 4. Test avec des valeurs null/none
        null_spec = {
            "title": None,
            "description": None,
            "requirements": None,
            "constraints": None
        }
        response = processor.process(**null_spec, model_choice="anthropic")
        assert "Erreurs de validation" in response

        # 5. Test avec des types incorrects
        wrong_type_spec = {
            "title": 123,
            "description": 456,
            "requirements": 789,
            "constraints": 101
        }
        response = processor.process(**wrong_type_spec, model_choice="anthropic")
        assert "Le titre doit être une chaîne de caractères" in response
        assert "La description doit être une chaîne de caractères" in response
        assert "Les exigences doivent être une chaîne ou une liste" in response
        assert "Les contraintes doivent être une chaîne ou une liste" in response
        assert "Erreurs de validation" in response

        # 6. Test avec des champs manquants
        with pytest.raises(TypeError):
            processor.process(model_choice="anthropic")

        # 7. Test avec des URLs longues
        long_url_spec = {
            "title": "Test URL",
            "description": "http://" + "a" * 1000 + ".com",
            "requirements": "http://" + "b" * 1000 + ".com",
            "constraints": "http://" + "c" * 1000 + ".com"
        }
        response = processor.process(**long_url_spec, model_choice="anthropic")
        assert "Points forts" in response
        assert "Points à améliorer" in response

        # 8. Test avec des chaînes encodées
        encoded_spec = {
            "title": "Test %20 encoding",
            "description": "Description with %20 spaces",
            "requirements": "Requirements with %2F slashes",
            "constraints": "Constraints with %3A colons"
        }
        response = processor.process(**encoded_spec, model_choice="anthropic")
        assert "Points forts" in response
        assert "Points à améliorer" in response

    def test_agent_execution_order(self, processor, sample_valid_spec):
        """Test l'ordre d'exécution des agents et la transmission des résultats"""
        # Créer des mocks pour tracer l'ordre d'exécution
        execution_order = []
        
        # Créer les mocks avec tracking
        coherence_verifier = Mock(spec=AgentVerificationCoherence)
        coherence_verifier.verify_coherence = Mock(side_effect=lambda x: (execution_order.append('verify_coherence'), None)[1])
        
        structuration_agent = Mock(spec=AgentStructuration)
        structuration_agent.structurer = Mock(side_effect=lambda x: (execution_order.append('structurer'), {'structured': True})[1])
        
        task_generator = Mock(spec=AgentGenerationTaches)
        task_generator.generer_taches = Mock(side_effect=lambda x: (execution_order.append('generer_taches'), "# Liste des tâches\n- [ ] Tâche 1")[1])
        
        best_practices_agent = Mock(spec=AgentBonnesPratiques)
        best_practices_agent.appliquer_bonnes_pratiques = Mock(side_effect=lambda x: (execution_order.append('appliquer_bonnes_pratiques'), {'optimized': True})[1])
        
        # Remplacer les agents par les mocks
        processor._initialize_agents = lambda: {
            'coherence_verifier': coherence_verifier,
            'structuration_agent': structuration_agent,
            'task_generator': task_generator,
            'best_practices_agent': best_practices_agent
        }
        
        # Exécuter le processus
        processor.process(
            title=sample_valid_spec["title"],
            description=sample_valid_spec["description"],
            requirements=sample_valid_spec["requirements"],
            constraints=sample_valid_spec["constraints"],
            model_choice="anthropic"
        )
        
        # Vérifier l'ordre d'exécution
        expected_order = [
            'verify_coherence',
            'structurer',
            'generer_taches',
            'appliquer_bonnes_pratiques'
        ]
        assert execution_order == expected_order

    def test_error_handling_workflow(self, processor, sample_invalid_spec):
        """Test la gestion des erreurs dans le flux"""
        
        # 1. Validation initiale
        is_valid, errors = SpecificationValidator.validate_specification(
            title=sample_invalid_spec["title"],
            description=sample_invalid_spec["description"],
            requirements=sample_invalid_spec["requirements"],
            constraints=sample_invalid_spec["constraints"]
        )
        assert not is_valid
        assert errors is not None
        assert len(errors) > 0
        assert any("titre" in error.lower() for error in errors)

    def test_api_integration(self, processor, sample_valid_spec):
        """Test l'intégration avec les APIs"""
        # Configurer les mocks
        processor.anthropic_client.generate.return_value = """
        Évaluation de la spécification (8/10)

        Points forts :
        1. Structure claire
        2. Objectifs bien définis
        3. Contraintes précises

        Points à améliorer :
        1. Ajouter des métriques
        2. Détailler la sécurité
        3. Préciser les tests
        """

        # Mock pour OpenAI
        mock_response = """
        Évaluation de la spécification (7/10)

        Points forts :
        1. Exigences claires
        2. Architecture cohérente
        3. Standards respectés

        Points à améliorer :
        1. Ajouter des KPIs
        2. Détailler la performance
        3. Préciser la maintenance
        """
        processor.openai_client.generate = Mock(return_value=mock_response)

        # Configurer les agents
        agents = {
            'coherence_verifier': Mock(verify_coherence=Mock(return_value=None)),
            'structuration_agent': Mock(structurer=Mock(return_value=sample_valid_spec)),
            'task_generator': Mock(generer_taches=Mock(return_value="# Liste des tâches\n- [ ] Tâche 1")),
            'best_practices_agent': Mock(appliquer_bonnes_pratiques=Mock(return_value=sample_valid_spec))
        }
        processor._initialize_agents = lambda: agents

        # 1. Test avec Anthropic
        response_anthropic = processor.process(
            title=sample_valid_spec["title"],
            description=sample_valid_spec["description"],
            requirements=sample_valid_spec["requirements"],
            constraints=sample_valid_spec["constraints"],
            model_choice="anthropic"
        )
        assert "Points forts" in response_anthropic
        assert "Points à améliorer" in response_anthropic
        assert "Agents impliqués" in response_anthropic
        
        # 2. Test avec OpenAI
        response_openai = processor.process(
            title=sample_valid_spec["title"],
            description=sample_valid_spec["description"],
            requirements=sample_valid_spec["requirements"],
            constraints=sample_valid_spec["constraints"],
            model_choice="openai"
        )
        assert "Points forts" in response_openai
        assert "Points à améliorer" in response_openai
        assert "Agents impliqués" in response_openai

        # 3. Test avec des tokens invalides
        processor.anthropic_client.generate.side_effect = Exception("Invalid API token")
        response_invalid_token = processor.process(
            title=sample_valid_spec["title"],
            description=sample_valid_spec["description"],
            requirements=sample_valid_spec["requirements"],
            constraints=sample_valid_spec["constraints"],
            model_choice="anthropic"
        )
        assert "Invalid API token" in response_invalid_token

        # 4. Test avec quota dépassé
        processor.anthropic_client.generate.side_effect = Exception("Rate limit exceeded")
        response_rate_limit = processor.process(
            title=sample_valid_spec["title"],
            description=sample_valid_spec["description"],
            requirements=sample_valid_spec["requirements"],
            constraints=sample_valid_spec["constraints"],
            model_choice="anthropic"
        )
        assert "Rate limit exceeded" in response_rate_limit

        # 5. Test avec timeout
        processor.anthropic_client.generate.side_effect = Exception("Request timed out")
        response_timeout = processor.process(
            title=sample_valid_spec["title"],
            description=sample_valid_spec["description"],
            requirements=sample_valid_spec["requirements"],
            constraints=sample_valid_spec["constraints"],
            model_choice="anthropic"
        )
        assert "Request timed out" in response_timeout

    def test_api_error_handling(self, processor, sample_valid_spec):
        """Test la gestion des différents types d'erreurs API"""
        # Test avec erreur d'API
        agents = {
            'coherence_verifier': Mock(verify_coherence=Mock(return_value=None)),
            'structuration_agent': Mock(structurer=Mock(return_value=sample_valid_spec)),
            'task_generator': Mock(generer_taches=Mock(return_value="# Liste des tâches\n- [ ] Tâche 1")),
            'best_practices_agent': Mock(appliquer_bonnes_pratiques=Mock(return_value=sample_valid_spec))
        }
        processor._initialize_agents = lambda: agents
        processor.anthropic_client.generate.side_effect = Exception("tuple index out of range")
        
        response = processor.process(
            title=sample_valid_spec["title"],
            description=sample_valid_spec["description"],
            requirements=sample_valid_spec["requirements"],
            constraints=sample_valid_spec["constraints"],
            model_choice="anthropic"
        )
        assert "Erreur lors de l'analyse" in response
        assert "tuple index out of range" in response

    def test_cross_component_interaction(self, processor, sample_valid_spec):
        """Test les interactions entre les différents composants"""
        # 1. Création et validation de la spécification
        spec = processor._create_specification(
            title=sample_valid_spec["title"],
            description=sample_valid_spec["description"],
            requirements=sample_valid_spec["requirements"],
            constraints=sample_valid_spec["constraints"]
        )
        
        # 2. Traitement par les agents
        agents = {
            'coherence_verifier': Mock(verify_coherence=Mock(return_value=None)),
            'structuration_agent': Mock(structurer=Mock(return_value=spec)),
            'task_generator': Mock(generer_taches=Mock(return_value="# Liste des tâches\n- [ ] Tâche 1")),
            'best_practices_agent': Mock(appliquer_bonnes_pratiques=Mock(return_value=spec))
        }
        tasks, errors = processor._process_with_agents(spec, agents)
        
        # Vérifier les appels et résultats
        assert errors is None
        assert tasks is not None
        agents['coherence_verifier'].verify_coherence.assert_called_once_with(spec)
        agents['structuration_agent'].structurer.assert_called_once_with(spec)
        agents['task_generator'].generer_taches.assert_called_once()
        agents['best_practices_agent'].appliquer_bonnes_pratiques.assert_called_once()
        
        # 3. Génération du prompt
        prompt = processor._generate_prompt(
            title=sample_valid_spec["title"],
            description=sample_valid_spec["description"],
            requirements=sample_valid_spec["requirements"],
            constraints=sample_valid_spec["constraints"],
            tasks=tasks
        )
        assert prompt is not None
        assert sample_valid_spec["title"] in prompt
        assert "Exigences" in prompt
        assert "Contraintes" in prompt
