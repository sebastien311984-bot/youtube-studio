# Journal des retours (prioritaire sur le skill)
Chaque retour de l'utilisateur ou des stats YouTube devient une règle ici. Les plus récents d'abord.

- 2026-10-07 — PROCHAIN CHANTIER (intentions, pas des règles) : (1) SÉRIES cohérentes — « Survivre aux conditions extrêmes », « Comprendre les phénomènes de la Terre », « Les étrangetés de l'espace » ; chaque vidéo mène vers une autre de la même série (fin, écran de fin, fiche, playlist). (2) DÉBUT captivant : le phénomène dès la 1re seconde, une question précise, la réponse commence aussitôt, sans intro de chaîne. (3) PENSÉ TÉLÉPHONE : textes lisibles en petit, miniature simple à une seule idée forte, rien de coupé dans les Shorts (zones sûres). (4) Sujets vraiment accrocheurs et extraordinaires.

- 2026-10-07 — LEÇON N°1 : ne JAMAIS écrire de consignes trop strictes (quotas, chiffres, cases à cocher) : Claude devient robotique, ne réfléchit plus et accumule les erreurs. Les consignes donnent l'intention ; le jugement de réalisateur décide. But : des vidéos monétisables, sur des sujets passionnants et accrocheurs, qui attirent le plus de monde.

- 2026-10-07 — ✅ « inside_hurricane » VALIDÉE : « beaucoup mieux » — intro, final, titres, chapitres, plans d'ensemble, images réalistes et cohérentes, explications claires. LA FAÇON DE PROCÉDER À GARDER : vraies photos uniquement quand elles montrent littéralement la phrase ; schémas animés pour toutes les explications ; histoire serrée (~3-4 min) en chapitres ; ouverture et miniature sur l'image la plus forte ; moteur figé pendant la production ; aucune promesse non tenue ni fait inventé.

- 2026-10-07 — « space_no_suit » : promesse « reste jusqu'à la fin, un homme a survécu… » mal tenue (histoire au milieu, pas de vrai témoignage) = tromperie perçue. Ne jamais promettre ce que la vidéo ne livre pas exactement, au moment annoncé.

- 2026-10-07 — Encore un plan hors sujet (chambre de test NASA sur « vous ne gèleriez pas »). Racine : vouloir ~60 % de plans réels force des photos « d'ambiance ». Désormais : plan réel uniquement s'il montre littéralement la phrase, sinon infographie/schéma animé.

- 2026-10-07 — Sous-titres anglais INCRUSTÉS + sous-titres YouTube = superposition, et anglais sur la version doublée. Désormais pas d'incrustation (burn_captions=false par défaut) : on fournit le .srt, YouTube traduit. Piste audio FR : vérifier dans Studio > Langues qu'elle est bien publiée ; le spectateur la choisit via ⚙ > Piste audio.
- 2026-10-07 — outrun_tsunami refait SANS Pixabay : plans officiels/Commons/archives + motion design quand aucune vraie image n'existe ; voix off réécrite si l'image disponible raconte autre chose (ouverture : vague qui arrive, pas « bateaux sur la vase »). Vidéos Commons issues de particuliers/YouTubeurs (Sendai ambulances, Kita-Ibaraki) exclues. Nouveau : `"ambience": {"kind": "ocean"}` (houle + grondement du large sous la musique).

- 2026-10-07 — « Carrington n'est PAS une référence » : trop de consignes appliquées à la lettre = Claude ne réfléchit plus → régressions. Skill allégé : contrôle qualité par jugement (« est-ce que je cliquerais / est-ce juste ? »), règles = mémoire des erreurs, pas un script.

- 2026-10-07 — « space_no_suit » publiée telle quelle mais RÉGRESSIONS : (1) miniature nettement moins bonne que Carrington ; (2) aurore boréale au début (intro générique hors sujet) ; (3) quelques plans peu adaptés. À partir de maintenant : miniature regardée et comparée à celle de Carrington AVANT livraison (image choc du sujet, visage/objet net, 2-3 mots énormes) ; ouverture = image du SUJET, jamais un fond générique ; un plan « acceptable » ne suffit pas, il doit être juste.

- 2026-10-07 — Revue v3 outrun_tsunami : Pixabay renvoie souvent n'importe quoi (vaches pour « boats on mud », Mont-Saint-Michel pour « exposed seabed », famille qui court VERS la mer pour une évacuation, chaussures dessinées) + un carton-texte NASA et une image noire. Règle : tout plan Pixabay est suspect jusqu'à la revue `_review.jpg` ; en cas de doute on le supprime et on laisse les plans officiels/animations couvrir la scène. Moteur : un plan répété réutilise le même fichier ; Pixabay = requête complète seulement (plus de raccourcissement), vrais films seulement (video_type=film), au moins la moitié des mots de la requête dans les tags, sinon plan retiré ; `pixabay:id:<n>` pour figer un plan choisi à l'œil sur la planche du scout.
- [REMPLACÉ le 2026-10-08, voir plus bas] 2026-10-07 — PIXABAY INTERDIT par défaut (met le bazar : hors-sujet, métaphores). Images = sources officielles/archives uniquement (NASA, NOAA, USGS via Scout/Commons, CDC/NIH, DVIDS, Internet Archive). Choisir des sujets pour lesquels ces sources ont de VRAIES images, et alterner les thèmes à chaque vidéo.

- 2026-10-07 — SOUND DESIGN cinématique obligatoire : musique de fond adaptée au thème, petits sons pros (whoosh aux transitions, impacts sur les chiffres, riser + silence avant les révélations, ambiance du lieu). Il compense la voix de synthèse. Ne jamais régresser là-dessus.

