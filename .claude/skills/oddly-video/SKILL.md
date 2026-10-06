---
name: oddly-video
description: Produce a new "Oddly Logical Science" YouTube video (script + footage + episode JSON) and have GitHub Actions render it. Use whenever the user asks for a new video, episode, topic or improvement of the channel's videos. Token-frugal process.
---

# Oddly Logical Science — processus de production (v2, à faire évoluer)

## Déroulé d'une vidéo (« machine de guerre »)
1. Lire `channels/oddly-logical/FEEDBACK.md` (prioritaire) et prendre le premier sujet non fait dans `channels/oddly-logical/TOPICS.md`.
2. Déléguer l'écriture à l'agent **oddly-scriptwriter** (modèle sonnet, moins coûteux) : il cherche les plans et écrit `channels/oddly-logical/episodes/<slug>.json`.
3. Déléguer la relecture à l'agent **oddly-factchecker**, puis corriger les points [BLOCKING] (petites modifications).
4. Pousser l'épisode : GitHub Actions fait le rendu (vidéo, miniature, sous-titres, kit SEO, Shorts).
5. À la notification, donner le lien de l'artefact et le texte à copier-coller pour YouTube Studio.
6. Mettre à jour `channels/oddly-logical/VIDEOS.md` à chaque étape (écrite, rendue avec le lien, programmée, publiée, stats). Noter le retour de l'utilisateur dans `FEEDBACK.md` et cocher le sujet dans `TOPICS.md`. **C'est la mémoire de la chaîne.**

Chaîne YouTube en anglais : science spectaculaire (espace, Terre, océans, animaux).
Objectif : un rendu cinématographique, rythmé et **monétisable** (pas de « contenu réutilisé »).

## Règle d'or : économiser les tokens
- **Ne jamais faire de rendu complet en local.** On pousse l'épisode JSON, et GitHub Actions fait le rendu (0 token).
- Tester en local seulement des **images fixes** d'un élément nouveau (1 frame par ffmpeg), jamais une vidéo entière.
- Ne pas télécharger les plans en local : les épisodes référencent les **URL**.
- Pas d'allers-retours inutiles : écrire l'épisode complet en une passe, pousser, attendre la notification de fin de rendu, donner le lien.
- Le travail par vidéo se limite à : choisir le sujet → chercher les plans (`find_footage.py`) → écrire `channels/oddly-logical/episodes/<slug>.json` → pousser.

## Fichiers
- `engine/render.py` : moteur (voix, plans, sous-titres, titres, musique, mixage).
- `engine/visuals.py` : plans générés (intro, schéma dessiné au crayon, chiffre choc).
- `engine/find_footage.py "sujet"` : liste les MP4 HD domaine public de la NASA (SVS) avec leurs URL.
- `channels/oddly-logical/episodes/*.json` : un fichier par vidéo. Pousser un fichier nouveau ou modifié déclenche le rendu.
- `.github/workflows/render-videos.yml` : rendu automatique ; le MP4 est dans l'artefact `videos` de l'exécution.
- `channels/oddly-logical/AUDIT.md` : audit des sources d'images et stratégie de la chaîne.

## Récupérer la vidéo pour l'utilisateur
Après le push, attendre la notification de fin de rendu, puis récupérer l'exécution et son artefact avec `mcp__github__actions_list` (list_workflow_runs, puis list_workflow_run_artifacts).
Dépôt : sebastien311984-bot/youtube-studio. Lien à donner : `https://github.com/sebastien311984-bot/youtube-studio/actions/runs/<RUN_ID>/artifacts/<ARTIFACT_ID>`.
En cas d'échec : `mcp__github__get_job_logs` (tail 25 lignes), corriger, re-pousser.

## Format d'un épisode (JSON)
```json
{"title": "...", "voice": "en-US-AndrewMultilingualNeural", "credits": "Footage: NASA ...",
 "scenes": [ {scène}, ... ]}
```
Types de scènes (`kind`) :
| kind | champs | usage |
|---|---|---|
| `intro` | `min` (environ 4) | intro cinématique avec logo, toujours en 1re position |
| (aucun) = plan réel | `clip` (URL), `start`, `move` (in/out/left/right) **ou** `shots` = liste de {clip,start,move} | images réelles ; utiliser `shots` pour couper toutes les 3-5 s |
| `diagram` | `heading`, `elements` | schéma dessiné au crayon sur papier (line, arrow, circle, arc, curve, text, drops) ; coordonnées sur 1920x1080 ; couleurs : ink, red, orange, blue, gold, green |
| `stat` | `value`, `prefix`, `suffix`, `caption` | chiffre choc plein écran (compteur animé, décimales possibles) |
| `scale` | `heading`, `items` [{label, size (relative), color, note}] | comparaison d'échelle, cercles côte à côte |
| `timeline` | `heading`, `events` [{year, text}] (retour à la ligne = vrai saut de ligne `\n` en JSON, PAS `\\N`) | frise chronologique animée |
| `versus` | `heading`, `left`/`right` {name, color, stats[]} | écran partagé VS |
| `quiz` | `question`, `options` (2 à 4), `answer` (index), `min` ≥ 6 | quiz avec compte à rebours de 3 s, réponse révélée (engagement) |
| `kinetic` | `words` [3 à 6 mots] | typographie choc, mot par mot |
| `rank` | `number`, `title_rank`, `sub` | carton « #3 » pour les vidéos Top N |
| plan réel avec photo | `clip` = URL .jpg/.png | photo NASA animée par un travelling ; la NASA a des dizaines de milliers d'images |

