# YouTube Studio — production automatisée de vidéos YouTube

- Une chaîne = un dossier `channels/<chaîne>/` (episodes/, RULES.md, VIDEOS.md, TOPICS.md, PACKS.md).
- Moteur partagé dans `engine/` ; le rendu se fait **uniquement** via GitHub Actions (`.github/workflows/render-videos.yml`), déclenché par un push d'épisode JSON.
- Pour toute vidéo de la chaîne Oddly Logical Science : utiliser le skill **oddly-video** et les agents `oddly-scriptwriter` (écriture) et `oddly-factchecker` (relecture).
- Priorité absolue : économiser les tokens de l'utilisateur. Pas de rendu local complet ; déléguer l'écriture aux agents (modèle sonnet) ; réponses courtes en français.
- Toujours lire `channels/<chaîne>/RULES.md` avant de produire (règles consolidées). FEEDBACK.md = archive, ne pas lire.
- Toujours partir de `origin/main` et fusionner dans main en fin de conversation (sinon le travail est perdu pour les suivantes).
- Ne jamais publier sur YouTube sans accord explicite de l'utilisateur.
