# PROTOCOL_V1 - Communication Inter-Agents

## 1. Objectif

Coordination de deux agents IA via messages structurés.
Priorités : rapidité, clarté, économie de tokens.

---

## 2. Rôles des agents

| Rôle | Responsabilité | Initiative |
|------|----------------|------------|
| `ORCHESTRATOR` | Assigne tâches, valide résultats | Initie échanges |
| `WORKER` | Exécute tâches, rapporte résultats | Répond uniquement |

---

## 3. Format des messages

```
[MSG_XX]
FROM: <ROLE>
TO: <ROLE>
TYPE: <TYPE_MESSAGE>
TASK: <TASK_XX> (optionnel)
DATA: <contenu>
```

Règles :
- Ordre des champs fixe
- Pas de champs vides
- `DATA` : texte minimal ou structure clé:valeur

---

## 4. Types de messages

| Type | Usage | DATA attendu |
|------|-------|--------------|
| `REQ` | Demande de tâche | Description courte de la tâche |
| `RES` | Réponse à tâche | Résultat ou statut |
| `CLR` | Clarification | Question précise |
| `UPD` | Mise à jour | Progression ou changement |
| `ACK` | Accusé réception | Vide ou confirmation |
| `ERR` | Erreur | Code + description courte |

---

## 5. Règles d'optimisation tokens

1. **Références par ID** : utiliser `TASK_01`, `MSG_01` au lieu de répéter le contenu
2. **Pas de formules** : pas de "bonjour", "merci", "s'il te plaît"
3. **Mots-clés** : phrases télégraphiques acceptées
4. **Abréviations stables** :
   - `REQ` = request
   - `RES` = response
   - `CLR` = clarification
   - `UPD` = update
   - `ACK` = acknowledge
   - `ERR` = error
5. **Incréments protocole** : `PROTOCOL_V2` documente uniquement les deltas vs V1

---

## 6. Exemples d'échanges

### Échange standard

```
[MSG_01]
FROM: ORCHESTRATOR
TO: WORKER
TYPE: REQ
TASK: TASK_01
DATA: analyser fichier config.json
```

```
[MSG_02]
FROM: WORKER
TO: ORCHESTRATOR
TYPE: RES
TASK: TASK_01
DATA: 3 clés trouvées: host, port, debug
```

### Clarification

```
[MSG_03]
FROM: WORKER
TO: ORCHESTRATOR
TYPE: CLR
TASK: TASK_01
DATA: format sortie attendu?
```

```
[MSG_04]
FROM: ORCHESTRATOR
TO: WORKER
TYPE: RES
TASK: TASK_01
DATA: liste simple
```

### Erreur

```
[MSG_05]
FROM: WORKER
TO: ORCHESTRATOR
TYPE: ERR
TASK: TASK_01
DATA: E01:fichier introuvable
```

### Accusé réception

```
[MSG_06]
FROM: ORCHESTRATOR
TO: WORKER
TYPE: ACK
TASK: TASK_01
DATA: recu
```

---

## 7. Versioning

- Version actuelle : `PROTOCOL_V1`
- Prochaine version : `PROTOCOL_V2`
- Format changelog : liste des ajouts/modifications/suppressions uniquement

---
---

# PROTOCOL_V2 - Communication Inter-Agents

## Objectif V2

Optimisation token-aggressive de V1.
Cibles : format monoligne, champs implicites, délimiteurs fixes.

---

## 1. Objectif

Coordination agents IA. Tokens minimaux. Parsing simple.

---

## 2. Rôles

| ID | Rôle | Init |
|----|------|------|
| `O` | Orchestrator | Oui |
| `W` | Worker | Non |

Convention : `O` initie, `W` répond.

---

## 3. Format des messages

**Format monoligne :**
```
MSG_XX|ROLE|TYPE|TASK_XX|data
```

Règles :
- Délimiteur : `|`
- `ROLE` : émetteur uniquement (`O` ou `W`), récepteur implicite
- `TASK_XX` : obligatoire sauf `ACK`
- `data` : texte brut, pas de `|` dans data

