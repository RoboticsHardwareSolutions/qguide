#!/bin/bash

set -e

echo "Moving to project directory"

cd "${CI_PROJECT_DIR}"

echo "Unshallowing repository..."

git fetch --unshallow || true

echo "Checking out ${CI_COMMIT_REF_NAME}..."

git checkout "${CI_COMMIT_REF_NAME}"

echo "Setting up credentials"

git config user.email "${BOT_EMAIL}"
git config user.name "${BOT_NAME}"

url_host=$(git remote get-url origin | sed -e "s/https:\\/\\/gitlab-ci-token:.*@//g")
git remote set-url origin "https://${BOT_NAME}:${BOT_TOKEN}@${url_host}"

echo "Adding readme file to changesets"

git add README.md

echo "Trying to commit readme"

git commit -m "[skip ci] Update documentation" || (echo "Nothing to commit, exiting"; exit 0)

echo "Pushing changes"

git push origin "${CI_COMMIT_REF_NAME}"
