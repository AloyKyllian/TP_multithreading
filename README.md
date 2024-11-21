# TP_Multithreading n°1

## Objectif

Permet de creer un projet avec une verification lors des push

## commande a réaliser pour arriver au meme resultat

Aller a l'emplacement ou creer le pojet
uv init Nom_Projet
cd Nom_Projet

### creer une cle ssh pour github

ssh-keygen -t ed25519
cat ~/.ssh/id_ed25519.pub
copier coller le resultat aller sur github et le coller dans la cle ssh
git config --global user.name "John Doe"
git config --global user.email johndoe@example.fr

### se connecter au repo et faire le premier push

git remote add origin git@github.com:votre-nom/votre-dépôt.git
git add .
git commit -m "start uv project"
git branch -M main
git push -u origin main

### ajout du fichier pre_commit.yaml pour verifier les codes (la derniere ligne lance la verification manuellement)

curl https://gitlab.laas.fr/gsaurel/teach/-/raw/main/.pre-commit-config.yaml -o .pre-commit-config.yaml
uv add --dev pre-commit
uv run pre-commit install
uv run pre-commit run -a

git add .
git commit -m "setup tooling"
git push

### ajouter une license depuis github

aller sur github creer un fichier a la main le nommer LICENSE puis selectionner la license voulu (conseil du prof : MIT ou j'ai oublié)
git pull

### creer le fichier qui va executer les outils de verification et les tests unittaires

creer le fichier .github/workflows/ci.yml
puis le remplir comme ce qui suit (ref https://docs.astral.sh/uv/guides/integration/github)
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

ajouter les differentes verions de python à tester

### ajouter numpy au projet et faire un test unittaire

$ uv add numpy
$ curl https://gitlab.laas.fr/gsaurel/teach/-/raw/main/src/task.py -o task.py
creer un fichier test_task.py la nomenclature est importante
import unittest
import numpy as np
from task import Task

class TestTask(unittest.TestCase):
def test_work(self):
task = Task()
task.work()
np.testing.assert_allclose(np.dot(task.a, task.x), task.b)

if **name** == "**main**":
unittest.main()
$ git add .
$ git commit -m "task & test"
$ git push