**Format étendu (si data complexe) :**
```
MSG_XX|ROLE|TYPE|TASK_XX|k1=v1;k2=v2
```

---

## 4. Types de messages

| Type | Usage | Data |
|------|-------|------|
| `R` | Request | instruction |
| `S` | Response | résultat |
| `C` | Clarification | question |
| `U` | Update | progression |
| `A` | Ack | - |
| `E` | Error | Ecode:desc |

**Codes erreur standardisés :**
| Code | Signification |
|------|---------------|
| `E01` | Fichier introuvable |
| `E02` | Format invalide |
| `E03` | Timeout |
| `E04` | Ressource indisponible |
| `E99` | Autre |

---

## 5. Règles tokens V2

1. IDs courts : `O`, `W`, `R`, `S`, `C`, `U`, `A`, `E`
2. Pas de préfixes (`FROM:`, `TO:`) → implicites
3. Monoligne obligatoire
4. Référencer par ID, jamais répéter contenu
5. data : mots-clés, pas de phrases
6. Erreurs : code uniquement si message clair

---

## 6. Exemples V2

**Request :**
```
MSG_01|O|R|TASK_01|analyser config.json
```

**Response :**
```
MSG_02|W|S|TASK_01|3 clés:host,port,debug
```

**Clarification :**
```
MSG_03|W|C|TASK_01|format sortie?
```
```
MSG_04|O|S|TASK_01|liste
```

**Erreur :**
```
MSG_05|W|E|TASK_01|E01:config.json
```

**Ack :**
```
MSG_06|O|A|TASK_01|ok
```

---

## Diff_V1_V2

**Modifications :**
- Format multi-lignes → monoligne avec `|`
- `ORCHESTRATOR` → `O`, `WORKER` → `W`
- `REQ` → `R`, `RES` → `S`, `CLR` → `C`, `UPD` → `U`, `ACK` → `A`, `ERR` → `E`
- Champs `FROM`/`TO` → `ROLE` émetteur seul
- Préfixes supprimés

**Ajouts :**
- Codes erreur standardisés (E01-E99)
- Format data structuré `k=v;k=v`

**Suppressions :**
- Blocs multi-lignes
- Champ `TO` explicite

**Gain estimé :** ~40-50% tokens par message

---

## Roadmap_PROTOCOL_V3

Axes envisagés :
- Multi-agents (>2) : routage par ID agent
- Priorités : champ `P` (1-3)
- Chaînage : `REF_MSG_XX` pour lier messages
- Compression data : dictionnaire partagé de termes fréquents
- Batch : plusieurs instructions par message

---
---

# PROTOCOL_V3 - Communication Multi-Agents

## Objectif V3

Extension multi-agents de V2.
Cibles : routage N agents, priorités, états tâches, erreurs étendues.
Compatibilité : mode 2-agents = V2 valide.

---

## 1. Objectif

Coordination N agents IA. Routage explicite. Priorités. États. Tokens optimaux.

---

## 2. Agents

**Format ID agent :** `<ROLE><NUM>`

| Pattern | Description | Exemples |
|---------|-------------|----------|
| `O<n>` | Orchestrator n | `O1`, `O2` |
| `W<n>` | Worker n | `W1`, `W2`, `W3` |
| `*` | Broadcast | tous agents du type |

**Règles :**
- `O1` = orchestrator principal (défaut si omis)
- `W1`...`Wn` = workers numérotés
- Multi-orchestrators : `O1`, `O2` (rare, cas distribués)

---

## 3. Format des messages V3

**Format monoligne enrichi :**
```
MSG_XX|FROM>TO|TYPE|TASK_XX|PRI|STATE|data
```

| Champ | Obligatoire | Valeurs | Défaut |
|-------|-------------|---------|--------|
| `MSG_XX` | Oui | `MSG_01`... | - |
| `FROM>TO` | Oui | `O1>W1`, `W2>O1`, `O1>*` | - |
| `TYPE` | Oui | `R`,`S`,`C`,`U`,`A`,`E`,`B` | - |
| `TASK_XX` | Oui* | `TASK_01`... ou `-` | `-` |
| `PRI` | Non | `P0`,`P1`,`P2` | `P1` |
| `STATE` | Non | `N`,`R`,`D`,`F`,`X` | `-` |
| `data` | Oui | texte, `k=v;k=v` | - |

