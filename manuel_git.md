
# Manuel d'utilisation de Git et GitHub
```markdown
## 1. Git et Github, c'est quoi?

**Git** est un système de contrôle de version qui permet de suivre les modifications apportées à votre code, de collaborer avec d'autres développeurs et de gérer différentes versions d'un projet.  
**GitHub** est une plateforme en ligne qui héberge les dépôts Git et facilite la collaboration entre développeurs.

Avec GitHub, on peut :
- Travailler en équipe sur le même projet.
- Visualiser l’historique des modifications.
- Gérer les contributions via des branches et des pull requests.

Etape 1 : Vérifier si on possède déjà git
  -> Recherchez Git Bash et Git CMD avec la barre de rechercher du pc
Si ces deux applications sont bien présentes, on peut directement passer au travail collaboratif avec git (3) , sinon il faut passer par la configuration initiale (2)

## 2. Configuration initiale (Si on ne possède pas git)

### 2.1 Installation de Git
 
1. Rendez-vous sur https://git-scm.com.
2. Cliquez sur Download 
3. Une fois le téléchargement fini, on passe les différentes étapes de l'installation classique.


### 2.2 Prérequis pour collaborer sur un projet avec git 
1. Si quelqu'un ne l'a pas déjà fait, il faut déposer le projet dans un espace appelé repository.
          -> Un repository ou dépôt est un dépôt distant, c’est-à-dire qu’il est hébergé sur internet.
2. Il faut posséder un compte github ou alors en créer un sur https://github.com/ 
3. Le repository doit être public pour pouvoir y accéder (c'est le créateur du repository qui peut le définir comme public)
4. Le propriétaire du repository (celui qui l’a créé) le partage aux collaborateurs


### 2.3 Accéder au repository
Une fois que tous les prérequis sont prêts, les collaborateurs doivent copier le répertoire distant sur leur ordinateur (en local).
Pour cela :
1. Il faut d'abord lancer Git Bash, Git Bash permet d'écrire des commandes afin de recevoir, envoyer ou ajouter de nouveaux fichiers au répertoire
2. Pour récupérer le rpéertoire sur l'ordinateur, il faut executer la commande suivante dans l'invite de commande (gitbash) :
  - git clone https://github.com/YassineCHN/SISE_Enedis.git
  - Appuyer sur Entrée
**Explication** :
   - `git clone` : copie le repository distant sur votre machine locale.
   - `origin` : nom par défaut donné au repository distant.
Pour accédez au répertoire cloné :
   - cd origin
   ```
---

## 3. Travail collaboratif avec git 
Quand on travaille avec git on va modifier ou créer des fichiers dans le répertoire présent en local (sur notre ordinateur)

### 3.1 Flux de travail de base
1. **Récupérer les dernières modifications** : Avant de commencer à travailler, il est important de synchroniser votre copie locale avec le repository distant. 
   - **Avec `git pull`** :
     ```bash
     git pull origin main
     ```
     **Explication** :
     - `git pull` : télécharge les dernières modifications depuis le repository distant et les intègre directement dans votre copie locale.
     - `origin` : réfère au repository distant.
     - `main` : la branche principale du projet.

   - **Avec `git fetch`** :
     ```bash
     git fetch origin
     ```
     **Explication** :
     - `git fetch` : récupère les dernières modifications du repository distant sans les intégrer dans votre copie locale. Cela vous permet de voir les changements disponibles avant de les fusionner.
     - `origin` : réfère au repository distant. Par défaut, `origin` est le nom du repository distant principal, mais cela peut être différent selon votre configuration.