Couleurs disponibles : gold, red, blue, green, purple, white, orange.

Options communes à toutes les scènes :
- `text` : voix off ; la durée de la scène suit la voix.
- `min` : durée minimale.
- `lead` : délai avant la voix (1,2 s si la scène a un `chapter`).
- `label` [titre, sous-titre] : bandeau d'information en haut à gauche.
- `fact` : encart « DID YOU KNOW? » ; retour à la ligne avec `\\N`, 2 lignes de 45 caractères maximum.
- `chapter` ["CHAPTER 1", "TITRE"] : carton de chapitre ; il compte aussi comme chapitre YouTube.
- `teaser` : « COMING UP: ... » affiché pendant les 3 dernières secondes de la scène ; à mettre juste avant chaque chapitre pour la rétention.
- `transition` : facultatif (fade, smoothleft, circleopen, fadeblack, zoomin, slideup, fadewhite, dissolve, radial…). Par défaut, le moteur alterne automatiquement.

Ajouts automatiques du moteur : barre de progression dorée avec repères de chapitres, encart « SUBSCRIBE » à 30 % de la durée (réglable avec `subscribe_at`), Shorts verticaux (`shorts` : [{from, to, title}], indices de scènes, 58 s maximum ; par défaut, l'accroche).
- `title` [grand, petit] : titre plein écran.

## Recette d'une vidéo addictive (checklist)
1. **Accroche de 0 à 10 s** : une question folle, et « NASA simulated it / the answer is terrifying ».
2. **Titre plein écran** juste après l'accroche.
3. **Des chapitres** toutes les 60 à 90 s (« CHAPTER 1 · ... ») avec une révélation chacun.
4. **Varier les formats** : plan réel → chiffre choc → schéma → plan réel. Jamais deux scènes du même type d'affilée, sauf les plans réels. **Chaque vidéo d'environ 10 min** utilise au moins 6 types différents : 1 quiz, 1 scale ou versus, 1 timeline si le sujet a une histoire, 2 à 3 diagrams, 2 à 3 stats, 1 kinetic. Environ 60 % du temps en plans réels.
4bis. **Rétention** : boucle ouverte dès l'accroche (« stay until the end for... »), teaser avant chaque chapitre, une révélation toutes les 60 à 90 s, et la promesse tenue à la fin.
5. **Un encart « Did you know? »** toutes les 45 à 60 s, avec un fait surprenant et exact.
6. **Un bandeau `label`** pour nommer chaque phénomène.
7. **Une fin** : une question au spectateur (pour les commentaires), puis abonnement et le titre « ODDLY LOGICAL SCIENCE ».
8. **Faits exacts et sourcés** ; les crédits vont dans la description YouTube.
9. **Durée cible pour monétiser** : 8 à 12 minutes, soit 25 à 40 scènes (environ 2,6 mots prononcés par seconde, soit 1 300 à 1 800 mots). Au moins 8 minutes pour pouvoir placer des pubs au milieu de la vidéo.
10. **SEO** : titre avec le mot-clé au début et un élément de curiosité ou « NASA » ; description dont les 2 premières lignes contiennent le mot-clé ; 5 chapitres ou plus ; 3 hashtags ; tags avec des variantes longues.
11. **Miniature** : 2 à 4 mots maximum, ne pas répéter le titre, une image choc à droite, un fort contraste.

## Kit YouTube généré automatiquement (engine/publish_kit.py)
Chaque rendu produit, dans l'artefact :
- `<nom>.mp4` : la vidéo ;
- `<nom>_thumb.jpg` : miniature 1280x720 (image choc agrandie et décalée à droite, texte énorme à contour, dernière ligne en jaune, pastille rouge, cercle rouge, marque) ;
- `<nom>.srt` : sous-titres anglais ; YouTube les traduit automatiquement pour l'international ;
- `<nom>_youtube.md` : titre, description SEO avec **chapitres horodatés calculés automatiquement**, crédits, hashtags, tags, traductions du titre (FR, ES, PT, DE, HI) et réglages Studio.

Champs à remplir dans l'épisode : `youtube` {title, description, tags, hashtags, translations}, `thumbnail` {scene, text (4 mots max), sub, shift, circle}, et `yt_chapter` sur les scènes qui ouvrent une partie. Un `chapter` compte aussi. YouTube exige au moins 3 chapitres d'au moins 10 s, le premier à 0:00.

## Publication YouTube
Suivre `channels/oddly-logical/PUBLISHING.md` (réglages de la chaîne, mise en ligne, horaires, actions sur 48 h, suivi des statistiques).
Publier n'est possible qu'après une connexion OAuth du compte YouTube par l'utilisateur, via une connexion « YouTube » dans Make, ou une clé OAuth en secret GitHub.
Ne jamais publier en Public sans accord explicite : envoyer d'abord en « Non répertoriée » ou « Privée », puis l'utilisateur valide.

## Livrables YouTube à donner avec chaque vidéo
Titre (moins de 60 caractères, curiosité), description avec chapitres horodatés et crédits, 10 à 15 tags, idée de miniature (une image choc et 2 ou 3 mots).

## Historique et améliorations
- v0 : voix Edge TTS, sous-titres mot à mot, travellings, fondus, musique synthétisée avec ducking.
- v1 : intro cinématique, schémas dessinés au crayon, chiffres chocs, plusieurs plans par scène, encarts « Did you know? », cartons de chapitre, plans courts bouclés.
- Idées suivantes : vraie main qui dessine, barre de progression et teaser « coming up », cartes animées, versions Shorts verticales automatiques, voix ElevenLabs, miniature générée automatiquement.
