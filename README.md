# Analyse de Performance - Vélo Stationnaire 🚴

Analyse exploratoire de mes données personnelles d'entraînement en vélo stationnaire,
comparant les séances effectuées au **gym** 🏋️ et à la **maison**🏡

## Description du projet 📝

Ce projet analyse l'évolution de ma performance en vélo stationnaire sur plusieurs mois. 
Étant une personne qui adore faire du vélo stationnaire, j'ai décidé de mieux comprendre ma progression en exploitant les données de mes séances.

Le projet inclut le nettoyage des données, le calcul de statistiques descriptives et la génération automatique de graphiques. 

**Les analyses et les graphiques se mettent à jour automatiquement dès que j'ajoute de nouvelles données à mon fichier Excel qui est stocké dans mon Cloud.** 

## Structure du projet 📁
```
Performance_Velo_Stationnaire/
|__ README.md                       #Documentation principale
|__ Data Vélo.xlsx                  #Données brutes des séances
|__ data_velo.py                    #Script de l'analyse
|__ requirement.txt                 #Dépendances Python (pip install -r requirements.txt)
|__ .gitignore                      #Ignorer fichier inutiles lors du dépot
|__ graphs/                         #Graphique générés automatiquement
|   |__ Distance_parcouru_par_seance.png
|   |__ Gym_VS_Maison.png
|   |__ Distance_par_mois.png
|   |__ Nombre_de_seance_par_mois.png
|   |__ Distance_VS_Duree.png
|__ output/                            #Fichier de sortie générés
    |__ rapport_analyse.txt

```
## Données 📊

Les données ont été collectées manuellement après chaque séance d'entraînement et contiennent les variables suivantes : 

| Variable   | Description          |
|------------|----------------------|
|Date        | Date de la séance    |
|Emplacement | Lieu de la séance (Gym ou maison)|
|Temps       | Durée de la séance (HH:MM:SS) |
|Distance (KM)| Distance parcourue en kilomètres |

### Variables calculées par le script :

+ Temps en minutes - Conservision de la durée en minutes décimales
+ KM/H - Vitesse moyenne calculée
+ Mois - Mois de la séance pour les agrégations 

## Fonctionnement du script ⚙️

Le script data_velo.py effectue les étapes suivantes : 

1. Chargement et nettoyage des données : Lecture du fichier Excel, standardisation des valeurs, conversions des types 🧹

2. Calcul des métriques : Vitesse moyenne (KM/H), durée en minutes 🧮

3. Statistiques descriptives :  Résumé par emplacement (distance, vitesse durée)📈

4. Génération de 5 graphiques : Sauvegardés automatiquement dans le dossier graphs/ 📉

## Visualisation des graphiques  📊

|Graphiques      | Description           |
|---------------|-----------------------|
|Distance par séance| Évolution de la distance dans le temps avec tendance globale|
|Gym VS Maison  |Boxplots comparant la distance et la vitesse selon l'emplacement |
|Distance par mois |Barres empilées de la distance mensuelle |
|Séance par mois| Nombre de séances par mois selon l'emplacement|
|Distance VS Durée| Nuage de points comparant la distance VS la durée avec une droite de tendance|

## Technologies utilisées 🐍

* Python 3 
* ```pandas ```- Manipulation et nettoyage des données 
* ```matplotlib```- Visualisations 
* ```numpy ```- Calculs statistiques
* ```pathlib```- Gestion des chemins de fichiers 

## Utiliser ce projet 💻

1. Cloner le dépôt : 

```bash 
git clone git@github.com:alepine9596/Performance_Velo_Stationnaire.git
```

2. Installer les dépendances :
```bash
pip install -r requirement.txt
````

3. Mettre le chemin du fichier Excel dans data_velo.py 
```bash 
EXCEL_FILE : "Data Vélo.xlsx" 
````

4. Lancer le script : 
```bash 
python data_velo.py
```

Les graphiques seront générés dans le dossier `graph/` et le rapport de performance des statistiques en format txt sera généré dans le dossier `output/`

## Principaux résultats de l'analyse 🧐

* La distance parcourue par séance montre une tendance de progression au fil des séances

* Les séances à la maison ont tendance à être plus longues et la distance parcourue est plus grande

* La corrélation positive entre la durée et la distance confirme une amélioration de la performance 

_Projet réalisé dans le cadre du développement de mon portfolio_ 

Alexandra Lépine 