![image](https://github.com/user-attachments/assets/459c75f7-2b8f-44a3-8040-1ff3d86953c1)

   Après avoir utilisé `git fetch`, vous pouvez utiliser `git merge` ou `git rebase` pour intégrer les modifications récupérées dans votre branche locale.

![image](https://github.com/user-attachments/assets/050327f0-c54f-41b0-844a-ed2b27f07b3b)


3. **Créer une branche** : Créez une branche pour vos modifications afin de ne pas affecter directement la branche principale (« main »)

Une branche est une copie du code du répertoire à un instant T, par défaut la branche du répertoire se nomme "main" ou "master", on ne va pas apporter de modification directement sur cette branche car elle représente le projet final.
`git branch` permet de visualiser toutes les branches du dépôt


Ainsi, il est préférable de créer de nouvelles branches afin de réaliser des modifications sans modifier le projet principal. Pour créer une nouvelle branche :
   ```bash
   git branch dev
   git checkout dev 
   ```
   **Explication** :
   - `git branch dev` : crée une nouvelle branche nommé dev
   - `git checkout dev` : basculer sur la branche dev
  
   Ou : 
   ```bash
   git checkout -b nom-de-la-branche
   ```   
   **Explication** :
   - `git checkout -b` : crée une nouvelle branche et bascule dessus.
   - `nom-de-la-branche` : nom que vous donnez à votre branche, par exemple « ajout-feature-x ».

On va créer une nouvelle branche par fonctionnalité, pour cela on se positionne sur la branche dev : 
  - git checkout dev
  - git branch nomfonctionnalite

Une fois le projet opérationnel, on pourra merger la branche dev vers la branche master 

4. **Faire des modifications et des commits** :

L'index est un espace temporaire contenant les modifications prêtes à être "commitées", les modifications sont ajoutés dans l'index suite au git add.

Pour cela on execute le code suivant dans l’invite de commande, qui va permettre de se placer dans le répertoire concerné
  ```bash
  cd SISE_Enedis/
  ```
Une fois à l’intérieur, on peut ajouter un fichier avec :
  ```bash
  git add nomdufichier  (Ou git add .  pour ajouter tout les changements)
  ```

Ajoutez les modifications à l’index :
  ```bash
  git add chemin/vers/fichier
  ```
  **Explication** :
  - `git add` : prépare les fichiers modifiés pour le prochain commit.

Pour l’instant le git add a simplement ajouter les fichiers à une liste temporaire qui est en attente d’envoi dans le dépot local.

L'historique d'un projet est une séquence de « photos », contenant l'état de tous les fichiers du projet. Ces « photos » s'appellent des commits, et possèdent : une date, un auteur, une description textuelle, un lien vers le(s) commit(s) précédent(s)

On va donc empaqueter toutes les modifications dans un commit, c’est une sorte de paquet contenant toutes les modifications correspondant à une version : 
  ```bash
  git commit –m "Ajout méthodes".
  ```

 **Explication** :
 - `git commit` : enregistre les modifications dans le repository local.
 - `-m` : permet de fournir un message descriptif pour le commit.



5. **Envoyer vos modifications sur GitHub** :

Ensuite on peut envoyer ce pack (commit) dans le repository en ligne :
  ```bash
  git push
  ```
  - Le `git push` pousse le contenu du repositoy local vers le distant. Cela comprend à la fois les fichiers commités que la branche locale.

- **Première fois** que vous poussez une branche locale vers une branche distante, utilisez :
  ```bash
  git push --set-upstream origin dev
  ```
- Pour pousser des commits sur une branche déjà configurée ou sans besoin de configuration supplémentaire, utilisez simplement :
  ```bash
  git push origin dev
  ```
- **Explication** :
   - `git push` : transfère vos commits vers le repository distant.
   - `dev` : est le nom de la branche que vous souhaitez pousser.


Pour intégrer les modifications d’une branche à une autre, on se place sur la branche main ou dev avec git checkout et on execute : 
  ```bash
  git merge branche_fnc
  ```
  - Git merge fusionne les commits de la branche branche_fnc vers la branche main ou dev (en fonction de sur laquelle on s'est placé).

### 3.2 Créer une pull request (PR)
Le pull request montre aux autres collaborateurs les changements sur notre branche et leur permet d'accepter, rejeter ou suggérer des changements supplémentaires. C'est une demande formelle de révision des modifications par les pairs avant intégration.
Comment s'y prendre?
1. Rendez-vous sur le repository sur GitHub.
2. Cliquez sur le bouton « Pull Request ».
3. Comparez votre branche avec « main » et créez une pull request.
4. Ajoutez un commentaire expliquant vos modifications.
5. Attendez la validation ou les retours des autres membres de l’équipe.

### 3.3 Schéma récapitulatif des commandes git 
- Le working directory correpond au dossier du projet sur l'ordinateur
- Le stage ou l'index est un intermediaire entre le working directory et le repository, représentant tous les fichiers modifiés que l'on souhaite voir apparaitre dans la prochaine version de code
- Le repository est le dépôt local
- Le dépôt Github est le dépôt distant 

![image](https://github.com/user-attachments/assets/534b41c9-3bad-491c-b7d9-2d3d99486b49)
![image](https://github.com/user-attachments/assets/1bdae018-16e2-42db-817a-802a76664ef6)

---

## 4. Gestion des conflits

Un conflit survient lorsque deux membres modifient la même partie du code. Voici comment les résoudre :

1. **Identifiez le conflit** : Git indique les fichiers en conflit après un « pull » ou une tentative de fusion.
2. **Résolvez manuellement le conflit** :
   - Ouvrez les fichiers conflictuels.
   - Recherchez les sections marquées par `<<<<<<<`, `=======` et `>>>>>>>`.
   - Choisissez ou combinez les modifications nécessaires.
3. **Enregistrez les modifications et marquez le conflit comme résolu** :
   ```bash
   git add chemin/vers/fichier
   ```
4. **Finalisez la fusion** :
   ```bash
   git commit -m "Résolution de conflit"
   ```

---

## 5. Bonnes pratiques et Schema recapitulatif 
- **Commitez souvent** : Réalisez de petits commits avec des messages clairs.
- **Utilisez des branches** pour chaque fonctionnalité ou correction.
- **Synchronisez régulièrement** votre copie locale avec « main ».
- **Ajoutez des commentaires sur vos pull requests** pour faciliter la revue.
- **Communiquez avec votre équipe** pour éviter les conflits inutiles.

![image](https://github.com/user-attachments/assets/33442f47-e8d2-4884-a739-6daecfa24bc9)


