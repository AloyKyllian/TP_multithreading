# TP_Multithreading n°1

## Objectif

Permet de créer un projet avec une vérification lors des push.

## Commandes à réaliser pour arriver au même résultat

### Initialisation du projet

1. Allez à l'emplacement où vous souhaitez créer le projet.

```bash
uv init Nom_Projet
```

Cette commande crée un dossier nommé Nom_Projet.

2. Accédez au répertoire créé.

```bash
cd Nom_Projet
```

### Création d'une clé SSH pour GitHub

1. Générez une clé SSH :

```bash
ssh-keygen -t ed25519
```

Cela crée une clé SSH au format ed25519.

2. Affichez la clé publique :

```bash
cat ~/.ssh/id_ed25519.pub
```

3. Copiez la clé affichée et ajoutez-la à votre compte GitHub dans les Paramètres > SSH and GPG keys.
4. Configurez votre identité Git :

```bash
git config --global user.name "John Doe"
git config --global user.email johndoe@example.fr
```

### Connexion au dépôt GitHub et premier push

1. Ajoutez l'URL du dépôt GitHub :

```bash
git remote add origin git@github.com:votre-nom/votre-dépôt.git
```

2. Préparez les fichiers pour le commit :

```bash
git add .
git commit -m "start uv project"
```

3. Assurez-vous que la branche principale se nomme main :

```bash
git branch -M main ->
```

4. Envoyez les modifications vers GitHub :

```bash
git push -u origin main
```

### Ajout du fichier pre_commit.yaml pour les vérifications automatiques

1. Téléchargez le fichier de configuration :

```bash
curl https://gitlab.laas.fr/gsaurel/teach/-/raw/main/.pre-commit-config.yaml -o .pre-commit-config.yaml
```

2. Installez les dépendances nécessaires :

```bash
uv add --dev pre-commit
uv run pre-commit install
```

3. Exécutez les vérifications configurées sur tous les fichiers :

```bash
uv run pre-commit run -a
```

4. Committez et envoyez les modifications :

```bash
git add .
git commit -m "setup tooling"
git push
```

### Ajout d'une licence sur GitHub

1. Allez sur GitHub et créez manuellement un fichier nommé LICENSE.
2. Sélectionnez une licence (recommandation du professeur : MIT).
3. Synchronisez les modifications localement :

```bash
git pull
```

### Création du fichier pour la CI (Continuous Integration)

1. Créez le fichier .github/workflows/ci.yml.
2. Ajoutez-y le contenu suivant pour exécuter les outils et tests :

```yaml
name: ci

on: [push]

jobs:
  uv-example:
    name: python
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Run tools
        run: uv run pre-commit run -a

      - name: Run tests
        run: uv run python -m unittest
```

3. Pour tester plusieurs versions de Python, modifiez ainsi :

```yaml
name: ci

on: [push]

jobs:
  uv-example:
    name: python
    runs-on: ubuntu-latest

    strategy:
      matrix:
        python-version:
          - "3.10"
          - "3.11"
          - "3.12"

    steps:
      - uses: actions/checkout@v4

      - name: Install uv
        uses: astral-sh/setup-uv@v3

      - name: Set up Python
        run: uv python install ${{ matrix.python-version }}

      - name: Install the project
        run: uv sync --all-extras --dev

      - name: Run tools
        run: uv run pre-commit run -a

      - name: Run tests
        run: uv run python -m unittest
```

On peut voir son effet sur l'onglet action sur le repo github
Pour remplir le yaml (ref https://docs.astral.sh/uv/guides/integration/github)

### Ajout de numpy et création d'un test unitaire

1. Installez numpy dans le projet :

```bash
uv add numpy
```

2. Téléchargez un fichier d'exemple contenant des classes et des méthodes :

```bash
curl https://gitlab.laas.fr/gsaurel/teach/-/raw/main/src/task.py -o task.py
```

3. Créez un fichier de test nommé test_task.py (la nomenclature est importante) :

```python
import unittest
import numpy as np
from task import Task

class TestTask(unittest.TestCase):
    def test_work(self):
        task = Task()
        task.work()
        np.testing.assert_allclose(np.dot(task.a, task.x), task.b)

if __name__ == "__main__":
    unittest.main()
```

4. Committez et envoyez les modifications :

```bash
git add .
git commit -m "task & test"
git push
```

source $HOME/.local/bin/env


Pour une meme tache
time minion.py 0.40308431000084965
resul minion [-2.86928542 -0.21209887 -0.48722827 ...  1.86955375  1.81221005
 -1.08180001]
time c++ 109.21178436279297
result c++ [-2.86924243 -0.21211024 -0.48720407 ...  1.86960566  1.81211662
 -1.0818063 ]


cmake -B build -S . -DCMAKE_BUILD_TYPE=Release
