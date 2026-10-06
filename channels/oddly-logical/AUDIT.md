# Oddly Logical Science — Étape 1 : audit des images et stratégie

*Audit réalisé le 06/10/2026, avec des requêtes réelles sur les archives publiques (script `footage_audit.py`).*

## 1. Verdict : faisable, avec un très gros stock d'images pro

| Source (domaine public) | Accès automatique | Contenu |
|---|---|---|
| **NASA Image & Video Library** | ✅ API sans clé | Plus de 140 000 médias, dont des milliers de vidéos (ISS, lancements, planètes) |
| **NASA Scientific Visualization Studio (SVS)** | ✅ API sans clé | Visualisations 4K de niveau cinéma : Soleil, trous noirs, ouragans, océans |
| **ESA** | ✅ accessible | Spatial (licence à vérifier sujet par sujet) |
| **Wikimedia Commons** | ✅ API sans clé | Complément, attribution requise |
| **USGS, NOAA** (volcans, grands fonds) | ⚠️ sites qui bloquent les robots | À récupérer via Wikimedia ou à l'aide de liens fournis manuellement |
| **Pexels, Pixabay** | ⚠️ clé API gratuite requise | Plans de coupe nature et ciel en 4K |

## 2. Les 30 sujets testés

Les chiffres indiquent le nombre de vidéos NASA / visualisations SVS / images NASA disponibles pour chaque sujet.
- 🟢 : assez d'images pour une vidéo de 8 à 12 minutes.
- 🟡 : il faut compléter avec d'autres sources.
- 🔴 : à éviter pour l'instant.

| Sujet | Vidéos NASA | SVS | Images | Verdict |
|---|---|---|---|---|
| The Biggest Solar Flares Ever Recorded | 68 | 439 | 194 | 🟢 |
| Rain Falls on the Sun | 1 | 10 | 6 | 🟡 à intégrer dans une vidéo plus large sur le Soleil |
| What Happens Inside a Sunspot | 13 | — | 46 | 🟢 avec SVS |
| Why Auroras Glow Different Colors | 32 | 153 | 805 | 🟢 |
| Earth at Night From Space | 33 | — | 931 | 🟢 |
| Hurricanes Seen From Space | 56 | 665 | 1 054 | 🟢 |
| Lightning Seen From Space | 32 | 114 | 1 422 | 🟢 |
| Why Volcanoes Shoot Lava Fountains | 0 | 113 | 13 | 🟡 compléter via USGS et Wikimedia |
| Kilauea | 1 | — | 53 | 🟡 idem |
| Volcanoes on Io | 1 | 26 | 50 | 🟢 avec SVS |
| Jupiter's Great Red Spot Is Dying | 5 | 43 | 170 | 🟢 |
| Saturn's Rings Are Disappearing | 13 | — | 801 | 🟢 |
| The Moon Is Moving Away | 2 266 | 983 | 20 150 | 🟢 |
| Mars Dust Storms | 3 | 605 | 76 | 🟢 |
| What Perseverance Found on Mars | 124 | — | 1 282 | 🟢 |
| Pillars of Creation (James Webb) | 2 | 21 | 11 | 🟢 avec SVS |
| What a Black Hole Really Looks Like | 51 | 379 | 978 | 🟢 |
| Neutron Stars | 22 | 256 | 168 | 🟢 |
| When Galaxies Collide | 4 | 44 | 37 | 🟢 |
| Asteroids That Almost Hit Earth | 261 | — | 3 592 | 🟢 |
| How NASA Smashed an Asteroid (DART) | 28 | — | 121 | 🟢 |
| Comets | 52 | — | 1 049 | 🟢 |
| Rocket Launches Explained | 1 442 | — | 42 386 | 🟢 |
| Life on the ISS | 2 866 | — | 65 268 | 🟢 |
| Spacewalks: The Most Dangerous Job | 376 | — | 6 955 | 🟢 |
| Earth's Shrinking Glaciers | 39 | 265 | 367 | 🟢 |
| Wildfires Seen From Space | 5 | 93 | 149 | 🟢 |
| Strangest Creatures of the Deep Sea | 10 | — | 362 | 🟡 il faut les images NOAA |
| Hydrothermal Vents | 1 | 1 | 6 | 🔴 |
| Underwater Volcanoes | 1 | — | 6 | 🔴 |

**Bilan : 24 sujets 🟢, 4 🟡, 2 🔴.** Le spatial, le Soleil et la Terre vue de l'espace sont quasi inépuisables. Les grands fonds marins et les volcans terrestres demanderont une source en plus.

## 3. Viser des centaines de vidéos : 6 piliers × 50 sujets

| Pilier | Exemples | Stock d'images |
|---|---|---|
| ☀️ Le Soleil | éruptions, taches, vent solaire, fin du Soleil | Énorme (SDO, SVS) |
| 🌍 La Terre vue de l'espace | ouragans, éclairs, aurores, nuits, glaciers | Énorme |
| 🪐 Les planètes et lunes | Jupiter, Saturne, Mars, Io, Europe, Titan | Très grand |
| 🌌 L'univers extrême | trous noirs, étoiles à neutrons, collisions | Très grand (SVS) |
| 🚀 L'exploration | ISS, sorties dans l'espace, fusées, missions, accidents | Énorme |
| 🌋 La Terre extrême | volcans, séismes, grands fonds | Moyen, à compléter |

Avec environ 50 sujets par pilier, on atteint **300 vidéos** et plus. On peut aussi décliner un même sujet en plusieurs angles : « Top 10 », « What if… ? », « Explained in 10 minutes ».

## 4. Les règles pour être monétisable

1. **Durée de 8 à 12 minutes** pour les vidéos principales (heures de visionnage et pubs en cours de vidéo). Les Shorts sont découpés dans chaque vidéo pour attirer des abonnés.
2. **Un script original et exact** : c'est la vraie valeur ajoutée face à la règle sur le contenu « réutilisé » ou « produit en masse ». Les faits sont vérifiés et les sources citées en description.
3. **Une marque visuelle propre** : une intro de 3 secondes, des repères animés posés sur les images NASA et un étalonnage homogène.
4. **Une voix de qualité constante**, toujours la même, qui devient l'identité de la chaîne.
5. **Les crédits** en description (« Footage: NASA/GSFC/SDO… »). C'est obligatoire pour Wikimedia et conseillé pour la NASA.
6. **Une publication régulière** : 2 vidéos longues et 5 Shorts par semaine.

## 5. Économie de tokens

| Tâche | Qui | Coût en tokens |
|---|---|---|
| Moteur de montage (une seule fois) | Claude | Élevé, mais payé une seule fois |
| Script et liste de plans | Claude | Faible, environ 10 vidéos par session |
| Recherche et téléchargement des images, voix, montage, rendu | Le moteur, sur GitHub Actions | **0** |
| Publication | Toi, ou plus tard un envoi automatique sur YouTube | 0 |

## 6. Prochaine étape (étape 2)
Construire le moteur pro (Remotion + images NASA/SVS + voix + musique) et un **pilote de 8 à 10 minutes**.
Sujet proposé : **« The Sun Is Raining Fire »**, qui regroupe les éruptions, la pluie coronale et les taches solaires. Les images sont de niveau cinéma, et le sujet prolonge une vidéo déjà publiée sur ta chaîne.

À fournir de ton côté (facultatif) : une clé Pexels gratuite, et éventuellement plus tard une voix ElevenLabs.
