tu es un agent orchestrateur spécialiste en développement d'appli web.
Tu vas devoir guider un agent codeur claudecode qui va coder pour toi.
Voici le plan de développement de l'appli : 
Voici un plan d’action structuré pour la création de l’appli todo‑list (Python + HTML) qui servira de base à ton document de communication entre agents.
​

1. Objectif et périmètre
Construire une mini application web de type todo‑list avec : une page HTML unique, un backend Python minimal, stockage en mémoire (liste Python), sans base de données.
​

S’en servir comme cas d’école pour formaliser et optimiser la communication entre deux agents :

Agent 1 = spécification/reformulation.

Agent 2 = génération et ajustement du code Python/HTML.
​

2. Découpage en étapes
Définir le comportement fonctionnel exact (UX minimale).

Définir l’architecture de fichiers la plus simple.

Spécifier l’API minimale entre frontend et backend.

Générer le squelette de code (Python + HTML).

Tester en local et corriger les bugs.

Itérer sur de très petits raffinements (style, messages) pour tester le processus multi‑agents.
​

3. Spécification fonctionnelle (version courte)
Page d’accueil :

Affiche un titre "Ma Todo‑list".

Formulaire avec champ texte "Nouvelle tâche" + bouton "Ajouter".

Liste des tâches en dessous, chaque nouvelle tâche s’ajoute en haut ou en bas de la liste.
​

Comportement :

Si le champ est vide et qu’on clique sur "Ajouter", ne rien ajouter (optionnel : afficher un petit message).

Les tâches sont stockées en mémoire (liste Python), non persistantes : tout est perdu au redémarrage du serveur.
​

4. Architecture technique
Stack : Python 3 + micro‑framework type Flask (pour rester simple mais réaliste).
​

Structure de projet recommandée :

app.py : point d’entrée du serveur web.

templates/index.html : page HTML principale (utilisation minimale de Jinja pour afficher la liste).

static/style.css (optionnel) : quelques règles CSS simples.
​

5. API minimale entre frontend et backend
Route GET / :

Rôle : renvoyer la page HTML avec la liste actuelle des tâches.

Réponse : rendu du template index.html avec la liste passée en contexte.
​

Route POST /add :

Entrée : champ de formulaire task (texte).

Traitement : si non vide, ajouter la tâche à la liste en mémoire.

Réponse : redirection vers / (pattern simple type "POST/Redirect/GET").
​

6. Rôle des 2 agents sur ce plan
Agent 1 (spécification) doit produire, à partir d’une phrase utilisateur libre :

Un résumé du besoin.

La liste des fichiers à créer.

La description des routes (GET /, POST /add).

Les contraintes de simplicité (pas de DB, stockage en mémoire, 1 seule page).
​

Agent 2 (codeur) doit :

Générer app.py avec les routes définies.

Générer templates/index.html avec le formulaire + boucle d’affichage des tâches.

Proposer ensuite un mini plan de tests manuels (démarrage serveur, ajout de tâches, cas champ vide).
​

7. Étapes concrètes pour la création
Préparation environnement : créer dossier projet, environnement virtuel, installer Flask (pip install flask).
​
​

Implémentation initiale :

Étape 1 : route GET / qui renvoie juste "Hello" pour valider la stack.

Étape 2 : ajouter la liste en mémoire + template HTML simple.

Étape 3 : route POST /add + formulaire HTML qui appelle cette route.
​

Validation :

Tester dans le navigateur : ajout de plusieurs tâches, rafraîchissement, redémarrage du serveur pour constater la perte des données (comportement attendu).

Tu vas lui demander de créer l'appli dans le dossier C:\Users\raph6\Documents\ServOMorph\auto_copier_coller\situations_tests\test1

Dans cette conversation tu vas répondre sans commentaires, juste avec le message à envoyer à claudecode. Je te partagerai en suivant son retour. Tu devras le guider pour créer l'appli le plus rapidement possible