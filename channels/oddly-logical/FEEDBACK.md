# Journal des retours (prioritaire sur le skill)
Chaque retour de l'utilisateur ou des stats YouTube devient une règle ici. Les plus récents d'abord.

- 2026-10-07 — Contrôle outrun_tsunami v1 : les animations NOAA/RIFT de Commons commencent par un carton-titre (nom d'un AUTRE événement, URL) → toujours `start` ≥ 14 s. Plans Pixabay hors sujet repérés (anémone, illustration, parasols sous « boats on mud ») → requêtes plus concrètes. Doublage hi/ar encore trop long (×1,3-1,4 sur ~12 scènes) → viser 30 % de syllabes en moins que l'anglais.

- 2026-10-07 — STOP ESPACE pour un moment (Soleil, Carrington, espace : trop). Prochaines vidéos : corps humain, Terre, catastrophes, animaux, histoire.

- 2026-10-07 — Doublage v1 (space_no_suit) : hindi et arabe plus longs (accélération jusqu'à ×1,4 sur 3-4 scènes) → demander au traducteur des phrases encore plus courtes pour hi et ar.

- 2026-10-07 — INTERNATIONAL : chaque vidéo sort avec des pistes audio doublées (es, pt, hi, fr, de, ar) via le champ `dub` ; l'utilisateur supprime les fichiers après publication, donc tout doit pouvoir se régénérer depuis le dépôt (épisode JSON + minutage). Carrington : doublage approximatif accepté.

- 2026-10-07 — Claude = chef de projet, réalisateur, monteur, étalonneur : il SURVEILLE TOUT lui-même. Pixabay = dernier recours (fonds verts, dessins animés, hors-sujet) ; priorité aux sources officielles (NASA SVS/images.nasa.gov, NOAA, USGS, ESA). Avant rendu : planche contact de toutes les photos/plans choisis ; après rendu : planche 1 image/4 s de la vidéo, regardée en entier avant de livrer.

- 2026-10-07 — AUTONOMIE : l'utilisateur ne valide pas chaque étape ; Claude décide en expert (sujet, format, style) et livre la vidéo finie. Durée libre selon le sujet : formats courts 4-6 min privilégiés pour lancer la chaîne (pas de longueur artificielle) ; 8 min+ seulement si le sujet le porte.

- 2026-10-07 — « deep_sea » ABANDONNÉE : le même rush tournait 3-4 fois à la suite (1 seul plan Pixabay de ~8 s pour une scène de 25 s → bouclé) ; sujet « méduses/abysses » jugé trop faible pour lancer la chaîne. Garde-fou moteur : une scène réelle est découpée automatiquement en plans de ~4,5 s tous différents. Règle d'écriture : TOUJOURS `shots` (1 plan par 4-5 s de voix), jamais un `clip` seul sur une scène longue. L'utilisateur regarde la vidéo avant publication : ne jamais annoncer « plans sans doublon » sans l'avoir vérifié.

- 2026-10-07 — IMAGES D'ACTUALITÉ : OK = agences fédérales US (NASA, NOAA, USGS, NSF, JPL : domaine public, pas de logo ni d'aval implicite) ; ESA (CC BY-SA 3.0 IGO) et ESO (CC BY 4.0) avec crédit ; Webb/Hubble (NASA, ESA, CSA, STScI) avec crédit. INTERDIT = images de médias (AFP, Reuters, AP, Getty, CNN…), vidéos d'autres YouTubeurs, vidéos de réseaux sociaux sans licence. Captures d'écran d'un article ou d'un communiqué : seulement brèves, commentées, jamais le cœur de la vidéo (risque « contenu réutilisé » qui bloque la monétisation).

- 2026-10-07 — STRATÉGIE « croissance » (validée) : (1) Shorts d'abord : 2-3 Shorts/jour (tirés des longues ou dédiés) pour attirer les abonnés ; (2) angle « TOI » : titres What Happens to Your Body / Could You Survive / What If You… plutôt que sujets documentaires (« les méduses » n'attire pas) ; (3) actualité : quand un événement scientifique fort tombe (astéroïde, éruption, aurore, découverte JWST/NASA), vidéo + Shorts en moins de 48 h avec les images officielles du communiqué ; (4) version FR (piste audio ou 2e chaîne) dans un mois si les chiffres suivent. Mesure : CTR > 4 %, rétention 30 s > 60 % ; bilan après ~20 vidéos.

