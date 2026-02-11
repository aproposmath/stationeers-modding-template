#!/bin/bash
set -e
git checkout main
git pull

cp NuGet.Config ../
cp Main.csproj.template ../
cp github-deploy.yml ../.github/workflows/deploy.yml || true

cd ..
git add Template
echo "Update done, to commit, run: git commit -m'Update Template'"
