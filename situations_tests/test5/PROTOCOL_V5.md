# PROTOCOL_V5 - Multi-Agents Orchestré

## 1. Vue d'ensemble

### 1.1 Objectifs

- **Orchestration hiérarchique** : orchestrateur central (Comet) + workers spécialisés appelés comme outils
- **Pattern Agents-as-Tools** : workers exposent des capabilities, orchestrateur route par compétence
- **Token-efficiency** : format compact, références contextuelles, budgets explicites
- **Robustesse** : gestion erreurs, limites profondeur, retries, fallbacks
- **Observabilité** : trace IDs, parent IDs, logs structurés

### 1.2 Compatibilité V4

V5 **étend** V4 :
- Segments 1-8 de V4 conservés (positions identiques)
- Segments 9-12 ajoutés (DEPTH, CTX, BUDGET, CAPS)
- Agent V4 peut ignorer segments 9+ (graceful degradation)
- Orchestrateur V5 peut forcer V4 si worker ne supporte pas V5

---

## 2. Modèle d'agents

### 2.1 Rôles

| ID | Rôle | Description | Initiative |
|----|------|-------------|------------|
| `O<1-9>` | Orchestrator | Route, agrège, décide | Initie tâches |
| `W<1-99>` | Worker | Exécute tâches spécialisées | Répond uniquement |
| `R<1-9>` | Router | Relais/load-balancer (optionnel) | Transmet |
| `G<1-9>` | Group | Groupe logique de workers | Broadcast cible |

**Conventions :**
- `O1` = orchestrateur principal (Comet)
- `W1`...`W99` = workers numérotés par ordre d'enregistrement
- `*` = broadcast tous agents
- `W*` = broadcast tous workers

### 2.2 Format ID agent

```
<ROLE><NUM>[.<SUB>]
```

| Élément | Format | Exemples |
|---------|--------|----------|
| ROLE | `O`, `W`, `R`, `G` | - |
| NUM | 1-99 | `W1`, `W42` |
| SUB | optionnel, sous-agent | `O1.W1` (hiérarchie) |

**Contraintes :** alphanum uniquement, max 10 chars.

### 2.3 Capabilities (Agents-as-Tools)

Chaque worker déclare ses **capabilities** = compétences/outils exposés.

**Format de déclaration :**
```
caps=cap1,cap2,cap3;desc=Description courte
```

**Capabilities standard :**

| Capability | Description |
|------------|-------------|
| `web_search` | Recherche web |
| `web_fetch` | Extraction contenu URL |
| `code_read` | Lecture/analyse code |
| `code_write` | Écriture/modification code |
| `code_exec` | Exécution code/scripts |
| `file_ops` | Opérations fichiers |
| `data_analysis` | Analyse données |
| `text_gen` | Génération texte |
| `summarize` | Résumé/synthèse |
| `translate` | Traduction |
| `reason` | Raisonnement complexe |
| `plan` | Planification tâches |

**Règle :** l'orchestrateur route vers le worker dont les capabilities matchent la tâche.

### 2.4 Registre d'agents (Discovery)

**Messages système pour gestion du registre :**

| Action | TYPE | DATA format |
|--------|------|-------------|
| Enregistrement | `J` (Join) | `caps=...;desc=...;max_depth=N` |
| Départ | `L` (Leave) | `reason=...` |
| Mise à jour caps | `K` (Caps update) | `caps=...` |
| Liste agents | `Q` (Query) | `filter=W*` |
| Heartbeat | `H` | `load=N%;queue=N` |

**Exemple d'enregistrement :**
```
M1|W3>O1|J|T0|-|-|-|0|S0|-|caps=web_search,summarize;desc=Research agent;max_depth=2
```

**Réponse orchestrateur :**
```
M2|O1>W3|A|T0|-|-|-|0|S0|-|registered;id=W3
```

---

## 3. Format des messages V5

### 3.1 Schéma général

```
M<n>|FROM>TO|TYPE|TID|PRI|STATE|ERR|DEPTH|CTX|BUDGET|DATA
```

**12 segments** séparés par `|`.

### 3.2 Spécification des segments