- 2026-10-07 — « deep_sea » : mêmes plans répétés 3-4 fois (requêtes Pixabay proches → même 1er résultat). Corrigé : le moteur n'utilise jamais deux fois la même vidéo Pixabay. Règle : requêtes Pixabay toutes différentes et variées (animal, lumière, plongée, sous-marin, plancton…).

- 2026-10-06 — Short : impossible de lier la vidéo longue tant qu'elle n'est pas en ligne → publier la longue d'abord, puis le Short avec « Vidéo associée ».

- 2026-10-06 — Le style NE doit PAS être toujours pareil : palette, rythme, musique, polices de titres et transitions adaptés au sujet (abysses = bleu nuit/cyan bioluminescent, lent et oppressant ; volcan = orange/rouge, nerveux ; espace = violet/or, majestueux).

- 2026-10-06 — Carrington « parfaite, bluffante » : images, titres (apparition, police, couleurs accordées à l'image = TOP), motion design → systématique. À renforcer : (1) 5 premières secondes percutantes = image la plus forte + question choc AVANT l'intro logo (cold open) ; (2) référencement Google (moments clés) : chapitres = questions/mots-clés recherchés (« How deep do anglerfish live? »), 6 à 8 chapitres, chaque chapitre ouvert par une phrase-réponse claire, description = résumé de 2-3 phrases + mini-FAQ, sous-titres SRT envoyés.

- 2026-10-06 — VARIER LES THÈMES : pas deux vidéos de suite sur le même thème (trop de Soleil). Alterner Terre / animaux / océans / espace ; NASA plus tard.
- 2026-10-06 — Pixabay n'a pas les espèces rares (anglerfish, viperfish, giant squid : 0 résultat) → requêtes génériques ; le moteur raccourcit désormais la requête automatiquement.
- 2026-10-06 — Pixabay opérationnel (testé) : utiliser `"clip": "pixabay:..."` pour la nature, les océans et les animaux. Pexels indisponible (clés suspendues). Secours : NOAA, USGS, US Fish & Wildlife, Wikimedia Commons.

- 2026-10-06 — « Carrington Event » VALIDÉE, jugée « magnifique, excellente » : effets 3D NASA, narration, sons, chapitres, visuels variés de qualité, infographies dynamiques, titres, motion design. C'est LA référence : garder ce niveau et cette recette.
- 2026-10-06 — Failles corrigées dans le moteur : sous-titres qui mélangeaient deux phrases (coupure désormais aux pauses de la voix) ; Short de 7 s trop court (minimum 30 s imposé). Règle : chaque Short = un mini-récit complet de 30 à 58 s (accroche, révélation, chute), choisi sur un passage fort.

- 2026-10-06 — Objectif : 1 vidéo longue par jour (si le quota le permet). Une nouvelle conversation par vidéo pour économiser les tokens.
- 2026-10-06 — À FAIRE PLUS TARD : l'utilisateur a déjà un compte d'affiliation Amazon (liens à mettre dans les descriptions le moment venu). Mettre en place une veille des commentaires YouTube et des alertes (marques, sponsors, questions) pour ne rien laisser passer. En reparler vers 1 000 abonnés (sponsors, BrandConnect).

- 2026-10-06 — Leçons de la relecture de « carrington_event » : titre YouTube < 60 caractères ; Shorts ≤ 58 s (compter environ 2,6 mots/s plus les `min`) ; ne jamais poser un bandeau de date sur une image d'un autre événement ; fréquences d'événements rares = fourchettes publiées, pas d'affirmation ; accroche = question directe dans les 10 premières secondes.

- 2026-10-06 — Démo « It Rains on the Sun » v2 : l'intro cinématique, la musique, l'outro et les changements de format plaisent → à garder systématiquement.
- 2026-10-06 — Risque de monotonie : varier les formats d'une vidéo à l'autre (ne pas toujours schéma + chiffre). Utiliser le pack (scale, timeline, versus, quiz, kinetic, rank, photos).
- 2026-10-06 — Les vidéos de 1,5 à 3 min ne suffisent pas pour monétiser : viser 8 à 12 min.
- 2026-10-06 — L'utilisateur ne veut plus de ChatGPT ; tout se fait ici. Économiser le quota : déléguer l'écriture à l'agent oddly-scriptwriter (sonnet), relecture par oddly-factchecker, et rendu par GitHub Actions.
