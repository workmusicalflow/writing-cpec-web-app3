from typing import Dict, List
import structlog

logger = structlog.get_logger(__name__)

class BonnesPratiquesAgent:
    def __init__(self):
        self.logger = logger.bind(agent="bonnes_pratiques")
        # Base de données minimale de bonnes pratiques
        self.pratiques = [
            # Node.js
            {
                "titre": "Validation des entrées utilisateur",
                "description": "Toujours valider et assainir les entrées utilisateur côté serveur",
                "technologies": ["Node.js", "Express"],
                "domaines": ["sécurité"],
                "tags": ["XSS", "injection"],
                "source": "OWASP"
            },
            {
                "titre": "Gestion des erreurs",
                "description": "Implémenter une gestion centralisée des erreurs",
                "technologies": ["Node.js"],
                "domaines": ["maintenance", "fiabilité"],
                "tags": [],
                "source": "Node.js Best Practices"
            },
            {
                "titre": "Protection des données",
                "description": "Chiffrer les données sensibles et respecter le GDPR",
                "technologies": ["Node.js"],
                "domaines": ["sécurité"],
                "tags": ["GDPR", "chiffrement"],
                "source": "GDPR Guidelines"
            },
            
            # Python
            {
                "titre": "Gestion des dépendances",
                "description": "Utiliser un environnement virtuel et un fichier requirements.txt",
                "technologies": ["Python"],
                "domaines": ["maintenance"],
                "tags": ["pip", "virtualenv"],
                "source": "Python Packaging"
            },
            {
                "titre": "Typage statique",
                "description": "Utiliser les type hints pour améliorer la maintenabilité",
                "technologies": ["Python"],
                "domaines": ["qualité"],
                "tags": ["mypy"],
                "source": "PEP 484"
            },
            
            # Java
            {
                "titre": "Gestion des exceptions",
                "description": "Toujours logger les exceptions avec un contexte",
                "technologies": ["Java"],
                "domaines": ["fiabilité"],
                "tags": ["logging"],
                "source": "Effective Java"
            },
            {
                "titre": "Concurrence",
                "description": "Utiliser les ExecutorService pour gérer les threads",
                "technologies": ["Java"],
                "domaines": ["performance"],
                "tags": ["multithreading"],
                "source": "Java Concurrency in Practice"
            },
            
            # React
            {
                "titre": "Composants fonctionnels",
                "description": "Privilégier les composants fonctionnels avec hooks",
                "technologies": ["React"],
                "domaines": ["maintenance"],
                "tags": ["hooks"],
                "source": "React Docs"
            },
            {
                "titre": "Gestion d'état",
                "description": "Utiliser Context API ou Redux pour l'état global",
                "technologies": ["React"],
                "domaines": ["architecture"],
                "tags": ["state management"],
                "source": "React Patterns"
            },
            
            # PHP
            {
                "titre": "Sécurité des sessions",
                "description": "Utiliser session_regenerate_id() pour prévenir les attaques de fixation de session",
                "technologies": ["PHP"],
                "domaines": ["sécurité"],
                "tags": ["session", "OWASP"],
                "source": "PHP Security Best Practices"
            },
            {
                "titre": "Validation des entrées",
                "description": "Utiliser filter_var() pour valider et assainir les entrées utilisateur",
                "technologies": ["PHP"],
                "domaines": ["sécurité"],
                "tags": ["XSS", "injection"],
                "source": "PHP Manual"
            },
            {
                "titre": "Gestion des erreurs",
                "description": "Configurer error_reporting et utiliser des exceptions",
                "technologies": ["PHP"],
                "domaines": ["maintenance"],
                "tags": ["logging"],
                "source": "PHP Best Practices"
            },
            {
                "titre": "Performances",
                "description": "Utiliser OPcache pour améliorer les performances",
                "technologies": ["PHP"],
                "domaines": ["performance"],
                "tags": ["caching"],
                "source": "PHP Performance Tips"
            },
            
            # POO - Bonnes pratiques transversales
            {
                "titre": "Encapsulation",
                "description": "Utiliser des accesseurs (getters/setters) pour contrôler l'accès aux propriétés",
                "technologies": ["Java", "Python", "PHP"],
                "domaines": ["qualité"],
                "tags": ["POO", "encapsulation"],
                "source": "Clean Code"
            },
            {
                "titre": "Héritage vs Composition",
                "description": "Préférer la composition à l'héritage pour une meilleure flexibilité",
                "technologies": ["Java", "Python", "PHP"],
                "domaines": ["architecture"],
                "tags": ["POO", "design patterns"],
                "source": "Effective Java"
            },
            {
                "titre": "Principe SOLID",
                "description": "Respecter les principes SOLID pour une conception orientée objet robuste",
                "technologies": ["Java", "Python", "PHP"],
                "domaines": ["architecture"],
                "tags": ["POO", "SOLID"],
                "source": "Clean Architecture"
            },

            # TypeScript
            {
                "titre": "Typage strict",
                "description": "Activer strict mode dans tsconfig.json",
                "technologies": ["TypeScript"],
                "domaines": ["qualité"],
                "tags": ["typage"],
                "source": "TypeScript Handbook"
            },
            {
                "titre": "Interfaces vs Types",
                "description": "Préférer les interfaces pour les objets et les types pour les unions/intersections",
                "technologies": ["TypeScript"],
                "domaines": ["qualité"],
                "tags": ["typage"],
                "source": "TypeScript Best Practices"
            },

            # Go
            {
                "titre": "Gestion des erreurs",
                "description": "Utiliser les erreurs personnalisées et error wrapping",
                "technologies": ["Go"],
                "domaines": ["fiabilité"],
                "tags": ["errors"],
                "source": "Effective Go"
            },
            {
                "titre": "Concurrence",
                "description": "Utiliser les goroutines et channels de manière responsable",
                "technologies": ["Go"],
                "domaines": ["performance"],
                "tags": ["concurrency"],
                "source": "Go Concurrency Patterns"
            },

            # Rust
            {
                "titre": "Gestion de la mémoire",
                "description": "Comprendre et appliquer le système de propriété",
                "technologies": ["Rust"],
                "domaines": ["sécurité"],
                "tags": ["memory"],
                "source": "The Rust Book"
            },
            {
                "titre": "Gestion des erreurs",
                "description": "Utiliser Result et Option plutôt que les exceptions",
                "technologies": ["Rust"],
                "domaines": ["fiabilité"],
                "tags": ["errors"],
                "source": "Rust by Example"
            },

            # Kotlin
            {
                "titre": "Null safety",
                "description": "Utiliser les types nullables et les opérateurs de sécurité",
                "technologies": ["Kotlin"],
                "domaines": ["qualité"],
                "tags": ["null safety"],
                "source": "Kotlin Docs"
            },
            {
                "titre": "Coroutines",
                "description": "Utiliser les coroutines pour la programmation asynchrone",
                "technologies": ["Kotlin"],
                "domaines": ["performance"],
                "tags": ["async"],
                "source": "Kotlin Coroutines Guide"
            },

            # Swift
            {
                "titre": "Optionals",
                "description": "Utiliser les optionals et le optional binding",
                "technologies": ["Swift"],
                "domaines": ["qualité"],
                "tags": ["null safety"],
                "source": "Swift Programming Language"
            },
            {
                "titre": "Memory management",
                "description": "Comprendre ARC et éviter les cycles de référence",
                "technologies": ["Swift"],
                "domaines": ["performance"],
                "tags": ["memory"],
                "source": "Swift Memory Management"
            }
        ]

    def rechercher(self, spec: Dict) -> List[Dict]:
        """Recherche des bonnes pratiques correspondant à la spécification"""
        self.logger.info("Recherche de bonnes pratiques", spec=spec)
        
        resultats = []
        
        for pratique in self.pratiques:
            # Filtre par domaine
            if spec["domaine"] not in pratique["domaines"]:
                continue
                
            # Filtre par technologies
            if not any(tech in pratique["technologies"] for tech in spec["technologies"]):
                continue
                
            # Priorisation des contraintes
            score = 0
            if any(constraint in pratique["tags"] for constraint in spec["contraintes"]):
                score += 1
                
            resultats.append({**pratique, "score": score})
        
        # Trie par score puis par titre
        resultats.sort(key=lambda x: (-x["score"], x["titre"]))
        
        self.logger.info("Bonnes pratiques trouvées", count=len(resultats))
        return resultats
