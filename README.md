# Specification Redactor and Optimiser Agent AI

## Description du projet

Ce projet vise à créer un agent IA capable de :

1. Évaluer des spécifications techniques
2. Identifier les points forts et faibles
3. Proposer des améliorations
4. Générer des recommandations structurées

## Fonctionnalités principales

- Interface utilisateur intuitive via Gradio
- Intégration avec l'API Anthropic (Claude 3.5 Sonnet)
- Gestion robuste des erreurs
- Logging détaillé pour le débogage
- Structure de code modulaire

## Architecture technique

```
src/
├── main.py                # Application principale
├── agents/
│   ├── agent_structuration.py  # Agent de structuration
├── utils/
│   ├── anthropic_client.py     # Client Anthropic
```

## Dépendances

- openai>=1.0.0
- pytest>=8.0.0
- python-dotenv>=1.0.0
- anthropic>=0.3.0
- structlog>=23.1.0

## Installation

1. Cloner le dépôt
2. Créer un environnement virtuel :

```bash
python -m venv venv
source venv/bin/activate
```

3. Installer les dépendances :

```bash
pip install -r requirements.txt
```

4. Configurer les variables d'environnement :

```bash
echo "ANTHROPIC_API_KEY=votre_clé_api" > .env
```

5. Lancer l'application :

```bash
python src/main.py
```

## Utilisation

1. Remplir les champs du formulaire :
   - Titre
   - Description
   - Exigences
   - Contraintes
2. Cliquer sur "Évaluer"
3. Consulter les résultats dans le panneau de droite

## Journalisation

Le système utilise structlog pour une journalisation détaillée :

- Niveau INFO pour les opérations principales
- Niveau DEBUG pour le suivi détaillé
- Niveau ERROR pour les erreurs critiques

Les logs sont formatés en JSON pour une intégration facile avec des systèmes de monitoring.

## Tests

Le projet inclut des tests unitaires :

- Validation des entrées
- Gestion des erreurs
- Intégration avec l'API Anthropic

Pour exécuter les tests :

```bash
pytest tests/
```

## Prochaines étapes prioritaires

1. Implémenter l'agent de structuration initiale
2. Développer l'intégration avec l'API OpenAI
3. Créer des tests unitaires pour les nouveaux composants
4. Améliorer la gestion des erreurs et le logging
5. Documenter les API internes

## Priorisation des tâches

### Méthode MoSCoW

- **Must have** : Fonctionnalités essentielles
- **Should have** : Fonctionnalités importantes mais non critiques
- **Could have** : Fonctionnalités souhaitables
- **Won't have** : Fonctionnalités exclues pour cette version

### Méthode WSJF (Weighted Shortest Job First)

1. Calculer la valeur métier
2. Évaluer le time-to-market
3. Estimer la réduction de risque
4. Calculer le coût du délai
5. Prioriser les tâches avec le ratio WSJF le plus élevé

## Contribution

1. Créer une nouvelle branche :

```bash
git checkout -b feature/nouvelle-fonctionnalite
```

2. Implémenter les modifications
3. Ajouter des tests unitaires
4. Soumettre une pull request

## Documentation complète

Consultez le [DEVBOOK.md](DEVBOOK.md) pour une documentation technique détaillée.

## Licence

MIT License - Voir le fichier [LICENSE](LICENSE) pour plus de détails.
