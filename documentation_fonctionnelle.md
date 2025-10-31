# Documentation fonctionnelle de l'application



## Présentation 
L'application présentée, a pour but de prédire le diagnostic de performances énergétiques (DPE) d'un logement, en renseignant quelques caractéristiques. Egalement, il permet de prédire la consommation d'énergie du logement. 
Pour ce faire, l'apprentissage automatique est utilisée. 

## Contenu de l'application

### 1. Contexte

La page contexte permet à l'utilisateur de comprendre la source des données utilisées (données provenant de l'Ademe), d'expliquer le DPE, et d'explorer les données qui seront utilisées. 
L'utilisateur peut explorer les données. Pour cela, il peut sélectionner le nombre de lignes de données qu'il souhaite visualiser. Il peut également faire des filtres sur la valeur d'une variable. 
Enfin, *un bouton de rafraîchissement des données* permet à l'utilisateur de mettre à jour les données. 

### 2. Statistiques & DPE

Cette page est composée de 3 sous-onglets: 
- Statistiques : Ce sous-onglet permet à l'utilisateur de visualiser les consommmations totale, chauffage et eau chaude/sanitaire, des données récupérées. Il peut également utiliser des filtres pour choisir d'afficher ces statistiques sur un code postal donné, un type de bâtiment, une période de construction, le type d'énérgie chauffage utilisé ou encore le type d'énergie eau chaude sanitaire utilisée ou encore, une fourchette de surface.

- Graphiques : Ce sous-onglet permet de visualiser différents types de graphiques choisis par l'utilisateur parmi histogramme, nuages de points, boxplot et diagramme circulaire.
L'utilisateur peut choisir d'y présenter des variables parmi celles disponibles dans le fichier des données (années de construction, type de bâtiments etc..)

- Cartographie : Ce sous-onglet permet de visualiser les différents logements issus des données sur une carte centrée sur Lyon. Y sont associés leur étiquette DPE (A,B,C,D,E,F,G), le type de bâtiment, la surface du logement, l'année de construction, la commune et enfin la consommation énergétique totale.
L'utilisateur peut choisir les étiquettes des DPE qu'il souhaite visualiser. 

### 3. Simulation 

*Cette page est composée de 2 sous-onglets:*

*- Etiquette DPE: Ce sous-onglet permet à l'utilisateur de prédire son étiquette DPE à l'aide de quelques paramètres qu'il renseigne en amont. Un modèle de classification est utilisé ici. 
Un bouton permettant de réentraîner le modèle est également disponible sur cette page.*

*- Consommation énergétique: Ce sous-onglet permet à l'utilsiateur de prédire sa consommation énergétique totale à l'aide d'un modèle de régression. 
Un bouton permettant de réentraîner le modèle est également disponible sur cette page.*


## Conclusion 

Cette application permet de visualiser les données de l'ADEME, en faire des graphiques, prédire étiquette DPE et consommation énergétique grâce à des modèles de classification et de régression. 
Les données peuvent être rafraîchies, et les modèles réentraîner afin d'intégrer au mieux aux données récentes. 