*`TASK_XX` = `-` pour `A` ou messages système.

**Délimiteurs :**
- Inter-champs : `|`
- Routage : `>`
- Data structuré : `=` et `;`
- Pas de `|` ni `>` dans data

---

## 4. Types de messages V3

| Type | Usage | Data |
|------|-------|------|
| `R` | Request | instruction |
| `S` | Response | résultat |
| `C` | Clarification | question |
| `U` | Update | progression % ou état |
| `A` | Ack | `-` ou `ok` |
| `E` | Error | `Exx:desc` |
| `B` | Broadcast | info pour tous |

---

## 5. Priorités

| Code | Niveau | Traitement |
|------|--------|------------|
| `P0` | Critique | Immédiat, interrompt P1/P2 |
| `P1` | Normal | File standard |
| `P2` | Faible | Différable |

**Règles :**
- Défaut = `P1`
- Worker surchargé → `E06:BUSY` + file actuelle
- Conflit priorité → worker signale via `C`

---

## 6. États tâche

| Code | État | Description |
|------|------|-------------|
| `N` | New | Tâche créée |
| `R` | Running | En cours |
| `D` | Done | Terminée OK |
| `F` | Failed | Échec |
| `X` | Cancelled | Annulée |
| `-` | N/A | Non applicable |

---

## 7. Codes erreur V3

| Code | Signification |
|------|---------------|
| `E01` | Fichier introuvable |
| `E02` | Format invalide |
| `E03` | Timeout |
| `E04` | Ressource indisponible |
| `E05` | Parsing échoué |
| `E06` | Agent saturé (BUSY) |
| `E07` | Version protocole incompatible |
| `E08` | Agent inconnu |
| `E09` | Tâche inconnue |
| `E10` | Priorité invalide |
| `E99` | Autre |

---

## 8. Règles tokens V3

1. IDs agents courts : `O1`, `W1`, `W2`
2. Routage compact : `FROM>TO` (pas `FROM|TO`)
3. Champs optionnels : `-` si non utilisé
4. Priorité implicite `P1` → omettre si standard
5. État uniquement si changement significatif
6. Référencer par ID, jamais répéter contenu
7. Broadcast `*` pour éviter N messages identiques

**Format minimal (compatibilité V2) :**
```
MSG_XX|O1>W1|TYPE|TASK_XX|-|-|data
```

---

## 9. Validation parsing

Avant traitement, vérifier :

1. **Structure** : 7 segments séparés par `|`
2. **MSG_ID** : format `MSG_\d+`
3. **Routage** : format `<ID>><ID>` ou `<ID>>*`
4. **TYPE** : ∈ {`R`,`S`,`C`,`U`,`A`,`E`,`B`}
5. **TASK_ID** : format `TASK_\d+` ou `-`
6. **PRI** : ∈ {`P0`,`P1`,`P2`,`-`}
7. **STATE** : ∈ {`N`,`R`,`D`,`F`,`X`,`-`}

**Si invalide :** répondre `E05:parsing` + segment fautif.

---

## 10. Exemples V3

### Assignation prioritaire O1 → W1

```
MSG_01|O1>W1|R|TASK_01|P0|N|analyser logs critiques
```

### Réponse succès W1 → O1

```
MSG_02|W1>O1|S|TASK_01|P0|D|3 erreurs détectées
```

### Assignation normale O1 → W2

```
MSG_03|O1>W2|R|TASK_02|P1|N|backup config
```

### Erreur ressource W2 → O1

```
MSG_04|W2>O1|E|TASK_02|P1|F|E04:disk full
```

### Worker saturé

```
MSG_05|W1>O1|E|TASK_03|P1|-|E06:BUSY;queue=3
```

### Clarification multi-agents

```
MSG_06|W1>O1|C|TASK_01|P0|R|format sortie?
```
```
MSG_07|O1>W1|S|TASK_01|P0|R|json
```

### Broadcast info

