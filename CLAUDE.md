# YouTube Studio — production automatisée de vidéos YouTube

- Une chaîne = un dossier `channels/<chaîne>/` (episodes/, FEEDBACK.md, TOPICS.md, AUDIT.md).
- Moteur partagé dans `engine/` ; le rendu se fait **uniquement** via GitHub Actions (`.github/workflows/render-videos.yml`), déclenché par un push d'épisode JSON.
- Pour toute vidéo de la chaîne Oddly Logical Science : utiliser le skill **oddly-video** et les agents `oddly-scriptwriter` (écriture) et `oddly-factchecker` (relecture).
- Priorité absolue : économiser les tokens de l'utilisateur. Pas de rendu local complet ; déléguer l'écriture aux agents (modèle sonnet) ; réponses courtes en français.
- Toujours lire `channels/<chaîne>/FEEDBACK.md` avant de produire : ce sont les retours de l'utilisateur, prioritaires sur tout le reste.
- Ne jamais publier sur YouTube sans accord explicite de l'utilisateur.
