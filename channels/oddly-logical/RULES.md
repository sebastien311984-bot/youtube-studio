# Oddly Logical Science — règles (refonte 12 oct. 2026)
Deux parties : des GARDE-FOUS courts (non négociables, vérifiés par les outils) et une MÉTHODE CRÉATIVE (on réfléchit, on ne coche pas des cases). Une nouvelle leçon remplace une ligne existante, jamais d'empilement.

## Objectif
1000 abonnés + 4000 h avant février 2027. Ce qui compte : rétention et envie de s'abonner. Mieux vaut une vidéo excellente que trois moyennes.

## A. Garde-fous (non négociables)
1. **Droits** : chaque image/son a une licence vérifiée (NASA/NOAA/USGS/ESA, Commons, archives, études CC BY, Pixabay en `pixabay:id:N` choisi à l'œil sur la planche). Crédits dans la description.
2. **Vérité** : factchecker sur chaque script ; fourchettes publiées ; le titre et la miniature tiennent leur promesse.
3. **Cohérence image ↔ voix** : chaque plan montre ce que dit SA phrase. Le moteur répartit le texte d'une scène à parts égales entre ses plans → 1 scène = 1 idée = 1 plan (plusieurs plans seulement s'ils montrent la même chose). Pas d'animal/décor « voisin » à la place du sujet. Aucun plan répété (photo ou vidéo). Pas de plan hors sujet « pour remplir » : si l'image manque, on raccourcit ou on anime.
4. **Monétisation** (contenu original, pas « images + voix ») : raisonnement et mise en scène à nous, séquences originales conçues pour le sujet, section « Sources », voix/musique/sons travaillés.
5. **Contrôle avant rendu** : check_episode → preflight (on REGARDE les planches) → oddly-viewer → un seul rendu → **contrôle final obligatoire** : oddly-viewer lit `<nom>_review.jpg` (image + phrase dite à chaque plan) et signale tout décalage ; on corrige et on re-rend AVANT de livrer.
6. **Jamais** de publication sans accord explicite de Sébastien (programmation via pack Chrome).

## Stratégie algorithme (YouTube = satisfaction à long terme, pas seulement temps passé)
Les signaux visés : CTR miniature/titre → rétention des 30 premières s → durée moyenne → satisfaction (likes, commentaires, pas de « Pas intéressé ») → session (le spectateur enchaîne une autre de nos vidéos) → retour sur la chaîne.
- **Fiche stratégie AVANT le script** (champ `strategy` du JSON, vérifié par check_episode) : `viewer` (qui clique et pourquoi), `hook` (la contradiction des 3 premières s), `promise` (ce que titre + miniature promettent), `payoff` (la réponse exacte donnée à la fin), `takeaway` (la phrase que le spectateur répétera à un ami).
- **Titre + miniature conçus d'abord**, 3 variantes chacun ; on garde le couple le plus fort et on vérifie que la 1re image de la vidéo le confirme (sinon abandon immédiat du spectateur).
- **Histoire qui progresse** : chaque scène répond à une question et en ouvre une nouvelle ; une relance marquée `reveal` ou `beat` au moins toutes les 40 s (contrôlé) ; procédé visuel jamais 3 fois de suite.
- **Fin qui récompense** : la dernière scène porte `payoff: true` et donne VRAIMENT la réponse promise (pas de teasing creux) ; puis renvoi vers une autre de nos vidéos (session).
- **3 mauvaises recettes interdites** : (1) titre/miniature qui promettent plus que la vidéo (clic trompé = signal négatif durable) ; (2) faire durer artificiellement (remplissage, répétitions, fausses relances « mais attendez… » sans contenu) ; (3) teasing permanent qui retarde la réponse jusqu'à frustrer.
- **Bilan après publication** (quand Sébastien partage les stats Studio) : CTR, % retenu à 30 s, courbe de rétention (où ça décroche), pour chaque vidéo une leçon qui remplace une ligne ici.

## B. Méthode créative (à repenser pour CHAQUE vidéo)
- **Partir des images, pas du texte** (leçon série corps, 12/10) : AVANT de proposer un sujet à Sébastien, lancer le scout et compter les vraies vidéos qui montrent exactement le sujet ; < 15 plans exacts → autre sujet. Ne jamais affirmer « on a les visuels » sans ce comptage. Une série = la 1re vidéo validée au contrôle final avant d'écrire les suivantes. Commits de travail en « [skip ci] » ; preflight regardé plan par plan (vidéos comprises) avant le rendu unique.
- **Ligne éditoriale (13/10, après la série corps jugée ennuyeuse)** : spectacle d'abord. Un sujet = un phénomène réel filmé qui fait « waouh » dès la 1re seconde (ralentis, labo, nature extrême, espace, crash, animaux hors norme). Test : « est-ce que je montrerais ce plan à un ami ? » sinon on coupe. Durée 2-4 min (jamais > 4 min sans matière exceptionnelle). Pas d'intro ni de final : on ouvre sur l'image choc, on finit sur la réponse + 10 s d'image pour l'écran de fin YouTube (S'abonner + vidéo suivante). Animations RARES (1-2) et uniquement au moment « mais comment c'est possible ? », jamais pour combler un manque d'images. Le savoir passe par une révélation par minute, pas par des explications longues.
- **Les 3 premières secondes** : la meilleure image + une contradiction qui crée une question. Pas de logo, pas de « bienvenue ».
- **Rythme** : une relance (révélation, chiffre, changement de point de vue) au moins toutes les 30 s ; plan nouveau toutes les 3-6 s.
- **Expliquer en montrant, avec des séquences créées pour CE sujet** : 3-5 séquences « signature » par vidéo, impossibles à trouver ailleurs (c'est ce qui rend la vidéo originale et monétisable). Outils : `globe` (Terre/planète photoréaliste texture NASA qui tourne, repères qui suivent), `manim` (animation sur mesure écrite en code : coupes, trajectoires, courbes, particules, échelles), vraie vidéo avec données (`hud`), annotations sur photo. Aucun outil n'est obligatoire ; éviter de répéter le même procédé d'une scène à l'autre. S'il manque un effet, on l'ajoute au moteur. Quand le code ne sait pas rendre quelque chose de réaliste (anatomie, vraie géographie, objet réel), on anime par-dessus une image libre vérifiée (voir SOURCES.md) plutôt que de dessiner un à-peu-près faux : l'exactitude prime.
- **Valeur ajoutée = comprendre, pas regarder** : chaque vidéo apporte au moins une chose qu'aucune image ne montre seule : un calcul refait à l'écran, une coupe/animation du mécanisme invisible (intérieur du corps, molécules, forces), une comparaison d'échelle parlante (« un camion-citerne par jour »), une expérience de pensée suivie pas à pas. Sujets ouverts à tout : corps humain, animaux, nature, technologie, histoire des sciences.
- **Appel à l'abonnement sans nom de chaîne** (le nom peut changer) : « Subscribe for the next one », jamais le nom de la chaîne dans la voix ni à l'image.
- **Fin** : la boucle ouverte se referme, une chute mémorable, puis renvoi vers la chaîne (sans annoncer un sujet précis).
- **Shorts** : chacun est un mini-récit autonome (`shorts[k].scenes`, 20-40 s, vraies images en mouvement) : accroche contradictoire → contexte en 1 phrase → révélation → « The full story is on the channel — subscribe for the next one. »
- **Titre** < 60 caractères, curiosité + mot-clé recherché ; **miniature** : une image nette et choc + 2-3 mots énormes.
- **Programmation** : mardi/vendredi 17 h (Paris), Shorts 1/jour ensuite, « vidéo associée » = la longue.