| # | Segment | Oblig. | Format | Valeurs | Max len | Défaut |
|---|---------|--------|--------|---------|---------|--------|
| 1 | `MSG` | Oui | `M<1-9999>` | - | 5 | - |
| 2 | `ROUTE` | Oui | `<ID>><ID>` | `O1>W1`, `W1>O1`, `O1>*` | 12 | - |
| 3 | `TYPE` | Oui | char(s) | voir §3.3 | 2 | - |
| 4 | `TID` | Oui | `T<1-999>` ou `-` | - | 4 | `-` |
| 5 | `PRI` | Non | `P<0-2>` | `P0`,`P1`,`P2` | 2 | `P1` |
| 6 | `STATE` | Non | char | `N`,`R`,`D`,`F`,`X` | 1 | `-` |
| 7 | `ERR` | Non | `E<00-99>` | voir §8 | 3 | `-` |
| 8 | `DEPTH` | Non | `<0-5>` | profondeur actuelle | 1 | `0` |
| 9 | `CTX` | Non | `S<id>` | session ID | 8 | `-` |
| 10 | `BUDGET` | Non | `B<n>` | tokens restants | 5 | `-` |
| 11 | `DATA` | Oui | texte | payload | 200 | - |

### 3.3 Types de messages

| Type | Nom | Usage | Émetteur typique |
|------|-----|-------|------------------|
| `R` | Request | Assignation tâche | O→W |
| `S` | Success | Résultat OK | W→O |
| `E` | Error | Erreur | W→O, O→W |
| `C` | Clarify | Question/clarification | W→O, O→W |
| `U` | Update | Progression | W→O |
| `A` | Ack | Accusé réception | tous |
| `B` | Broadcast | Info tous agents | O→* |
| `H` | Heartbeat | Santé agent | W→O |
| `D` | Disambiguate | Choix utilisateur | O→User |
| `J` | Join | Enregistrement agent | W→O |
| `L` | Leave | Départ agent | W→O |
| `K` | Caps | Mise à jour capabilities | W→O |
| `X` | Handoff | Délégation worker→worker | W→W |

### 3.4 Délimiteurs et contraintes

| Délimiteur | Usage |
|------------|-------|
| `\|` | Séparation segments |
| `>` | Routage FROM>TO |
| `=` | Clé=valeur dans DATA |
| `;` | Séparation paires dans DATA |
| `,` | Listes dans DATA |

**Interdit dans DATA :** `|`, `>`

**Taille max DATA :** 200 chars. Au-delà, utiliser référence `#REF:id`.

### 3.5 Validation parsing V5

Checklist avant traitement :

| # | Vérification | Erreur si invalide |
|---|--------------|-------------------|
| 1 | 11 segments séparés par `\|` | `E10` |
| 2 | MSG format `M\d{1,4}` | `E10` |
| 3 | ROUTE format `<ID>><ID\|*>` | `E13` |
| 4 | TYPE ∈ types valides | `E14` |
| 5 | TID format `T\d{1,3}` ou `-` | `E10` |
| 6 | PRI ∈ `{P0,P1,P2,-}` | `E11` |
| 7 | STATE ∈ `{N,R,D,F,X,-}` | `E15` |
| 8 | ERR format `E\d{2}` ou `-` | `E10` |
| 9 | DEPTH ∈ `{0,1,2,3,4,5}` | `E16` |
| 10 | CTX format `S[a-z0-9]+` ou `-` | `E10` |
| 11 | BUDGET format `B\d+` ou `-` | `E10` |
| 12 | DATA len ≤ 200 | tronquer + warn |
| 13 | Pas de `\|` ou `>` dans DATA | `E12` |

---

## 4. Cycle de vie d'une tâche

### 4.1 États et transitions

```
    ┌───┐
    │ N │ (New)
    └─┬─┘
      │ R reçu
      ▼
    ┌───┐
    │ R │ (Running)
    └─┬─┘
      │
   ┌──┴──┐
   ▼     ▼
 ┌───┐ ┌───┐
 │ D │ │ F │
 │Done│ │Fail│
 └───┘ └───┘
   ▲
   │ (annulation depuis N ou R)
 ┌───┐
 │ X │ (Cancelled)
 └───┘
```

**Transitions valides :**
- `N` → `R` (démarrage)
- `R` → `D` (succès)
- `R` → `F` (échec)
- `N|R` → `X` (annulation)

