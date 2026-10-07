---
name: oddly-video
description: Produce a new "Oddly Logical Science" YouTube video (script + footage + episode JSON) and have GitHub Actions render it. Use whenever the user asks for a new video, episode, topic or improvement of the channel's videos. Token-frugal process.
---

# Oddly Logical Science — processus de production (v2, à faire évoluer)

## Continuité entre discussions (à faire en premier et en dernier)
- Début : `git fetch origin main` puis partir de `origin/main` (mémoire à jour : FEEDBACK, VIDEOS, TOPICS, SOURCES, moteur, agents).
- Fin (et après chaque amélioration du process) : PR vers main + fusion, pour que les autres discussions en profitent. Plusieurs discussions en parallèle : fusionner souvent, petits changements.
- Toute leçon apprise va dans FEEDBACK.md (jamais seulement dans la conversation).

## Esprit (à lire en premier)
- **Réfléchir avant d'appliquer** : les règles ci-dessous sont la mémoire des erreurs passées, pas un script. Aucune vidéo n'est « la référence » à copier ; chaque sujet mérite ses propres choix. Si une règle produit un résultat absurde pour ce sujet, le jugement l'emporte (et on le note dans FEEDBACK).
- **Pixabay interdit** (sauf accord explicite) : uniquement sources officielles/archives. Un sujet sans vraies images disponibles = mauvais sujet → en choisir un autre (en alternant les thèmes).
- **Penser à tout, en chef de projet** : anticiper ce qui peut bloquer (branche non fusionnée, fichiers perdus, droits, licences, quotas, YouTube), le régler ou le signaler AVANT que l'utilisateur le découvre.
- Les listes ci-dessous sont une **boîte à outils, pas un gabarit**. Ne jamais cocher des cases : chaque vidéo part d'une vraie idée de réalisateur.
- Avant d'écrire, se poser 3 questions et les écrire en 3 lignes dans le brief à l'agent : **Quelle émotion ? Quelle image inoubliable ? Qu'est-ce qui rend CETTE vidéo différente des précédentes ?** Le style (rythme, couleurs, formats, musique) découle des réponses.
- Les règles techniques (plans, courbes, longueurs) sont dans le code : `engine/check_episode.py` avant chaque push, et le moteur se protège seul. Inutile de les répéter dans les consignes.
- En cas de doute : moins d'effets, mieux choisis. Relire le résultat comme un spectateur, pas comme un contrôleur.

## Déroulé d'une vidéo (« machine de guerre »)
1. Lire `channels/oddly-logical/FEEDBACK.md` (prioritaire) et prendre le premier sujet non fait dans `channels/oddly-logical/TOPICS.md`.
2. Déléguer l'écriture à l'agent **oddly-scriptwriter** (modèle sonnet, moins coûteux) : il cherche les plans et écrit `channels/oddly-logical/episodes/<slug>.json`.
3. Déléguer la relecture à l'agent **oddly-factchecker**, puis corriger les points [BLOCKING] (petites modifications).
4. Pousser l'épisode : GitHub Actions fait le rendu (vidéo, miniature, sous-titres, kit SEO, Shorts).
5. À la notification, donner le lien de l'artefact et le texte à copier-coller pour YouTube Studio.
6. Mettre à jour `channels/oddly-logical/VIDEOS.md` à chaque étape (écrite, rendue avec le lien, programmée, publiée, stats). Noter le retour de l'utilisateur dans `FEEDBACK.md` et cocher le sujet dans `TOPICS.md`. **C'est la mémoire de la chaîne.**

Chaîne YouTube en anglais : science spectaculaire (espace, Terre, océans, animaux).
Objectif : un rendu cinématographique, rythmé et **monétisable** (pas de « contenu réutilisé »).

## Stratégie de croissance (prioritaire, 2026-10-07)
1. **Angle TOI** : chaque sujet est formulé autour du spectateur (« What Happens to Your Body… », « Could You Survive… », « What If You… »). Choisir d'abord dans la section « TOI » de TOPICS.md.
2. **Shorts d'abord** : chaque vidéo longue → 3 Shorts de 30-58 s (accroche + révélation + chute), publiés après la longue, étalés (1/jour). Un Short peut aussi être produit seul (épisode court dédié).
3. **Actualité** : vérifier au début de chaque conversation s'il y a une actu science forte (NASA/ESA/NOAA/USGS, JWST, astéroïde, éruption, tempête solaire). Si oui, elle passe devant : vidéo de 6-8 min + Shorts en < 48 h, avec les images officielles du communiqué (domaine public NASA/NOAA/USGS ; ESA/ESO en CC BY à créditer). Titre = mot-clé de l'actu + angle TOI.
4. **Mesure** : noter CTR et rétention à 30 s dans VIDEOS.md 48 h après chaque publication ; bilan après ~20 vidéos.
5. **Plus tard** : version française (piste audio YouTube ou 2e chaîne).