```
MSG_08|O1>*|B|-|P1|-|maintenance 5min
```

### Annulation tâche

```
MSG_09|O1>W2|U|TASK_02|P1|X|annulé
```
```
MSG_10|W2>O1|A|TASK_02|-|-|ok
```

### Progression

```
MSG_11|W1>O1|U|TASK_01|P0|R|progress=75%
```

---

## Diff_V2_V3

**Ajouts :**
- IDs agents numériques : `O1`, `W1`, `W2`...
- Routage explicite : `FROM>TO`
- Champ `PRI` : `P0`, `P1`, `P2`
- Champ `STATE` : `N`, `R`, `D`, `F`, `X`
- Type `B` (Broadcast)
- Codes erreur : `E05`-`E10`
- Section validation parsing
- Broadcast `*`

**Modifications :**
- Format : 5 → 7 segments
- `O` → `O1`, `W` → `W1` (numérotation obligatoire)
- Séparateur routage : `>` au lieu de position implicite

**Compatibilité V2 :**
- Message V2 convertible : ajouter `>TO`, `|-|-|` pour PRI/STATE

**Gain tokens :**
- Multi-destinataires : `*` évite N messages
- États inline évitent messages `UPD` séparés

---

## Roadmap_PROTOCOL_V4

Axes envisagés :
- **Contexte persistant** : `CTX_ID` pour conversations longues
- **Compression payload** : dictionnaire partagé `$1`=terme fréquent
- **Batch messages** : `[MSG_01;MSG_02;MSG_03]` en une ligne
- **Métadonnées** : timestamps compacts, TTL
- **Retry intégré** : `RETRY=n` dans erreurs
- **Hiérarchie agents** : `O1.W1.W1a` pour sous-workers

---
---

# PROTOCOL_V4 - Data-Layer Robuste Multi-Agents

## Objectif V4

Data-layer industrialisé pour systèmes multi-agents à grande échelle.
Cibles : schéma figé, validation stricte, scalabilité N agents, token-efficiency maximale.
Compatibilité : V3 subset valide.

---

## 1. Objectif

Coordination N agents IA. Schéma rigide. Validation automatisable. Tokens minimaux.

---

## 2. Modèle d'agents et routage

### 2.1 Format ID agent

```
<ROLE><NUM>[.<SUB>]
```

| Pattern | Description | Max |
|---------|-------------|-----|
| `O<1-9>` | Orchestrator | 9 |
| `W<1-99>` | Worker | 99 |
| `R<1-9>` | Router/Relay | 9 |
| `G<1-9>` | Groupe logique | 9 |

**Exemples :** `O1`, `W12`, `R1`, `G1`, `O1.W1` (hiérarchie)

### 2.2 Routage

| Pattern | Signification |
|---------|---------------|
| `O1>W1` | Direct unicast |
| `O1>G1` | Groupe (tous membres G1) |
| `O1>*` | Broadcast global |
| `O1>W*` | Broadcast workers |
| `W1>O1` | Réponse au caller |

### 2.3 Anti-collision IDs

- IDs assignés séquentiellement par `O1`
- Nouveau worker : `O1` envoie `MSG|O1>Wn|A|-|-|-|ID=Wn`
- Collision détectée → `E11:ID_CONFLICT`

---

## 3. Format des messages V4

### 3.1 Schéma monoligne

```
MSG|FROM>TO|TYPE|TASK|PRI|STATE|ERR|DATA
```

### 3.2 Spécification segments

| # | Segment | Oblig. | Format | Valeurs | Max len |
|---|---------|--------|--------|---------|---------|
| 1 | `MSG` | Oui | `M<1-9999>` | - | 5 |
| 2 | `ROUTE` | Oui | `<ID>><ID>` | voir §2.2 | 10 |
| 3 | `TYPE` | Oui | char | `R,S,C,U,A,E,B,H` | 1 |
| 4 | `TASK` | Oui | `T<1-999>` ou `-` | - | 4 |
| 5 | `PRI` | Non | `P<0-2>` ou `-` | `P0,P1,P2` | 2 |
| 6 | `STATE` | Non | char ou `-` | `N,R,D,F,X` | 1 |
| 7 | `ERR` | Non | `E<01-99>` ou `-` | voir §4.3 | 3 |
| 8 | `DATA` | Oui | texte | - | 200 |

