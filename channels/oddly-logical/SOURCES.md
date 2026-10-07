# Sources d'images — où trouver du spectaculaire légal
Règle : jamais d'images de chaînes YouTube, BBC, National Geographic, Discovery, etc. Créditer en description quand c'est demandé.

| Source | Contenu | Accès par le moteur | Licence / crédit |
|---|---|---|---|
| **NASA SVS** (svs.gsfc.nasa.gov) | Visualisations 4K : Soleil, trous noirs, Terre, planètes | `find_footage.py "requête"` → URL MP4 | Domaine public. Crédit : « NASA's Scientific Visualization Studio » |
| **NASA Image & Video Library** (images.nasa.gov) | ISS, lancements, astronautes, missions | API publique sans clé | Domaine public. Crédit « NASA » |
| **Pixabay** | Nature, animaux, océans, météo, villes, en 4K | `"clip": "pixabay:requête"` (résolu au rendu, secret GitHub) | Libre, crédit facultatif |
| **Wikimedia Commons** | Animaux, phénomènes, archives historiques, éruptions, NOAA/USGS miroités | `find_footage.py --commons "requête"` → URL | CC BY / CC BY-SA / domaine public. **Crédit obligatoire** (auteur + licence) dans la description |
| **NOAA Ocean Exploration** (oceanexplorer.noaa.gov) | Grands fonds, créatures abyssales, volcans sous-marins | Site anti-robots : passer par Wikimedia (beaucoup y sont copiés) ou des liens fournis | Domaine public. Crédit « NOAA Ocean Exploration » |
| **USGS** (usgs.gov) | Volcans (Kilauea), séismes, geysers | Idem (anti-robots) → Wikimedia ou liens fournis | Domaine public. Crédit « USGS » |
| **US Fish & Wildlife / NPS** (parcs nationaux) | Faune nord-américaine, Yellowstone, paysages | Wikimedia (catégories « USFWS », « NPS ») | Domaine public |
| **ESA** (esa.int/ESA_Multimedia) | Spatial européen, comètes, Mars Express | Liens directs | Souvent CC BY-SA 3.0 IGO. Crédit « ESA » |
| **ESO** (eso.org) | Télescopes au Chili, nébuleuses, vues d'artiste | Liens directs | CC BY 4.0. Crédit « ESO » |
| **Coverr / Mixkit** | Plans de coupe génériques (ciel, ville, nature) | Téléchargement manuel uniquement (pas d'API) | Libre |
| **Pexels** | (création de clés API suspendue en 2026) | — | — |

Astuce rétention : alterner une source « réelle » (NASA, NOAA, Pixabay) et une animation maison toutes les 5 à 10 s. Une image rare (grands fonds, archives) en accroche augmente le taux de clics.

## Sources élargies (2026-10-07) — toutes légales et gratuites
| Source | Contenu | Licence / crédit |
|---|---|---|
| DVIDS (dvidshub.net) | armée US : avions, navires, explosions, sauvetages, catastrophes | domaine public (vérifier la mention « public release ») ; pas d'aval implicite |
| CDC PHIL (phil.cdc.gov), NIH / NIAID (flickr NIAID) | microscopie, virus, bactéries, corps humain | domaine public pour la plupart (lire chaque fiche) ; NIAID en CC BY : créditer |
| Internet Archive — Prelinger, films gouvernementaux | films anciens, histoire, essais, accidents | domaine public (vérifier chaque film) |
| Smithsonian Open Access | animaux, fossiles, objets, histoire | CC0 |
| NOAA Ocean Exploration, NPS (parcs US), US Fish & Wildlife, USDA | océans profonds, volcans, faune, nature | domaine public |
| ESA, ESO, Hubble/Webb, EUMETSAT | espace, météo | CC BY / CC BY-SA : créditer |
| Wikimedia Commons | tout | licence par fichier : créditer l'auteur |
| Mixkit, Coverr, Videvo (licence gratuite), Pixabay | stock générique | libres ; tri visuel sévère obligatoire |
| Images IA (générées par nous) | ce qui est infilmable | légal ; cocher « contenu synthétique » si réaliste |
INTERDIT : images de médias (TV, agences AFP/Reuters/AP/Getty, journaux), vidéos YouTube/TikTok/Instagram d'autrui, films et séries. Content ID les détecte : blocage, démonétisation, avertissements.