### 4.2 Main loop orchestrateur (O1)

```
LOOP:
  1. RECEIVE message (user request ou worker response)

  2. IF user_request:
     a. CREATE TID, CTX, BUDGET
     b. PARSE intent, MATCH capabilities
     c. SELECT worker(s) par capabilities + load
     d. SEND R message(s) à worker(s)
     e. STATE = N → R

  3. IF worker_response:
     a. VALIDATE format V5
     b. SWITCH TYPE:
        - S (Success): AGGREGATE result, IF complete → respond to user
        - E (Error): APPLY retry/fallback strategy
        - C (Clarify): FORWARD to user OR resolve internally
        - U (Update): LOG progress, UPDATE state
        - X (Handoff): VALIDATE depth, APPROVE or REJECT
     c. UPDATE task state

  4. IF timeout(TID):
     a. SEND E message with E20
     b. APPLY fallback

  5. IF all_tasks_complete(CTX):
     a. SYNTHESIZE final response
     b. SEND to user
     c. CLOSE CTX
```

### 4.3 Comportement worker

```
ON RECEIVE message:
  1. VALIDATE format V5
  2. IF invalid: RESPOND E with E10

  3. CHECK DEPTH:
     IF DEPTH >= max_depth: RESPOND E with E16

  4. CHECK BUDGET:
     IF BUDGET insufficient: RESPOND E with E17

  5. PROCESS task:
     a. IF need_clarification: SEND C
     b. IF can_execute:
        - SEND U (progress) si long
        - EXECUTE
        - SEND S (success) ou E (error)
     c. IF need_handoff:
        - SEND X to target worker (DEPTH+1)
        - NOTIFY O1

  6. ALWAYS include: TID, CTX, DEPTH from request
```

### 4.4 Diagramme de séquence standard

```
User          O1              W1              W2
  │            │               │               │
  │──Request──▶│               │               │
  │            │               │               │
  │            │──M1:R,T1,D0──▶│               │
  │            │               │               │
  │            │◀──M2:U,T1,D0──│ (progress)    │
  │            │               │               │
  │            │◀──M3:S,T1,D0──│               │
  │            │               │               │
  │◀──Result───│               │               │
```

**Avec handoff :**

```
User          O1              W1              W2
  │            │               │               │
  │──Request──▶│               │               │
  │            │──M1:R,T1,D0──▶│               │
  │            │               │──M2:X,T1,D1──▶│ (handoff)
  │            │◀──M3:U,T1,D1──│ (notify O1)   │
  │            │               │               │
  │            │               │◀──M4:S,T1,D1──│
  │            │◀──M5:S,T1,D0──│ (aggregate)   │
  │◀──Result───│               │               │
```

---

## 5. Routage et délégation (Agents-as-Tools)

### 5.1 Sélection worker par capabilities

**Algorithme orchestrateur :**

```
SELECT_WORKER(task):
  1. EXTRACT required_caps from task
  2. FOR each registered worker W:
     - MATCH W.caps ∩ required_caps
     - SCORE = |match| / |required_caps|
  3. FILTER workers with SCORE >= threshold (0.5)
  4. SORT by: SCORE desc, load asc, last_used asc
  5. RETURN top worker (ou top N pour parallel)
```

### 5.2 Format d'appel capability dans DATA

```
call=<capability>;params=<params>;
```

**Exemples :**

```
call=web_search;params=query:"AI orchestration patterns";
```

```
call=code_write;params=file:main.py,action:edit,target:function:init;
```

```
call=summarize;params=src:#REF:T41:S,maxlen:100;
```

### 5.3 Handoffs worker→worker

**Règles :**
1. Worker peut déléguer à un autre worker via `TYPE=X`
2. `DEPTH` incrémenté de 1
3. Worker source DOIT notifier O1 via `TYPE=U`
4. Worker cible répond au worker source (pas directement à O1)
5. Worker source agrège et répond à O1

**Format handoff :**
```
M<n>|W1>W2|X|TID|PRI|STATE|ERR|DEPTH+1|CTX|BUDGET|call=...;reason=...
```

**Notification à O1 :**
```
M<n>|W1>O1|U|TID|PRI|R|-|DEPTH|CTX|BUDGET|handoff=W2;reason=...
```