**Délimiteurs :**
- Segments : `|`
- Routage : `>`
- Data structuré : `k=v;k=v`
- Interdit dans DATA : `|`, `>`

### 3.3 Types de messages V4

| Type | Nom | Usage |
|------|-----|-------|
| `R` | Request | Assignation tâche |
| `S` | Response | Résultat tâche |
| `C` | Clarify | Question/clarification |
| `U` | Update | Progression |
| `A` | Ack | Accusé réception |
| `E` | Error | Erreur |
| `B` | Broadcast | Info tous agents |
| `H` | Heartbeat | Santé agent |

---

## 4. Priorités, états, erreurs

### 4.1 Priorités

| Code | Niveau | SLA implicite | Action |
|------|--------|---------------|--------|
| `P0` | Critique | Immédiat | Interrompt tout |
| `P1` | Élevé | < 1 cycle | File prioritaire |
| `P2` | Modéré | Best effort | File standard |

**Règles scheduling :**
- `P0` préempte `P1`/`P2` en cours (sauf atomique)
- Worker surchargé : `E06:BUSY;queue=n`
- Demande baisse priorité : `C` avec `suggest=P2`

### 4.2 États et transitions

```
     ┌──────┐
     │  N   │ (New)
     └──┬───┘
        │ R (Request reçu)
        ▼
     ┌──────┐
     │  R   │ (Running)
     └──┬───┘
        │
   ┌────┴────┐
   ▼         ▼
┌──────┐  ┌──────┐
│  D   │  │  F   │
│(Done)│  │(Fail)│
└──────┘  └──────┘
        ▲
        │ (annulation)
     ┌──────┐
     │  X   │ (Cancelled)
     └──────┘
```

**Transitions valides :**
- `N` → `R` (démarrage)
- `R` → `D` (succès)
- `R` → `F` (échec)
- `N|R` → `X` (annulation)

### 4.3 Codes erreur catégorisés

| Cat. | Codes | Description |
|------|-------|-------------|
| **Parsing** | `E01-E05` | Format, structure |
| **Ressource** | `E06-E09` | Indispo, saturé |
| **Protocole** | `E10-E15` | Version, routing |
| **Timeout** | `E20-E25` | Délais dépassés |
| **Autre** | `E99` | Non catégorisé |

| Code | Signification |
|------|---------------|
| `E01` | Fichier introuvable |
| `E02` | Format DATA invalide |
| `E03` | Segment manquant |
| `E04` | Valeur hors plage |
| `E05` | Parsing échoué |
| `E06` | Agent saturé (BUSY) |
| `E07` | Ressource indisponible |
| `E08` | Agent inconnu |
| `E09` | Tâche inconnue |
| `E10` | Priorité invalide |
| `E11` | ID collision |
| `E12` | Version protocole incompatible |
| `E13` | Route invalide |
| `E14` | Type message inconnu |
| `E15` | État transition invalide |
| `E20` | Timeout global |
| `E21` | Timeout réponse |
| `E22` | Timeout heartbeat |
| `E99` | Autre |

---

## 5. Règles tokens V4

1. **IDs compacts** : `M1` au lieu de `MSG_01`, `T1` au lieu de `TASK_01`
2. **Segments optionnels** : `-` si non utilisé
3. **DATA max 200 chars** : au-delà → référence externe
4. **Pas de répétition** : référencer par ID
5. **Broadcast** : `*` évite N messages
6. **Heartbeat** : 1 msg/cycle, pas de flood
7. **Batch implicite** : plusieurs DATA via `;` (ex: `k1=v1;k2=v2`)

**Format ultra-compact :**
```
M1|O1>W1|R|T1|-|-|-|action
```
(8 segments, ~25 chars)

---

## 6. Validation et robustesse

### 6.1 Checklist parsing (côté agent)

Avant traitement, valider :