## International (doublage)
- Après relecture, l'agent **oddly-translator** ajoute le champ `dub` (es, pt, hi, fr, de, ar). Le rendu produit `<nom>_<langue>.m4a` (voix native + même musique, calée sur le minutage) et `<nom>_timing.json`.
- Dans YouTube Studio : vidéo → Langues → Ajouter → Piste audio (fichier .m4a), + titre/description traduits. Les pistes s'ajoutent aussi à une vidéo déjà publiée.
- Textes à l'écran restent en anglais pour l'instant.

## Repérage d'images (réseau)
Depuis Claude, seuls NASA et Internet Archive répondent (Wikimedia limite, USGS bloque). Pour Commons/USGS/NOAA (souvent sur Commons) : lancer le workflow **Scout footage** : `gh api -X POST repos/sebastien311984-bot/youtube-studio/actions/workflows/scout.yml/dispatches -f ref=main -f "inputs[queries]=commons:volcano eruption filetype:video|nasa:lava|archive:volcano"` (GraphQL interdit : pas de `gh workflow run`), id via `gh api repos/.../actions/workflows/scout.yml/runs?per_page=1`, puis `gh run download <id> -R sebastien311984-bot/youtube-studio -n scout` (~1 min) : `candidates.json` (URL, licence, auteur) + `sheet.jpg` numérotée à regarder. Le rendu GitHub télécharge ensuite ces URL sans problème.

## Contrôle qualité (jugement, pas case à cocher)
**Cause n°1 des plans hors sujet** : remplir une phrase abstraite avec une photo « à peu près ». Solution : infographie maison.
Se mettre à la place d'un spectateur exigeant qui découvre la vidéo sur YouTube :
- **Miniature** : est-ce que je cliquerais ? Sujet net et fort, 2-3 mots, contraste. Sinon la refaire.
- **Ouverture** : les premières secondes montrent-elles le sujet et donnent-elles envie de rester ?
- **Chaque plan** : montre-t-il vraiment ce que dit la voix ? (outils : `engine/storyboard.py` avant rendu, `_review.jpg` après). « À peu près » = remplacer.
- **Son** : musique et effets au service de l'histoire ; voix doublées vivantes.
- **Technique** : `engine/check_episode.py` avant push.
Avant livraison, noter en une ligne dans VIDEOS.md ce qui a été regardé et ce qui reste faible, et le dire honnêtement à l'utilisateur.

## Règle d'or : économiser les tokens
- **Ne jamais faire de rendu complet en local.** On pousse l'épisode JSON, et GitHub Actions fait le rendu (0 token).
- Tester en local seulement des **images fixes** d'un élément nouveau (1 frame par ffmpeg), jamais une vidéo entière.
- Ne pas télécharger les plans en local : les épisodes référencent les **URL**.
- Pas d'allers-retours inutiles : écrire l'épisode complet en une passe, pousser, attendre la notification de fin de rendu, donner le lien.
- Le travail par vidéo se limite à : choisir le sujet → chercher les plans (`find_footage.py`) → écrire `channels/oddly-logical/episodes/<slug>.json` → pousser.

## Fichiers
- `engine/render.py` : moteur (voix, plans, sous-titres, titres, musique, mixage).
- `engine/visuals.py` : plans générés (intro, schéma dessiné au crayon, chiffre choc).
- `engine/find_footage.py "sujet"` : liste les MP4 HD domaine public de la NASA (SVS) avec leurs URL. `engine/find_footage.py --commons "sujet"` : vidéos Wikimedia Commons (licence et auteur à créditer dans la description).
- `channels/oddly-logical/SOURCES.md` : catalogue des sources légales (NASA, Pixabay, Wikimedia, NOAA, USGS, ESA, ESO…) avec licences et crédits.
- `channels/oddly-logical/brand/` : intro (4 s) et écran de fin (15 s) réutilisables.
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
| plan réel Pixabay | `clip` = `"pixabay:requête en anglais"` (filtrée : tags pertinents, vrais films ; sinon plan retiré) ou `"pixabay:id:12345"` (plan choisi sur la planche du scout, recommandé) | nature, océans, animaux, météo : la vidéo HD est cherchée et téléchargée au rendu (secret GitHub PIXABAY_API_KEY), sans attribution obligatoire. Requêtes précises (« octopus underwater close up »). |
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
- `tone` : ton de la voix (neutral, calm, tense, urgent, reveal, warm) ; par défaut reveal sur stat/kinetic/rank, tense sur quiz, calm sur timeline, warm sur diagram. La voix est aussi « réchauffée » automatiquement (EQ, compression, légère pièce).
- `transition` : facultatif (fade, smoothleft, circleopen, fadeblack, zoomin, slideup, fadewhite, dissolve, radial…). Par défaut, le moteur alterne automatiquement.

