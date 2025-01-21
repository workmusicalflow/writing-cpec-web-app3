# Specification Redactor and Optimiser Agent AI

Données exemple workflow de départ

# Evaluator-Optimizer Workflow

## `main.py` File Content

```python
import gradio as gr
from utils.anthropic_client import AnthropicClient

# Initialisation du client Anthropic
client = AnthropicClient()

def process_specification(
    title: str,
    description: str,
    requirements: str,
    constraints: str
) -> str:
    """Traite une spécification avec Claude."""
    try:
        # Création du prompt
        prompt = f"""
        Vous êtes un expert en rédaction de spécifications techniques.
        Voici une spécification à évaluer et optimiser :

        Titre : {title}
        Description : {description}
        Exigences : {requirements}
        Contraintes : {constraints}

        1. Évaluez cette spécification sur 10 points
        2. Identifiez 3 points forts
        3. Identifiez 3 points à améliorer
        4. Proposez une version améliorée
        """

        # Appel à l'API Anthropic
        response = client.generate(
            prompt=prompt,
            system_prompt="Vous êtes un expert en spécifications techniques. Fournissez des réponses structurées en Markdown.",
            model="claude-3-5-sonnet-20241022"
        )

        # Formatage des résultats
        evaluation_text = f"""
        ### Résultat de l'évaluation

        {response}
        """

        return evaluation_text

    except Exception as e:
        error_text = f"""
        ### Erreur lors du traitement

        Une erreur s'est produite lors de l'analyse de votre spécification :
        - {str(e)}

        Veuillez vérifier vos entrées et réessayer.
        """
        return error_text

# Création de l'interface Gradio
with gr.Blocks(title="Évaluateur de Spécifications", theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # Évaluateur de Spécifications

    Cet outil vous aide à évaluer vos spécifications techniques.
    Remplissez le formulaire ci-dessous pour commencer.
    """)

    with gr.Row():
        with gr.Column():
            title_input = gr.Textbox(
                label="Titre",
                placeholder="Entrez le titre de votre spécification"
            )
            description_input = gr.Textbox(
                label="Description",
                placeholder="Décrivez votre projet en détail",
                lines=5
            )
            requirements_input = gr.Textbox(
                label="Exigences",
                placeholder="Entrez une exigence par ligne",
                lines=5
            )
            constraints_input = gr.Textbox(
                label="Contraintes",
                placeholder="Entrez une contrainte par ligne",
                lines=5
            )
            submit_btn = gr.Button("Évaluer", variant="primary")

        with gr.Column():
            evaluation_output = gr.Markdown(label="Résultats de l'Évaluation")
            with gr.Accordion("Options", open=False):
                copy_btn = gr.Button("📋 Copier les résultats", variant="secondary")
                copy_btn.click(
                    None,
                    inputs=evaluation_output,
                    js="(text) => navigator.clipboard.writeText(text)"
                )

    submit_btn.click(
        fn=process_specification,
        inputs=[
            title_input,
            description_input,
            requirements_input,
            constraints_input
        ],
        outputs=evaluation_output
    )

if __name__ == "__main__":
    demo.launch(show_api=False)

```

## `AnthropicClient.py` File Content

```python
from anthropic import Anthropic
import os
from typing import Optional

class AnthropicClient:
    def __init__(self):
        self.client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
        self.default_model = "claude-3-5-sonnet-20241022"

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        model: Optional[str] = None
    ) -> str:
        """
        Génère une réponse à partir du modèle Claude.

        Args:
        prompt: Le prompt principal
        system_prompt: Le prompt système optionnel
        model: Le modèle à utiliser (utilise le modèle par défaut si non spécifié)

        Returns:
        La réponse générée par le modèle
        """
        messages = [{
            "role": "user",
            "content": prompt
        }]

        response = self.client.messages.create(
            model=model or self.default_model,
            messages=messages,
            system=system_prompt,
            max_tokens=4096
        )

        return response.content[0].text
```

# DEVBOOK.md

## Agents IA pour l'optimisation du workflow

### 1. Agent de structuration initiale

- **Objectif** : Générer une structure de base pour la spécification
- **Entrée** : Brève description du projet
- **Sortie** : Structure de spécification avec sections prédéfinies
- **Modèle** : GPT-3.5-turbo

### 2. Agent de recherche de bonnes pratiques

- **Objectif** : Suggérer des bonnes pratiques spécifiques au domaine
- **Entrée** : Domaine du projet
- **Sortie** : Liste de bonnes pratiques pertinentes
- **API** : Semantic Scholar
- **Modèle** : Claude-3-5-sonnet

### 3. Agent de vérification de cohérence

- **Objectif** : Vérifier la cohérence interne de la spécification
- **Entrée** : Spécification complète
- **Sortie** : Liste d'incohérences et suggestions de corrections
- **Modèle** : Claude-3-5-sonnet

### 4. Agent de génération de tâches

- **Objectif** : Créer une liste de tâches de développement
- **Entrée** : Spécification complète
- **Sortie** : Liste de tâches au format Markdown
- **Modèle** : Claude-3-5-sonnet

### 5. Agent de comparaison avec des exemples

- **Objectif** : Comparer la spécification à des exemples de bonnes pratiques
- **Entrée** : Spécification complète et domaine du projet
- **Sortie** : Analyse comparative et suggestions d'améliorations
- **Base de données** : Collection d'exemples de spécifications
- **Modèle** : Claude-3-5-sonnet

## Workflow d'évaluation et d'amélioration

1. Utiliser l'agent de structuration initiale pour créer un squelette de spécification
2. Appliquer l'agent de recherche de bonnes pratiques pour enrichir la spécification
3. Rédiger la spécification détaillée
4. Utiliser l'agent de vérification de cohérence pour identifier les problèmes potentiels
5. Appliquer l'agent de comparaison avec des exemples pour améliorer la qualité
6. Utiliser l'agent de génération de tâches pour créer une liste de tâches initiale
7. Appliquer la méthode MoSCoW pour catégoriser les tâches
8. Utiliser la méthode WSJF pour prioriser les tâches

## Intégration dans le processus de développement

1. Créer des endpoints API pour chaque agent
2. Développer des composants Gradio pour chaque fonctionnalité
3. Implémenter un système de workflow pour enchaîner les agents
4. Ajouter une fonctionnalité permettant aux utilisateurs de choisir les agents à utiliser

## Suivi et amélioration continue

- Mettre en place des métriques pour évaluer l'efficacité du workflow
- Organiser des rétrospectives régulières pour identifier les axes d'amélioration
- Mettre à jour le [DEVBOOK.md](http://devbook.md/) en fonction des retours d'expérience de l'équipe
