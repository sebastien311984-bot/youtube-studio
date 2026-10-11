# Règles de la chaîne — version consolidée (11 oct. 2026)
Seul fichier de règles à lire. Remplace FEEDBACK.md (archivé). Une nouvelle leçon = 1 ligne ici, en remplaçant la règle qu'elle contredit (jamais d'empilement).

## Objectif
1000 abonnés + 4000 h. 2-3 vidéos longues/semaine (6-10 min) + 3 Shorts chacune. Qualité > quantité (politique YouTube « contenu produit en masse »).

## Exigences permanentes du propriétaire (ne jamais lui faire répéter)
- Niveau pro, cinématographique, irréprochable. Sinon on ne livre pas.
- Règles YouTube strictes : contenu original et transformateur (pas « produit en masse » ni réutilisé), droits vérifiés sur chaque image et son, aucun clickbait mensonger (la vidéo tient la promesse du titre et de la miniature).
- Sujets à fort potentiel (viser des millions de vues) : peur, survie, mystère, record, « impossible mais vrai », avec un mot-clé que les gens recherchent vraiment. Vérifier la demande (recherche YouTube, tendances) avant de choisir.
- Faire s'abonner : promesse de chaîne dite tôt (« every week, the strangest true science »), appel à l'abonnement placé juste après un moment fort (jamais au début), séries/playlists, fin qui renvoie vers une autre vidéo de la chaîne (sans annoncer un sujet précis à venir).

## Sujet
- Angle TOI (« Could You Survive… », « What Happens to Your Body… ») ou mystère/histoire vraie (Flight 19 : 90,7 % de rétention).
- Rotation des thèmes, jamais 2 fois de suite le même. Vérifier VIDEOS.md (déjà faits).
- Pas de vraies images spectaculaires et légales → changer de sujet AVANT d'écrire.

## Images
- Une image montre LITTÉRALEMENT la phrase, sinon animation. Jamais de photo « d'ambiance ».
- Sources : NASA, NOAA, USGS, ESA/ESO (CC BY), Commons, archives (SOURCES.md). Pixabay seulement en `pixabay:id:<n>` choisi sur la planche scout ; `pixabay:requête` interdit.
- Aucun plan répété, ≤ 6 s par photo, pas de vidéos de particuliers (risque Content ID).
- Animer de préférence SUR la vraie image (annotate, zoomto, layers, beforeafter) ; fond noir 3 max.

## Montage
- Seconde 0 = le phénomène + question choc. Pas de carton logo au début ; boucle ouverte résolue à la fin.
- Changement visuel/son toutes les 4-6 s ; chapitres ; sound design cinématique (whoosh, impacts, riser + silence avant révélation).
- Ne jamais promettre ce que la vidéo ne livre pas. Faits prudents (fourchettes publiées).
- Fin : ne jamais annoncer un sujet précis pour la suivante.
- Pas de sous-titres incrustés : .srt fourni.

## Shorts
- Frame 0 : image en mouvement + texte contradictoire (« This should kill you. It doesn't. »), aucun logo.
- 20-58 s, mini-récit complet, plan qui change toutes les 1,5-3 s, fin qui boucle sur le début.
- Publiés APRÈS la longue, 1/jour, « Vidéo associée » = la longue.

## YouTube
- Titre < 60 caractères (mot-clé + curiosité). Miniature : 1 image choc du sujet + 2-3 mots énormes.
- Programmée mardi ou vendredi 17h (Paris), jamais Public direct.
- 2026-10-11 : AUCUN plan répété, ni photo ni vidéo (max 1 utilisation, vérifié par check_episode) ; le moteur allonge les plans au lieu de les répéter. Prévoir assez de visuels uniques dès le repérage (≈ 1 plan / 4 s).
- 2026-10-11 : CONTRÔLE « SPECTATEUR » avant livraison : regarder la vidéo comme un abonné potentiel (30 premières s, chaque début de chapitre, la fin). Question à chaque moment : « est-ce que je dis waouh / est-ce que je reste ? ». Sinon corriger. Le hook montre l'image la plus forte de la vidéo, pas une image d'ambiance.
- 2026-10-11 : PIPELINE QUALITÉ (obligatoire) : scout → liste blanche → scriptwriter → factchecker → check_episode (bloque : plan répété, écran infographique > 12 s, accroche non réelle, Short sur infographie) → preflight → agent **oddly-viewer** (spectateur exigeant, corrige avant rendu) → UN rendu → contrôle final. Pour l'espace : chercher aussi les animations 4K NASA SVS (engine/find_footage.py) pour avoir de la vraie vidéo, pas que des photos.
