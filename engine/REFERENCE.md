# Référence technique du moteur (lue par les agents, pas par l'orchestrateur)

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

## Kit YouTube généré automatiquement (engine/publish_kit.py)
Chaque rendu produit, dans l'artefact :
- `<nom>.mp4` : la vidéo ;
- `<nom>_thumb.jpg` : miniature 1280x720 (image choc agrandie et décalée à droite, texte énorme à contour, dernière ligne en jaune, pastille rouge, cercle rouge, marque) ;
- `<nom>.srt` : sous-titres anglais ; YouTube les traduit automatiquement pour l'international ;
- `<nom>_youtube.md` : titre, description SEO avec **chapitres horodatés calculés automatiquement**, crédits, hashtags, tags, traductions du titre (FR, ES, PT, DE, HI) et réglages Studio.

Champs à remplir dans l'épisode : `youtube` {title, description, tags, hashtags, translations}, `thumbnail` {scene, text (4 mots max), sub, shift, circle}, et `yt_chapter` sur les scènes qui ouvrent une partie. Un `chapter` compte aussi. YouTube exige au moins 3 chapitres d'au moins 10 s, le premier à 0:00.


## Animations sur vraie image (prioritaires)
- `annotate` : image, marks circle/box/arrow/measure/label{at,text}, question, heading, at — coordonnées MESURÉES sur l'image, jamais au jugé.
- `zoomto` (plonger vers une zone), `layers` (coupe translucide sur la photo), `beforeafter` (before, after, label_before/after).
- Infographies sur fond noir (scale, stat, versus, kinetic) : 3 maximum par vidéo.
- Ambiance sonore : `"ambience": {"kind": "ocean"}`.
