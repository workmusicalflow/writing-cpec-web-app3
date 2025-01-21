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
