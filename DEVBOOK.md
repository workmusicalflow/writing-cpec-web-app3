## Ressources utiles

- Documentation de l'API OpenAI : https://platform.openai.com/docs/api-reference/introduction

**Dépôt distant**
https://github.com/workmusicalflow/writing-cpec-web-app3.git

## API Internes

### Client OpenAI

#### Initialisation

```python
from utils.openai_client import OpenAIClient

# Initialisation avec modèle par défaut (gpt-4o-mini)
client = OpenAIClient()

# Initialisation avec modèle spécifique
client = OpenAIClient(default_model="gpt-4o")
```

#### Méthodes principales

**generate(prompt: str, system_prompt: Optional[str] = None, model: Optional[str] = None) -> str**

- Génère une réponse à partir d'un prompt
- Paramètres :
  - `prompt`: Le prompt principal
  - `system_prompt`: Prompt système optionnel
  - `model`: Modèle à utiliser (gpt-4o-mini ou gpt-4o)
- Retourne la réponse générée

**estimate_cost(prompt: str, system_prompt: Optional[str] = None, model: Optional[str] = None) -> float**

- Estime le coût d'une génération
- Retourne le coût estimé en dollars

**get_available_models() -> List[str]**

- Retourne la liste des modèles disponibles
- Exemple : ["gpt-4o-mini", "gpt-4o"]

### Client Anthropic

#### Initialisation

```python
from utils.anthropic_client import AnthropicClient

client = AnthropicClient()
```

#### Méthodes principales

**generate(prompt: str, system_prompt: Optional[str] = None, model: Optional[str] = None) -> str**

- Génère une réponse à partir d'un prompt
- Paramètres :
  - `prompt`: Le prompt principal
  - `system_prompt`: Prompt système optionnel
  - `model`: Modèle à utiliser (claude-3-5-sonnet-20241022 par défaut)
- Retourne la réponse générée

**estimate_cost(prompt: str, system_prompt: Optional[str] = None, model: Optional[str] = None) -> float**

- Estime le coût d'une génération
- Retourne le coût estimé en dollars