| # | Vérification | Rejet si |
|---|--------------|----------|
| 1 | 8 segments `|` | ≠8 → `E03` |
| 2 | `MSG` format `M\d{1,4}` | invalide → `E05` |
| 3 | `ROUTE` format `<ID>><ID|*>` | invalide → `E13` |
| 4 | `TYPE` ∈ `{R,S,C,U,A,E,B,H}` | invalide → `E14` |
| 5 | `TASK` format `T\d{1,3}` ou `-` | invalide → `E05` |
| 6 | `PRI` ∈ `{P0,P1,P2,-}` | invalide → `E10` |
| 7 | `STATE` ∈ `{N,R,D,F,X,-}` | invalide → `E15` |
| 8 | `ERR` format `E\d{2}` ou `-` | invalide → `E05` |
| 9 | `DATA` len ≤ 200 | > → tronquer + warn |
| 10 | Pas de `|` ou `>` dans DATA | présent → `E02` |

### 6.2 Comportement sur erreur

| Situation | Action |
|-----------|--------|
| Parsing fail | Répondre `E|E05:seg=n` |
| Agent inconnu | Répondre `E|E08:id=Wn` |
| Version incomp. | Répondre `E|E12:v=3` |
| Timeout | Répondre `E|E21` après délai |
| État invalide | Répondre `E|E15:N>D` |

### 6.3 Compatibilité descendante

| Version source | Adaptation V4 |
|----------------|---------------|
| V3 (7 seg) | Ajouter `ERR=-` en pos 7 |
| V2 (5 seg) | Ajouter `PRI=-;STATE=-;ERR=-` |

---

## 7. Exemples V4

### Assignation P0 multi-agents

```
M1|O1>W1|R|T1|P0|N|-|analyser logs critiques
```

### Réponse succès

```
M2|W1>O1|S|T1|P0|D|-|3 erreurs
```

### Surcharge worker

```
M3|W1>O1|E|T2|-|-|E06|BUSY;queue=5
```

### Refus priorité

```
M4|W2>O1|C|T3|P0|R|-|suggest=P1;reason=load
```

### Erreur parsing

```
M5|W1>O1|E|-|-|-|E05|seg=3;got=X
```

### Agent injoignable

```
M6|R1>O1|E|T4|-|-|E08|id=W3;last=120s
```

### Broadcast maintenance

```
M7|O1>*|B|-|P1|-|-|maintenance 5min
```

### Heartbeat

```
M8|W1>O1|H|-|-|R|-|load=45%;queue=2
```

### Annulation avec ack

```
M9|O1>W2|U|T5|-|X|-|annulé
```
```
M10|W2>O1|A|T5|-|-|-|ok
```

### Batch data structuré

```
M11|W1>O1|S|T6|P1|D|-|files=3;errors=0;size=1.2MB
```

---

## Diff_V3_V4

**Ajouts :**
- Segment `ERR` dédié (position 7)
- IDs compacts : `M1`, `T1` au lieu de `MSG_01`, `TASK_01`
- Type `H` (Heartbeat)
- Rôle `R` (Router), `G` (Groupe)
- Codes erreur : `E11-E15`, `E20-E22`
- Catégorisation erreurs
- State machine documentée
- Longueurs max par segment
- Checklist validation complète
- Compatibilité descendante explicite

**Modifications :**
- Format : 7 → 8 segments
- `MSG_XX` → `M<n>`, `TASK_XX` → `T<n>`
- DATA max : illimité → 200 chars
- Erreur inline `Exx:desc` → segment `ERR` + `DATA` séparés

**Suppressions :**
- Verbosité IDs (`MSG_`, `TASK_`)

**Gains :**
- ~20% tokens/message vs V3
- Parsing déterministe
- Erreurs actionnables

---

## Roadmap_PROTOCOL_V5

### Objectif V5

Superset discipliné de V4. Focus : sécurité, traçabilité, extensibilité contrôlée.
Contrainte : pas d'explosion tokens, compatibilité V4 stricte.

---

### Axes stratégiques

#### 1. Sécurité & authentification légère