Ajouts automatiques du moteur : barre de progression dorée avec repères de chapitres, encart « SUBSCRIBE » à 30 % de la durée (réglable avec `subscribe_at`), Shorts verticaux (`shorts` : [{from, to, title}], indices de scènes, 58 s maximum ; par défaut, l'accroche).
- `title` [grand, petit] : titre plein écran.

## Comment penser une vidéo (principes, pas quotas)
Aucun chiffre de cette page n'est un objectif à remplir. On part de l'histoire, pas d'une grille.
1. **Une question que le spectateur se pose vraiment**, posée dès les premières secondes sur l'image la plus forte du sujet, et une réponse donnée au compte-gouttes jusqu'à la fin.
2. **Chaque scène doit mériter sa place** : elle apprend quelque chose, surprend ou fait monter la tension. Sinon on la coupe. La durée = ce que l'histoire porte, pas une cible.
3. **Le visuel suit le sens** : on montre la chose réelle quand elle existe en image ; on dessine (schéma, chiffre, frise, mots chocs) quand c'est une idée. Jamais d'image « d'ambiance » pour boucher un trou.
4. **Les formats du moteur sont des outils** (quiz, versus, timeline, encarts, chapitres, teasers…) : on en utilise un quand il sert l'histoire, pas pour cocher une variété.
5. **Relire comme un spectateur exigeant** : est-ce que je m'ennuie, est-ce que je doute d'une image, est-ce que je cliquerais ? Corriger avant de livrer.
6. **Faits exacts et prudents**, crédits dans `credits`.

## Pistes d'amélioration du moteur (à faire plus tard, par ordre de priorité)
1. Variantes de style des infographies : palettes par thème (Soleil = orange, espace profond = violet, Terre = bleu).
2. ~~Riser et silence avant les révélations~~ (fait : automatique avant stat, rank, kinetic, quiz et title). Reste à faire : varier les « hits » et les whooshes.
3. Nouveaux formats : carte du monde animée, globe qui tourne, « split timeline » passé/futur, compte à rebours plein écran.
4. Vraie main qui dessine pour les schémas.
5. Miniature : 3 variantes générées par vidéo, pour les tests A/B de YouTube.

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
Titre court qui donne envie de cliquer, description avec chapitres horodatés et crédits, tags pertinents, miniature forte (une image choc et 2 ou 3 mots).

## Historique et améliorations
- v0 : voix Edge TTS, sous-titres mot à mot, travellings, fondus, musique synthétisée avec ducking.
- v1 : intro cinématique, schémas dessinés au crayon, chiffres chocs, plusieurs plans par scène, encarts « Did you know? », cartons de chapitre, plans courts bouclés.
- Idées suivantes : vraie main qui dessine, barre de progression et teaser « coming up », cartes animées, versions Shorts verticales automatiques, voix ElevenLabs, miniature générée automatiquement.

## Feuille de route « être vu et cité » (à mettre en place progressivement)
- Style adapté au sujet : champ `theme` (palette, musique, rythme, transitions) par épisode — priorité moteur n°1.
- Découverte : titre = mot-clé recherché + curiosité ; 3 miniatures A/B ; Short publié APRÈS la longue (quelques heures à 1 jour) : le lien « Vidéo associée » n'accepte qu'une vidéo déjà en ligne ; playlists thématiques ; écran de fin vers la vidéo la plus proche.
- Google / IA (être cité) : chapitres-questions, phrase-réponse nette, chiffres sourcés dits à voix haute, description avec résumé + FAQ + sources (NASA, NOAA, études), SRT exact, page/article compagnon possible plus tard.
- Rétention : cold open, fausse fin, « pattern interrupt » toutes les 20-30 s (zoom, son, changement de format), boucle ouverte résolue à la fin.
- Engagement : question précise épinglée en commentaire, sondage communauté, réponse aux premiers commentaires dans l'heure.
- Qualité cinéma : sound design par thème (grondement grave pour les abysses), étalonnage par thème, cartes et globes animés, compte à rebours, vraie main qui dessine.
- Publication (ordre) : longue → Short quelques heures après avec « Vidéo associée » → commentaire épinglé (question) → ajout à la playlist du thème → écran de fin + fiches (cards) vers 1-2 vidéos proches → post Communauté (sondage) 1-2 jours après.
- Autres astuces : langue audio et titre/description traduits (FR, ES, PT, DE, HI) ; catégorie « Science & Technology » ; lieu et « contenu altéré/synthétique » renseignés honnêtement ; premiers 200 caractères de la description = résumé avec mot-clé ; tags « dérivés » (questions longues) ; 1 Short par chapitre fort (2-3 par vidéo) étalés sur la semaine ; republier les meilleurs passages en Shorts « réponse à un commentaire » ; analyser la rétention à 30 s et le CTR après 48 h et noter la leçon dans FEEDBACK.md.
- Qualité : voix plus expressive (pauses, emphase) ; musique qui monte avant chaque révélation et silence juste avant ; plans jamais répétés ; vérifier chaque plan Pixabay (aperçu 1 image par plan dans l'artefact) avant validation.
