---
name: oddly-video
description: Produce a new "Oddly Logical Science" YouTube video (script + footage + episode JSON) and have GitHub Actions render it. Use whenever the user asks for a new video, episode, topic or improvement of the channel's videos. Token-frugal process v3.
---

# Oddly Logical Science — processus v3 « express » (11 oct. 2026)

Le message de l'utilisateur peut se limiter à « vidéo » (ou « vidéo : <sujet> »). Tout le reste est autonome, sans validation intermédiaire.

## Budget (règle n°1)
- L'orchestrateur (toi) ne lit QUE : `channels/oddly-logical/RULES.md`, `VIDEOS.md`, `TOPICS.md`. Jamais FEEDBACK.md (archive), jamais engine/*.py sauf panne.
- Le travail lourd (recherche d'images, lecture des planches, écriture, relecture) est fait par les agents sonnet. L'orchestrateur ne regarde AUCUNE image sauf la miniature finale et la planche `_review.jpg` finale (1 coup d'œil chacune).
- 1 rendu par vidéo. 2e rendu seulement pour une erreur bloquante, et via `from_run` si le montage n'a pas changé. Jamais de 3e rendu : livrer en signalant le défaut.
- Moteur figé pendant une production. Une amélioration moteur = conversation dédiée.
- Réponses à l'utilisateur : 5 lignes max.

## Déroulé (1 conversation = 1 vidéo, sur une branche `claude/<slug>` partie de `origin/main`)
1. `git fetch origin main` ; lire RULES/VIDEOS/TOPICS ; choisir le sujet (rotation des thèmes, angle TOI ou mystère vrai).
2. Agent **oddly-footage** : lance le workflow Scout (commande ci-dessous), lit la planche, rend une liste blanche d'URL (sujet exact, HD, pas de doublon). Si rien de spectaculaire → il le dit, on change de sujet.
3. Agent **oddly-scriptwriter** : écrit l'épisode JSON sur la liste blanche uniquement (+ `youtube`, `thumbnail`, `shorts`).
4. Agent **oddly-factchecker** : corrige directement les points bloquants. Puis `python3 engine/check_episode.py <fichier>`.
5. Agent **oddly-translator** si le quota le permet (champ `dub`), sinon on saute.
6. Push → GitHub Actions rend tout (vidéo, miniature, srt, Shorts, kit SEO, CONSIGNES_CHROME). Attendre la fin avec `sleep`/polling espacé (≥ 5 min), sans lire les logs sauf échec (tail 25).
7. Coup d'œil miniature + `_review.jpg` (branche `review/<run_id>`). Puis : ligne dans VIDEOS.md, sujet coché dans TOPICS.md, PR + fusion dans main, ajout à `PACKS.md`.
8. Livrer à l'utilisateur : lien de l'artefact + date de programmation proposée. Rien d'autre.

## Mise en ligne (conversation séparée, Claude dans Chrome)
Le pack contient `<nom>_CONSIGNES_CHROME.md` : l'utilisateur télécharge l'artefact, puis dit à Claude dans Chrome « mets en ligne selon les consignes ». Aucune réflexion à refaire.

## Commandes utiles
- Scout : `gh api -X POST repos/sebastien311984-bot/youtube-studio/actions/workflows/scout.yml/dispatches -f ref=main -f "inputs[queries]=commons:<q>|nasa:<q>|archive:<q>|pixabay:<q>"` puis `gh api "repos/sebastien311984-bot/youtube-studio/actions/workflows/scout.yml/runs?per_page=1"` et `gh run download <id> -R sebastien311984-bot/youtube-studio -n scout` (`candidates.json` + `sheet.jpg`).
- Artefact : `gh api repos/sebastien311984-bot/youtube-studio/actions/runs/<id>/artifacts` → lien `https://github.com/sebastien311984-bot/youtube-studio/actions/runs/<RUN_ID>/artifacts/<ARTIFACT_ID>`.
- Reprise sans re-rendu : dispatch `render-videos.yml` avec `inputs[from_run]=<id>`.
- Ne jamais annuler un rendu d'une autre branche (filtrer par `head_branch`).

## Références
- Format des scènes et options du moteur : `engine/REFERENCE.md`.
- Sources légales : `channels/oddly-logical/SOURCES.md`. Publication : `channels/oddly-logical/PUBLISHING.md`.
