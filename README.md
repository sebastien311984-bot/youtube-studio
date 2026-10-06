# YouTube Studio

Production automatisée de vidéos YouTube (script → images libres → voix → montage cinématique → miniature, sous-titres, kit SEO, Shorts).

| Dossier | Contenu |
|---|---|
| `engine/` | Moteur de rendu (render.py, visuals.py, publish_kit.py, find_footage.py) |
| `channels/oddly-logical/` | Chaîne « Oddly Logical Science » : épisodes, retours, sujets, audit |
| `.claude/` | Skill de production et agents spécialisés |
| `.github/workflows/` | Rendu automatique des épisodes |

Récupérer une vidéo : onglet **Actions** → dernière exécution « Render videos » → **Artifacts** → `videos`.
