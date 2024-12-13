
# FR-movie-embed-link-scrapper-FR

## Description

FR-movie-embed-link-scrapper-FR est un projet Python conçu pour extraire des informations sur les films depuis un site de streaming. Les données récupérées incluent :
- **Le titre du film**
- **Le lien Embed**
- **Le lien de l'affiche du film**

Ces informations sont enregistrées dans un fichier texte au format suivant :
```
titre du film ----- lien du film ----- lien de l'affiche du film
```

Ce projet a été développé par **Pecorio**, un jeune passionné de 16 ans, pour se propulser dans le monde du travail en mettant en avant ses compétences en développement. Ce projet n'est actuellement **pas open source**, mais pourrait le devenir dans le futur.

---

## Fonctionnalités
- Interface graphique conviviale et moderne utilisant `tkinter` avec des effets "néon".
- Scraping des films à partir de pages web avec Selenium.
- Enregistrement des informations extraites dans des fichiers locaux.
- Reprise automatique de la progression en cas d'interruption.
- Barre de progression pour suivre l'avancement.

---

## Prérequis

1. **Python 3.7+**
2. **Modules Python** :
   - `tkinter`
   - `selenium`
   - `json`
3. **Edge WebDriver** : Téléchargez-le et spécifiez le chemin dans le script.
   - Exemple : `C:\Users\pecor\Downloads\edgedriver_win64\msedgedriver.exe`
4. **Site cible** : [https://www.cpasmieux.is/filmstreaming/](https://www.cpasmieux.is/filmstreaming/)

---

## Installation

1. Clonez ce dépôt :
   ```bash
   git clone https://github.com/clement91380/FR-movie-embed-link-scrapper-FR.git
   cd FR-movie-embed-link-scrapper
   ```
2. Installez les dépendances requises :
   ```bash
   pip install selenium
   ```
3. Configurez le chemin du Edge WebDriver dans le script Python.

---

## Utilisation

1. Exécutez le script Python :
   ```bash
   python scraper.py
   ```
2. Dans l'interface graphique :
   - Cliquez sur **"Démarrer le Scraping"** pour lancer l'extraction des informations des films.
   - Suivez l'avancement grâce à la barre de progression et les compteurs.
   - Les résultats seront enregistrés dans `film-results.txt`.

---

## Objectif

Ce projet a pour but de m'aider à améliorer mes compétences et à me faire remarquer dans le monde du développement. j'illustre une combinaison de compétences techniques en Python, interface utilisateur, et scraping web.

---

## Auteur
- **Pecorio** (pseudonyme)
- Site personnel : [Stream-2-Free](https://stream-2-free.fr.to/)
- Soutenez mon travail : [Don PayPal](https://www.paypal.com/donate?token=cygSGzbiaQetvJ3yHo09DnLRYEqWrEM39ar4elBwCh23PHVyTbCMbHMrIkgVxhXA0CeM2g_cFCzyHyIg)

---

## Notes importantes
1. Le scraping de sites web peut être soumis à des restrictions légales. Assurez-vous de respecter les **Conditions d'utilisation** du site cible.
2. Ce projet est actuellement **privé**, mais pourrait devenir open source selon son évolution.

---

## Améliorations futures
- Ajout d'un mode "head-less" pour le scraping sans fenêtre graphique.
- Export des résultats au format JSON ou CSV.
- Optimisation des performances du scraping.

---

Merci de votre intérêt pour FR-movie-embed-link-scrapper-FR ! 🎬