- 2026-10-07 — Doublages : voix DYNAMIQUES, convaincantes, fun (garder l'auditeur). Moteur : voix natives/multilingues + tons dynamiques par scène (version fusionnée des deux discussions) ; traducteur : ton YouTubeur natif, phrases courtes. Images toujours cohérentes avec l'histoire ; zéro régression d'une vidéo à l'autre.

- 2026-10-07 — PLUSIEURS DISCUSSIONS EN PARALLÈLE : ne JAMAIS annuler un rendu GitHub Actions d'une autre branche que la sienne (outrun_tsunami annulé 2 fois par une autre discussion). Filtrer par `head_branch` avant tout cancel.

- 2026-10-07 — VOIX DOUBLÉES : doivent être dynamiques, convaincantes et fun pour retenir l'auditeur (style présentateur natif, phrases courtes, pas de calque de l'anglais) → règles dans oddly-translator.md. Moteur : tons par scène (`tone`) + voix réchauffée. Images : cohérence stricte avec l'histoire, zéro régression.

- 2026-10-07 — RECADRAGE de l'utilisateur : « pas professionnel, pas expert » : infos mal transmises entre discussions, images non accordées au texte, manque de vérification. Réponse : continuité via main (début/fin de chaque discussion), revue finale image/texte obligatoire (`_review.jpg`), jamais livrer sans avoir regardé, et dire honnêtement ce qui n'a pas été vérifié.

- 2026-10-07 — « space_no_suit » : casserole qui bout, fumée = images-métaphores jugées hors sujet. Règle : chaque plan montre CE QUE dit la voix (le vrai objet, le vrai lieu, la vraie personne) ; pas de métaphore visuelle générique. Si rien de réel n'existe → infographie/diagramme maison plutôt qu'un stock « illustratif ».
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

- 2026-10-06 — « Carrington Event » VALIDÉE, jugée « magnifique, excellente » : effets 3D NASA, narration, sons, chapitres, visuels variés de qualité, infographies dynamiques, titres, motion design. (Bonne vidéo, mais pas un modèle à copier.)
- 2026-10-06 — Failles corrigées dans le moteur : sous-titres qui mélangeaient deux phrases (coupure désormais aux pauses de la voix) ; Short de 7 s trop court (minimum 30 s imposé). Règle : chaque Short = un mini-récit complet de 30 à 58 s (accroche, révélation, chute), choisi sur un passage fort.

- 2026-10-06 — Objectif : 1 vidéo longue par jour (si le quota le permet). Une nouvelle conversation par vidéo pour économiser les tokens.
- 2026-10-06 — À FAIRE PLUS TARD : l'utilisateur a déjà un compte d'affiliation Amazon (liens à mettre dans les descriptions le moment venu). Mettre en place une veille des commentaires YouTube et des alertes (marques, sponsors, questions) pour ne rien laisser passer. En reparler vers 1 000 abonnés (sponsors, BrandConnect).

- 2026-10-06 — Leçons de la relecture de « carrington_event » : titre YouTube < 60 caractères ; Shorts ≤ 58 s (compter environ 2,6 mots/s plus les `min`) ; ne jamais poser un bandeau de date sur une image d'un autre événement ; fréquences d'événements rares = fourchettes publiées, pas d'affirmation ; accroche = question directe dans les 10 premières secondes.

- 2026-10-06 — Démo « It Rains on the Sun » v2 : l'intro cinématique, la musique, l'outro et les changements de format plaisent → à garder systématiquement.
- 2026-10-06 — Risque de monotonie : varier les formats d'une vidéo à l'autre (ne pas toujours schéma + chiffre). Utiliser le pack (scale, timeline, versus, quiz, kinetic, rank, photos).
- 2026-10-06 — Les vidéos de 1,5 à 3 min ne suffisent pas pour monétiser : viser 8 à 12 min.
- 2026-10-06 — L'utilisateur ne veut plus de ChatGPT ; tout se fait ici. Économiser le quota : déléguer l'écriture à l'agent oddly-scriptwriter (sonnet), relecture par oddly-factchecker, et rendu par GitHub Actions.

## Recherche d'images — règle permanente (2026-10-08)
- 2026-10-08 — PIXABAY RÉAUTORISÉ AVEC TRI VISUEL : Pixabay a beaucoup de bons clips (ouragans, etc.). Le problème venait du choix automatique du 1er résultat. Désormais : plusieurs requêtes par plan, 20-40 candidats, planche de vignettes, tri visuel (sujet exact, qualité, format 16:9 HD+, pas de métaphore), un clip différent par plan. Jamais de choix à l aveugle.
- 2026-10-08 — STYLE INFOGRAPHIE VALIDÉ (« exploitable ») : carte satellite étalonnée + zoom lent, points pulsants, lignes lumineuses, trajectoires en pointillés, objets animés, bulles de dialogue, nuages, grain, vignettage. Modèle : engine/templates/map_story.py. Adapter la technique à chaque sujet.
- AVANT d'écrire un script : fouiller TOUTES les sources de SOURCES.md (monde entier, pas seulement les USA) + Openverse/Europeana + vidéos YouTube sous licence Creative Commons (filtre « Creative Commons », vérifier que l'auteur est bien le filmeur original, sinon risque Content ID).
- Présenter une planche d'images au propriétaire ; si rien de spectaculaire et légal, changer de sujet AVANT de produire.
- Être proactif : chercher de nouvelles sources et les ajouter à SOURCES.md sans attendre qu'on le demande. Dire honnêtement et tôt ce qui est impossible.
