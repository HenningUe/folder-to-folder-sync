#!/bin/bash

mkdir .repos
cd /workspaces
git clone https://github.com/HenningUe/simple-file-mirror.git
cd /workspaces/folder-to-folder-sync/.repos
ln -s /workspaces/simple-file-mirror/simplefilemirror simplefilemirror