| Élément | Description | Format envisagé |
|---------|-------------|-----------------|
| `SIG` | Signature courte (HMAC-SHA256 tronqué) | 8 chars hex |
| `SID` | Session ID | `S<1-999>` |
| `NONCE` | Anti-replay | 4 chars |
| `SYS` | Flag message système vs applicatif | `0`/`1` |

**Règles :**
- Segment optionnel `AUTH` = `SID:NONCE:SIG`
- Messages `SYS=1` : contrôle protocole, non routables
- Clé partagée pré-établie hors-bande

#### 2. Traçabilité & observabilité

| Élément | Description | Format envisagé |
|---------|-------------|-----------------|
| `TID` | Trace ID (corrélation distribuée) | `X<1-9999>` |
| `PID` | Parent ID (chaînage causal) | `M<n>` référence |
| `TS` | Timestamp compact | epoch mod 86400 (5 chars) |

**Règles :**
- `TID` propagé sur toute chaîne de messages liés
- `PID` optionnel, référence `MSG` parent direct
- Logs reconstruits post-hoc via `TID`+`PID`

#### 3. Routage avancé

| Pattern | Description |
|---------|-------------|
| `G<n>` | Groupe logique (cluster) |
| `@role` | Routage par rôle dynamique |
| `O1>G1>W*` | Fan-out multi-niveau |
| `W*>O1` | Fan-in agrégation |

**Règles :**
- Groupes définis par `O1` via `B` broadcast
- Appartenance dynamique : `JOIN`/`LEAVE` dans DATA
- Pattern fan-out : 1 message → N destinations

#### 4. Encodage DATA avancé

| Mode | Description | Exemple |
|------|-------------|---------|
| `$n` | Référence dictionnaire partagé | `$1`=analyser, `$2`=fichier |
| `#ref` | Pointeur contexte externe | `#CTX42` |
| `~zip` | Compression base64 courte | `~eJxz...` |

**Règles :**
- Dictionnaire synchronisé via `B` au démarrage
- `#ref` : DATA = ID externe, contenu stocké ailleurs
- Mode `~zip` : payload > 100 chars uniquement

#### 5. Gestion versions & compatibilité

| Mécanisme | Description |
|-----------|-------------|
| `VER` | Champ version protocole optionnel | `V4`, `V5` |
| Négociation | Handshake initial `H` avec `VER=max` |
| Fallback | Si `VER` incompatible → `E12` + downgrade |

**Règles :**
- V5 agent comprend V4 nativement
- V4 agent ignore champs V5 inconnus (graceful)
- Version explicite uniquement si mismatch détecté

---

### Format V5 envisagé (draft)

```
M<n>|FROM>TO|TYPE|TASK|PRI|STATE|ERR|AUTH|TRACE|DATA
```

| # | Segment | Oblig. | Nouveau V5 |
|---|---------|--------|------------|
| 1-7 | (=V4) | Oui | - |
| 8 | `AUTH` | Non | `SID:NONCE:SIG` ou `-` |
| 9 | `TRACE` | Non | `TID:PID:TS` ou `-` |
| 10 | `DATA` | Oui | + modes `$n`, `#ref`, `~zip` |

**Compatibilité V4 :** segments 8-9 = `-|-` → message V4 valide.

---

### Exemples V5 (preview)

**Message authentifié + tracé :**
```
M1|O1>W1|R|T1|P0|N|-|S1:A3F2:8B4C1D2E|X1:-:14523|$1 logs
```

**Fan-out groupe :**
```
M2|O1>G1|B|-|P1|-|-|-|X1:M1:14530|maintenance 5min
```

**Référence externe :**
```
M3|W1>O1|S|T1|P0|D|-|-|X1:M1:14545|#CTX42
```

---

### Roadmap_PROTOCOL_V6+ (vision)

Axes lointains :
- **Chiffrement** : payload chiffré E2E (clé session)
- **Multi-tenant** : namespace agents `NS1.O1`
- **QoS** : garanties de livraison, retries natifs
- **Streaming** : messages fragmentés pour gros payloads

---
---

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
- Segments 9-11 ajoutés (DEPTH, CTX, BUDGET)
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

**11 segments** séparés par `|`.

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