### 5.4 Limites de profondeur

| DEPTH | Signification |
|-------|---------------|
| 0 | Requête directe O→W |
| 1 | Premier handoff W→W |
| 2 | Second handoff |
| 3 | Max recommandé |
| 4-5 | Exceptionnel, justification requise |

**Dépassement :** répondre `E` avec `E16:max_depth`.

---

## 6. Gestion de contexte et sessions

### 6.1 Format CTX

```
S<id>
```

| Format | Exemple | Usage |
|--------|---------|-------|
| `S<num>` | `S1`, `S42` | Session numérotée simple |
| `S<alphanum>` | `Sabc12` | Session avec ID externe |

**Contraintes :** max 8 chars, alphanum lowercase.

### 6.2 Règles de gestion

1. **Création** : O1 crée CTX au début d'une conversation/tâche
2. **Propagation** : tous messages liés à la tâche portent le même CTX
3. **Fermeture** : O1 ferme CTX quand tâche complète ou timeout
4. **Isolation** : workers ne doivent pas inventer de CTX

### 6.3 Références contextuelles dans DATA

| Format | Signification |
|--------|---------------|
| `#CTX:key` | Référence valeur dans contexte courant |
| `#REF:TID:field` | Référence champ d'une tâche passée |
| `#MSG:Mn` | Référence message précédent |

**Exemples :**
```
src=#REF:T1:S;action=summarize
```
```
prev=#MSG:M3;continue=true
```

---

## 7. Désambiguïsation et clarification

### 7.1 Clarification O ↔ W

**Worker demande clarification :**
```
M5|W1>O1|C|T1|P1|R|-|1|S1|B100|question=format sortie?;options=json,txt,md
```

**Orchestrateur répond :**
```
M6|O1>W1|C|T1|P1|R|-|1|S1|B100|answer=json
```

### 7.2 Désambiguïsation utilisateur (TYPE=D)

Quand l'orchestrateur ne peut pas décider seul :

```
M7|O1>User|D|T1|P1|R|-|0|S1|-|question=Quel type d'analyse?;opt1=rapide;opt2=approfondie;opt3=comparative
```

**Règles :**
- Max 3-4 options
- Options courtes (1-3 mots)
- Timeout : 60s, puis fallback option 1 ou abandon

### 7.3 Limites de clarification

- Max **2 tours** de clarification par tâche
- Au-delà : décision autonome ou `E` avec `E18:max_clarify`

---

## 8. Gestion des erreurs

### 8.1 Codes erreur V5

| Cat. | Codes | Description |
|------|-------|-------------|
| **OK** | `E00` | Pas d'erreur |
| **Validation** | `E10-E19` | Format, parsing |
| **Timeout** | `E20-E29` | Délais |
| **Resource** | `E30-E39` | Indisponibilité |
| **Logic** | `E40-E49` | Erreurs métier |
| **System** | `E90-E99` | Autres |

**Table détaillée :**

