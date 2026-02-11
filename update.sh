#!/bin/bash
set -e
git checkout main
git pull

cp NuGet.Config ../
cp Main.csproj.template ../Main.csproj
cp github-deploy.yml ../.github/workflows/deploy.yml || true

# cleanup to trigger rebuild
rm -r VersionGenerator/bin
rm -r VersionGenerator/obj

cd ..
git add Template
echo "Update done, to commit, run: git commit -m'Update Template'"
