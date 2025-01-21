import gradio as gr
import logging
from utils.anthropic_client import AnthropicClient
import structlog

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

# Initialisation du client Anthropic
try:
    client = AnthropicClient()
    logger.info("Client Anthropic initialisé avec succès")
except Exception as e:
    logger.error("Erreur lors de l'initialisation du client Anthropic", error=str(e))
    raise

def process_specification(
    title: str,
    description: str,
    requirements: str,
    constraints: str
) -> str:
    """Traite une spécification avec Claude."""
    logger.info("Début du traitement de spécification", 
               title=title,
               description_length=len(description),
               requirements_count=len(requirements.split('\n')),
               constraints_count=len(constraints.split('\n')))

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

        logger.debug("Prompt généré", prompt_length=len(prompt))

        # Appel à l'API Anthropic
        response = client.generate(
            prompt=prompt,
            system_prompt="Vous êtes un expert en spécifications techniques. Fournissez des réponses structurées en Markdown.",
            model="claude-3-5-sonnet-20241022"
        )

        logger.info("Réponse reçue de l'API Anthropic",
                  response_length=len(response))

        # Formatage des résultats
        evaluation_text = f"""
        ### Résultat de l'évaluation

        {response}
        """

        logger.info("Traitement terminé avec succès")
        return evaluation_text

    except Exception as e:
        logger.error("Erreur lors du traitement de la spécification",
                   error=str(e),
                   stack_trace=e.__traceback__)
        
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
