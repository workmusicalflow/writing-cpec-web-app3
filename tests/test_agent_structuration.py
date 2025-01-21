from src.agents.agent_structuration import StructurationAgent, Specification
import pytest
from unittest.mock import MagicMock

@pytest.fixture
def agent():
    mock_client = MagicMock()
    mock_client.generate.return_value = """- Améliorer la description avec plus de détails techniques
- Ajouter des exigences non fonctionnelles
- Préciser les contraintes budgétaires"""
    return StructurationAgent(client=mock_client)

@pytest.fixture
def sample_specification():
    return Specification(
        title="Test Specification",
        description="This is a test description with objectives and functionalities.",
        requirements=[
            "The system must handle 1000 requests per second",
            "The response time should be under 200ms",
            "The uptime must be 99.9%"
        ],
        constraints=[
            "The budget must not exceed $100000",
            "The project must be completed within 6 months",
            "The solution must comply with GDPR regulations"
        ]
    )

def test_analyze_specification(agent, sample_specification):
    analysis = agent.analyze_specification(sample_specification)

    assert analysis["title"] == "Test Specification"
    assert "quality_score" in analysis
    assert isinstance(analysis["quality_score"], float)
    assert 0 <= analysis["quality_score"] <= 1
    
    assert "requirements_analysis" in analysis
    assert analysis["requirements_analysis"]["count"] == 3
    assert analysis["requirements_analysis"]["specificity"] is True
    
    assert "constraints_analysis" in analysis
    assert analysis["constraints_analysis"]["count"] == 3
    assert analysis["constraints_analysis"]["has_legal"] is True
    
    assert "recommendations" in analysis
    assert isinstance(analysis["recommendations"], list)

def test_calculate_quality_score(agent):
    # Test empty description
    assert agent._calculate_quality_score("") == 0.0
    
    # Test short description
    short_desc = "This is a short description."
    assert 0 < agent._calculate_quality_score(short_desc) < 1
    
    # Test complete description
    complete_desc = "Objectif: Test. Fonctionnalité: Test. Contrainte: Test."
    assert agent._calculate_quality_score(complete_desc) == 1.0

def test_analyze_requirements(agent):
    requirements = [
        "Requirement with number 123",
        "Requirement without specific measures"
    ]
    
    analysis = agent._analyze_requirements(requirements)
    assert analysis["count"] == 2
    assert analysis["specificity"] is True

def test_analyze_constraints(agent):
    constraints = [
        "Legal constraint",
        "Budget constraint"
    ]
    
    analysis = agent._analyze_constraints(constraints)
    assert analysis["count"] == 2
    assert analysis["has_legal"] is True
