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

## Sources internationales (2026-10-08) — vérifier la licence de CHAQUE fichier
| Zone | Source | Contenu | Licence / crédit |
|---|---|---|---|
| Méta-recherche | Openverse (openverse.org), Flickr Commons, Europeana (filtre « réutilisable ») | moteur sur des centaines de musées/archives du monde | CC0 / CC BY selon fichier |
| YouTube | Vidéos sous licence Creative Commons (CC BY) | CC BY : créditer ; vérifier que la chaîne est l auteur original |
| Europe – espace/Terre | ESA, Copernicus Sentinel, EUMETSAT, ESO, NOIRLab, ALMA | satellites, tempêtes vues d'en haut, incendies, télescopes | CC BY / CC BY-SA IGO ; « contains modified Copernicus Sentinel data » |
| Europe – science | CERN (CDS videos) | accélérateurs, physique | CC BY 4.0 |
| Europe – archives | Open Images (Beeld en Geluid, NL), Bundesarchiv & Deutsche Fotothek (via Commons), Nationaal Archief, Finna (FI), Riksarkivet/K-samsök (SE) | films d'actualités anciens, histoire, catastrophes historiques | CC BY-SA / CC0 selon fichier |
| Europe – musées | Rijksmuseum, Paris Musées, SMK (DK), Wellcome Collection | art, médecine ancienne, objets | CC0 / CC BY |
| Japon / Asie | Himawari (JMA, imagerie satellite), JAXA Digital Archives, ISRO | typhons vus de l'espace, fusées japonaises/indiennes | crédit obligatoire, usage commercial à vérifier fiche par fiche |
| Océanie | CSIRO ScienceImage, Australian Antarctic Division, Te Papa (NZ), DigitalNZ | faune australienne, Antarctique, volcans NZ | CC BY |
| Canada | Agence spatiale canadienne, Ressources naturelles Canada | espace, Arctique, géologie | Licence du gouvernement ouvert – Canada (crédit) |
| Nature (monde) | iNaturalist, Biodiversity Heritage Library | animaux rares, planches naturalistes | CC BY / domaine public |
| Stock vidéo cinéma | Pexels (site), Mixkit, Coverr, Videvo, Dareful (4K), Vecteezy/Videezy (crédit), Pond5 « Public Domain » | plans génériques de qualité | libres ; vérifier chaque plan, tri visuel sévère |

## Sources monde « 100 % légal monétisable » (ajout 12/10/2026) — toujours vérifier la licence de CHAQUE fichier
Règle : uniquement domaine public, CC0, CC BY, CC BY-SA, licence gouvernementale ouverte autorisant l'usage commercial. Exclure « non commercial » (NC) et « ND ». Créditer dans la description.

### Europe
- ESA (esa.int multimedia) : beaucoup d'images/vidéos en CC BY-SA 3.0 IGO — vérifier la mention par fichier.
- ESO (eso.org) : CC BY 4.0 (astronomie, télescopes, animations).
- Copernicus / Sentinel (UE) : images satellites libres avec attribution « contains modified Copernicus Sentinel data » ; Copernicus EMS : cartes de catastrophes (inondations, incendies, séismes).
- Royaume-Uni : contenus sous Open Government Licence v3 (usage commercial autorisé) — ex. Met Office, British Geological Survey (vérifier par ressource).
- Europeana : filtrer « réutilisation libre » (CC0, CC BY, domaine public) — archives historiques européennes.
- Parlement / Commission européenne (services audiovisuels) : réutilisation avec mention de la source — vérifier les conditions par clip.
- Wikimedia Commons : mondial, filtrer les licences ci-dessus.

### Asie-Pacifique
- Japon : contenus du gouvernement sous « Public Data License / Government Standard Terms of Use » (compatibles CC BY 4.0) — ex. Agence météorologique japonaise (satellite Himawari), à vérifier par ressource. JAXA : usage commercial soumis à autorisation → exclu.
- Corée du Sud : KOGL Type 1 uniquement (commercial autorisé).
- Australie : Geoscience Australia et nombreux sites gouvernementaux en CC BY 4.0 (Bureau of Meteorology : conditions restrictives → exclu).
- Nouvelle-Zélande : GNS Science, GeoNet (volcans, séismes) en CC BY 4.0.

### Amériques
- Agences fédérales américaines (domaine public) : NASA, NOAA, USGS, FEMA, US Coast Guard, DVIDS (armée / Garde nationale : sauvetages, ouragans, incendies).
- Canada : Licence du gouvernement ouvert – Canada (commercial autorisé).

### Vidéos d'actualité amateur
- YouTube, filtre « Creative Commons » (CC BY) : chasseurs d'orages, témoins. Créditer la chaîne d'origine.
- Banques sous licence payante (Newsflare, Storyful, ViralHog) : seulement pour une vidéo phare, licence achetée.

### Interdit
- Images de chaînes TV / agences (AFP, Reuters, AP) sans licence, même courtes, retournées ou recadrées. Jamais de contournement de Content ID.

### Corps humain, médecine, animaux, nature (ajout 12/10)
- Openverse (`openverse:` dans le scout) : moteur unique sur ~800 M d'images à licence commerciale (Flickr CC, Smithsonian Open Access CC0, Wellcome Collection CC BY, musées, Commons…).
- iNaturalist (`inat:` dans le scout) : photos d'animaux et plantes identifiés, filtrées CC BY / CC0.
- Servier Medical Art (smart.servier.com) : illustrations médicales/anatomie CC BY 4.0.
- NIH (images.nih.gov, NIAID Flickr CC BY), CDC Public Health Image Library (domaine public sauf mention) : microscopie, virus, cellules.
- Wellcome Collection : CC BY (histoire de la médecine, anatomie).
- Smithsonian Open Access : CC0 (animaux, fossiles, objets).
- US Fish & Wildlife Service, NOAA Fisheries, National Park Service : domaine public (faune).
- Revues en accès libre (PLOS, eLife, Scientific Reports, Nature Communications) : figures et vidéos supplémentaires en CC BY — vraies expériences de labo, ralentis, microscopie.