| Code | Signification |
|------|---------------|
| `E00` | OK (pas d'erreur) |
| `E10` | Format message invalide |
| `E11` | Priorité invalide |
| `E12` | DATA contient caractères interdits |
| `E13` | Route invalide |
| `E14` | Type message inconnu |
| `E15` | Transition état invalide |
| `E16` | Max depth dépassé |
| `E17` | Budget insuffisant |
| `E18` | Max clarifications atteint |
| `E19` | Capability non supportée |
| `E20` | Timeout global |
| `E21` | Timeout réponse worker |
| `E22` | Timeout heartbeat |
| `E23` | Timeout clarification user |
| `E30` | Worker indisponible |
| `E31` | Worker saturé (BUSY) |
| `E32` | Ressource externe indisponible |
| `E33` | Fichier introuvable |
| `E40` | Tâche inconnue |
| `E41` | Agent inconnu |
| `E42` | Session inconnue |
| `E43` | Référence invalide |
| `E90` | Version protocole incompatible |
| `E99` | Erreur non catégorisée |

### 8.2 Stratégie retry/fallback

**Dans DATA, métadonnées retry :**
```
retry=<n>;max=<max>;fallback=<agent>;
```

**Règles :**
1. Erreurs `E20-E29` (timeout) : retry auto, max 2
2. Erreurs `E30-E31` (worker) : fallback vers autre worker
3. Erreurs `E10-E19` (validation) : pas de retry, fix requis
4. Erreurs `E40+` (logic) : remonter à l'utilisateur

**Exemple retry :**
```
M8|O1>W1|R|T1|P1|N|-|0|S1|B200|call=web_search;retry=1;max=2
```

**Exemple fallback :**
```
M9|O1>W2|R|T1|P1|N|-|0|S1|B200|call=web_search;fallback_from=W1;reason=E31
```

### 8.3 Format message erreur

```
M<n>|FROM>TO|E|TID|PRI|F|ERR|DEPTH|CTX|BUDGET|desc=...;details=...
```

**Exemple :**
```
M10|W1>O1|E|T1|P1|F|E33|1|S1|B50|desc=file not found;path=/data/input.json
```

---

## 9. Contrôle des coûts

### 9.1 Budget tokens

**Format :** `B<n>` où n = tokens restants alloués.

**Règles :**
1. O1 définit budget initial basé sur complexité estimée
2. Chaque worker consomme et décrémente
3. Worker DOIT refuser si `BUDGET < estimation_cost`
4. Handoff : budget partagé/divisé

**Budgets typiques :**

| Complexité | Budget |
|------------|--------|
| Simple | `B100` |
| Moyen | `B500` |
| Complexe | `B2000` |
| Illimité | `-` (non recommandé) |

### 9.2 Dépassement budget

Si budget insuffisant :
```
M11|W1>O1|E|T1|P1|F|E17|1|S1|B20|desc=budget insufficient;needed=150;have=20
```

**Options O1 :**
- Augmenter budget et retry
- Demander version simplifiée
- Abandonner avec message user

### 9.3 Optimisation DATA

1. **Références** : utiliser `#REF:` au lieu de répéter
2. **Compression** : abréviations, mots-clés
3. **Pagination** : découper gros résultats en chunks

---

## 10. Traçabilité et logs

### 10.1 Identifiants de corrélation

| ID | Rôle | Scope |
|----|------|-------|
| `TID` | Task ID | Une tâche atomique |
| `CTX` | Session ID | Conversation/flux complet |
| `MSG` | Message ID | Un message unique |
| `PID` | Parent ID | Chaînage causal |

### 10.2 Parent ID (PID)

Encodé dans DATA si nécessaire :
```
pid=M<n>;
```

**Exemple :**
```
M12|W1>O1|S|T1|P1|D|-|1|S1|B100|pid=M5;result=...
```

### 10.3 Format log recommandé

```
[TS] [LEVEL] [CTX] [TID] FROM>TO TYPE ERR DATA_SUMMARY
```

**Exemple :**
```
[14523] [INFO] [S1] [T1] O1>W1 R - call=web_search
[14530] [INFO] [S1] [T1] W1>O1 S - results=3
[14532] [WARN] [S1] [T2] W2>O1 E E31 BUSY queue=5
```

---

## 11. Sécurité (optionnel)

### 11.1 Sessions authentifiées

**Segment AUTH optionnel** (peut remplacer `-` dans implémentation sécurisée) :
```
SID:NONCE:SIG
```

| Élément | Format | Description |
|---------|--------|-------------|
| SID | `S<n>` | Session ID |
| NONCE | 4 chars hex | Anti-replay |
| SIG | 8 chars hex | HMAC-SHA256 tronqué |

### 11.2 Règles

- Clé partagée pré-établie hors-bande
- Messages sans SIG valide : rejetés avec `E90`
- Optionnel pour systèmes internes de confiance

---

## 12. Exemples complets

### 12.1 Flux standard O1 → W1 → réponse

**Requête utilisateur :** "Recherche les dernières news sur l'IA"

```
M1|O1>W1|R|T1|P1|N|-|0|S1|B500|call=web_search;query=latest AI news 2024
```

**Update progression :**
```
M2|W1>O1|U|T1|P1|R|-|0|S1|B450|progress=50%;found=12 articles
```

**Résultat :**
```
M3|W1>O1|S|T1|P1|D|-|0|S1|B200|results=5;top1=OpenAI GPT-5;top2=Claude 4;src=#REF:T1:raw
```

### 12.2 Handoff W1 → W2

**Requête initiale :**
```
M1|O1>W1|R|T1|P1|N|-|0|S1|B1000|call=analyze_code;file=main.py
```

**W1 délègue à W2 (spécialisé tests) :**
```
M2|W1>W2|X|T1|P1|R|-|1|S1|B500|call=generate_tests;src=#REF:T1:code;reason=specialized
```

**W1 notifie O1 :**
```
M3|W1>O1|U|T1|P1|R|-|0|S1|B500|handoff=W2;subtask=generate_tests
```

**W2 répond à W1 :**
```
M4|W2>W1|S|T1|P1|D|-|1|S1|B300|tests=3;coverage=85%
```

**W1 agrège et répond à O1 :**
```
M5|W1>O1|S|T1|P1|D|-|0|S1|B200|analysis=done;tests=3;coverage=85%;quality=good
```

### 12.3 Désambiguïsation utilisateur

**Orchestrateur détecte ambiguïté :**
```
M1|O1>User|D|T1|P1|R|-|0|S1|-|question=Quel format de rapport?;opt1=résumé court;opt2=rapport détaillé;opt3=données brutes
```

**Utilisateur répond (via interface) :**
```
M2|User>O1|C|T1|P1|R|-|0|S1|-|choice=opt2
```

**O1 route vers worker :**
```
M3|O1>W1|R|T1|P1|R|-|0|S1|B1000|call=generate_report;format=detailed
```

### 12.4 Enregistrement capabilities (JOIN)

**Worker s'enregistre :**
```
M1|W3>O1|J|T0|P1|N|-|0|S0|-|caps=web_search,web_fetch,summarize;desc=Web research agent;max_depth=2;version=V5
```

**O1 confirme :**
```
M2|O1>W3|A|T0|P1|D|-|0|S0|-|registered;id=W3;status=active
```

**Query liste agents :**
```
M3|O1>O1|Q|T0|P1|-|-|0|S0|-|filter=W*;status=active
```

**Réponse interne :**
```
M4|O1>O1|S|T0|P1|D|-|0|S0|-|agents=W1,W2,W3;count=3
```

---

## 13. Prompts système

### 13.1 Prompt orchestrateur (Comet)

```
Tu es COMET, orchestrateur principal d'un système multi-agents.

## Protocole
Applique PROTOCOL_V5 pour toutes communications.
Format: M<n>|FROM>TO|TYPE|TID|PRI|STATE|ERR|DEPTH|CTX|BUDGET|DATA

## Rôle
- Router les requêtes vers workers par capabilities
- Gérer sessions (CTX), budgets (BUDGET), profondeur (DEPTH)
- Agréger réponses, gérer erreurs et retries

## Workers disponibles
[INSÉRER REGISTRE CAPABILITIES]

## Règles
1. Créer TID unique par tâche, CTX par conversation
2. Matcher capabilities avant routage
3. Limiter DEPTH à 3 max
4. Budget initial selon complexité (B100/B500/B2000)
5. Retry max 2 sur timeout (E20-E29)
6. Fallback vers autre worker sur E30-E31
7. Désambiguïer via TYPE=D si choix requis
8. Logger chaque message: [CTX] [TID] FROM>TO TYPE

## Format réponse user
Synthèse concise du résultat, sans exposer le protocole interne.
```

### 13.2 Prompt worker générique

```
Tu es un WORKER dans un système multi-agents orchestré par COMET.

## Protocole
Applique PROTOCOL_V5 pour toutes communications.
Format: M<n>|FROM>TO|TYPE|TID|PRI|STATE|ERR|DEPTH|CTX|BUDGET|DATA

## Tes capabilities
[INSÉRER CAPABILITIES: cap1, cap2, cap3]

## Règles
1. Répondre UNIQUEMENT aux messages de O1 ou handoffs valides
2. Conserver TID, CTX, DEPTH reçus dans ta réponse
3. Vérifier DEPTH < max_depth (sinon E16)
4. Vérifier BUDGET suffisant (sinon E17)
5. TYPE réponse: S (succès), E (erreur), C (clarification), U (update)
6. Handoff (X) autorisé si DEPTH+1 <= max, notifier O1

## Format réponse
Toujours format V5 monoligne. DATA compact, max 200 chars.
Références: #REF:TID:field pour éviter répétitions.

## Erreurs
- E10: format invalide reçu
- E16: depth max dépassé
- E17: budget insuffisant
- E19: capability non supportée
- E33: ressource introuvable
```

### 13.3 Prompt worker spécialisé (Research)

```
Tu es W1-RESEARCH, worker spécialisé recherche web.

## Capabilities
caps=web_search,web_fetch,summarize

## Protocole
PROTOCOL_V5. Format: M<n>|W1>O1|TYPE|TID|PRI|STATE|ERR|DEPTH|CTX|BUDGET|DATA

## Comportement
1. web_search: rechercher, retourner top 5 résultats
2. web_fetch: extraire contenu URL, max 500 chars
3. summarize: résumer en max 100 mots

## Réponses
- Succès: TYPE=S, DATA=results=N;top1=...;top2=...
- Clarification: TYPE=C, DATA=question=...;options=...
- Erreur: TYPE=E, ERR=code, DATA=desc=...

## Contraintes
- BUDGET: ajuster verbosité selon budget restant
- DEPTH: max 2, handoff vers W2-ANALYST si analyse poussée requise
```

---

## 14. Compatibilité et versioning

### 14.1 Historique versions

| Version | Statut | Usage |
|---------|--------|-------|
| V1 | Legacy | Documentation uniquement |
| V2 | Legacy | Documentation uniquement |
| V3 | Deprecated | Migration recommandée |
| V4 | Stable | Production, systèmes simples |
| V5 | **Recommandé** | Systèmes orchestrés modernes |

### 14.2 Règles de compatibilité

**V5 → V4 (downgrade) :**
```
V5: M1|O1>W1|R|T1|P1|N|-|0|S1|B500|data
V4: M1|O1>W1|R|T1|P1|N|-|data
```
Supprimer segments 8-10 (DEPTH, CTX, BUDGET).

**V4 → V5 (upgrade) :**
```
V4: M1|O1>W1|R|T1|P1|N|-|data
V5: M1|O1>W1|R|T1|P1|N|-|0|-|-|data
```
Ajouter `-` pour segments manquants.

### 14.3 Négociation version

**Handshake initial :**
```
M0|W1>O1|J|T0|-|-|-|0|-|-|version=V5;fallback=V4
```

**Si O1 ne supporte que V4 :**
```
M1|O1>W1|A|T0|-|-|-|-|-|-|version=V4;mode=compat
```

---

## Annexe A : Diff V4 → V5

### Ajouts

| Élément | Description |
|---------|-------------|
| Segment DEPTH | Contrôle profondeur handoffs |
| Segment CTX | Session/contexte |
| Segment BUDGET | Budget tokens |
| TYPE J/L/K | Join/Leave/Caps (discovery) |
| TYPE D | Désambiguïsation user |
| TYPE X | Handoff explicite |
| Capabilities | Déclaration compétences workers |
| Registre | Discovery dynamique agents |
| Références | #REF:, #CTX:, #MSG: |
| Retry/fallback | Stratégie dans DATA |
| Codes E16-E19 | Depth, budget, clarify, caps |

### Modifications

| V4 | V5 |
|----|-----|
| 8 segments | 11 segments |
| Pas de session | CTX obligatoire recommandé |
| Depth implicite | DEPTH explicite |
| Budget implicite | BUDGET explicite |

### Suppressions

Aucune suppression, V5 superset de V4.

---

## Annexe B : Quick Reference Card

```
FORMAT V5:
M<n>|FROM>TO|TYPE|TID|PRI|STATE|ERR|DEPTH|CTX|BUDGET|DATA

TYPES: R S E C U A B H D J L K X

PRI: P0 P1 P2
STATE: N R D F X
ERR: E00-E99
DEPTH: 0-5
CTX: S<id>
BUDGET: B<n>

EXEMPLES:
Request:  M1|O1>W1|R|T1|P1|N|-|0|S1|B500|call=web_search;query=AI
Success:  M2|W1>O1|S|T1|P1|D|-|0|S1|B300|results=5
Error:    M3|W1>O1|E|T1|P1|F|E33|0|S1|B300|desc=file not found
Handoff:  M4|W1>W2|X|T1|P1|R|-|1|S1|B250|call=analyze;reason=specialized
```

---
