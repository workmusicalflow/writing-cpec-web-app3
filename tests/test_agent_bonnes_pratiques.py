from src.agents.agent_bonnes_pratiques import BonnesPratiquesAgent
import pytest

@pytest.fixture
def agent():
    return BonnesPratiquesAgent()

def test_recherche_bonnes_pratiques(agent):
    # Test avec une spécification simple
    spec = {
        "domaine": "sécurité",
        "technologies": ["React", "Node.js"],
        "contraintes": ["GDPR"]
    }
    
    resultats = agent.rechercher(spec)
    
    assert isinstance(resultats, list)
    assert len(resultats) > 0
    for pratique in resultats:
        assert "titre" in pratique
        assert "description" in pratique
        assert "source" in pratique

def test_filtrage_par_technologie(agent):
    spec = {
        "domaine": "performance",
        "technologies": ["React"],
        "contraintes": []
    }
    
    resultats = agent.rechercher(spec)
    
    # Vérifie que les bonnes pratiques sont pertinentes pour React
    assert all("React" in pratique["technologies"] for pratique in resultats)

def test_priorisation_bonnes_pratiques(agent):
    spec = {
        "domaine": "sécurité",
        "technologies": ["Node.js"],
        "contraintes": ["GDPR"]
    }
    
    resultats = agent.rechercher(spec)
    
    # Vérifie que les pratiques liées à la sécurité et GDPR sont prioritaires
    assert any("GDPR" in pratique["tags"] for pratique in resultats[:3])

def test_recherche_python(agent):
    spec = {
        "domaine": "maintenance",
        "technologies": ["Python"],
        "contraintes": []
    }
    
    resultats = agent.rechercher(spec)
    
    assert len(resultats) > 0
    assert all("Python" in pratique["technologies"] for pratique in resultats)

def test_recherche_java(agent):
    spec = {
        "domaine": "performance",
        "technologies": ["Java"],
        "contraintes": []
    }
    
    resultats = agent.rechercher(spec)
    
    assert len(resultats) > 0
    assert all("Java" in pratique["technologies"] for pratique in resultats)

def test_recherche_react(agent):
    spec = {
        "domaine": "architecture",
        "technologies": ["React"],
        "contraintes": []
    }
    
    resultats = agent.rechercher(spec)
    
    assert len(resultats) > 0
    assert all("React" in pratique["technologies"] for pratique in resultats)

def test_recherche_php_securite(agent):
    spec = {
        "domaine": "sécurité",
        "technologies": ["PHP"],
        "contraintes": ["OWASP"]
    }
    
    resultats = agent.rechercher(spec)
    
    assert len(resultats) > 0
    assert all("PHP" in pratique["technologies"] for pratique in resultats)
    assert any("OWASP" in pratique["tags"] for pratique in resultats)

def test_recherche_php_performance(agent):
    spec = {
        "domaine": "performance",
        "technologies": ["PHP"],
        "contraintes": []
    }
    
    resultats = agent.rechercher(spec)
    
    assert len(resultats) > 0
    assert all("PHP" in pratique["technologies"] for pratique in resultats)
    assert any("caching" in pratique["tags"] for pratique in resultats)

def test_recherche_poo_architecture(agent):
    spec = {
        "domaine": "architecture",
        "technologies": ["Java", "Python", "PHP"],
        "contraintes": ["POO"]
    }
    
    resultats = agent.rechercher(spec)
    
    assert len(resultats) > 0
    assert any("POO" in pratique["tags"] for pratique in resultats)
    assert any("SOLID" in pratique["tags"] for pratique in resultats)

def test_recherche_poo_qualite(agent):
    spec = {
        "domaine": "qualité",
        "technologies": ["Java", "Python", "PHP"],
        "contraintes": ["encapsulation"]
    }
    
    resultats = agent.rechercher(spec)
    
    assert len(resultats) > 0
    assert any("POO" in pratique["tags"] for pratique in resultats)
    assert any("encapsulation" in pratique["tags"] for pratique in resultats)

def test_recherche_typescript(agent):
    spec = {
        "domaine": "qualité",
        "technologies": ["TypeScript"],
        "contraintes": ["typage"]
    }
    
    resultats = agent.rechercher(spec)
    
    assert len(resultats) > 0
    assert all("TypeScript" in pratique["technologies"] for pratique in resultats)
    assert any("strict mode" in pratique["description"].lower() for pratique in resultats)

def test_recherche_go(agent):
    spec = {
        "domaine": "performance",
        "technologies": ["Go"],
        "contraintes": ["concurrency"]
    }
    
    resultats = agent.rechercher(spec)
    
    assert len(resultats) > 0
    assert all("Go" in pratique["technologies"] for pratique in resultats)
    assert any("goroutines" in pratique["description"].lower() for pratique in resultats)

def test_recherche_rust(agent):
    spec = {
        "domaine": "sécurité",
        "technologies": ["Rust"],
        "contraintes": ["memory"]
    }
    
    resultats = agent.rechercher(spec)
    
    assert len(resultats) > 0
    assert all("Rust" in pratique["technologies"] for pratique in resultats)
    assert any("propriété" in pratique["description"].lower() for pratique in resultats)

def test_recherche_kotlin(agent):
    spec = {
        "domaine": "qualité",
        "technologies": ["Kotlin"],
        "contraintes": ["null safety"]
    }
    
    resultats = agent.rechercher(spec)
    
    assert len(resultats) > 0
    assert all("Kotlin" in pratique["technologies"] for pratique in resultats)
    assert any("nullable" in pratique["description"].lower() for pratique in resultats)

def test_recherche_swift(agent):
    spec = {
        "domaine": "performance",
        "technologies": ["Swift"],
        "contraintes": ["memory"]
    }
    
    resultats = agent.rechercher(spec)
    
    assert len(resultats) > 0
    assert all("Swift" in pratique["technologies"] for pratique in resultats)
    assert any("arc" in pratique["description"].lower() for pratique in resultats)
