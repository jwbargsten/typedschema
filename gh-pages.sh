#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
say() { echo "$*" >&2 ; }

workdir=$(mktemp -d)
publish_dir="$script_dir/docs/_build/html"
say "WORKDIR: $workdir"
say "PUBLISH_DIR: $publish_dir"
confirm() {
  # https://stackoverflow.com/questions/1885525/how-do-i-prompt-a-user-for-confirmation-in-bash-script
  read -p "${1:-Are you sure?} (y/n) " -n 1 -r
  echo    # (optional) move to a new line
  if [[ $REPLY =~ ^[Yy]$ ]]; then
    return 0
  fi
  return 1
}

confirm_or_exit() {
  if ! confirm "$@"; then
    exit 0
  fi
}

confirm_or_exit "release?"

. ./.venv/bin/activate
make docs
cd "$workdir"
git init
git checkout --orphan gh-pages
cp -vr "$publish_dir"/* "$workdir"
touch .nojekyll
git add --all
git remote add origin "git@github.com:jwbargsten/typedschema.git"
git commit -m "."
git push --force origin gh-pages
rm -rf "$workdir"
