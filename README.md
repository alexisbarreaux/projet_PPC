# projet_PPC

## Sujet

L’objectif du projet est d’implémenter un solveur générique de CSP où les contraintes sont binaires et les variables entières. Les domaines des variables seront finis. Il vous faudra modéliser un tel CSP, implémenter une ou plusieurs méthodes de consistance ainsi qu’un moteur de résolution. Vous testerez votre solveur sur de petits problèmes.

### 1 Travail minimal

#### 1.1 Modélisation
Tout d’abord, il faut écrire un modèle pour ce type de CSP. Nous vous rappelons qu’un problème est défini par un ensemble de variables, un domaine pour chaque variable et un ensemble de contraintes. Les contraintes sont binaires, elles sont donc définies par deux variables et un ensemble de tuples qui satisfont la contrainte. Un tuple est défini par deux valeurs ordonnées.