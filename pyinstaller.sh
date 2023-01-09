#!/bin/bash
# Change to script directory
cd "$(dirname "$0")"
# Add /usr/local/bin to PATH
if [[ ":$PATH:" != *":/usr/local/bin:"* ]]
then
    export PATH=$PATH:/usr/local/bin
fi
# Copy current app data directory to code data directory
cp -rf ./dist/Husky.app/Contents/Resources/data/ ./data
# Delete .DS_Store file
find ./data -name .DS_Store -delete
# Run pyinstaller
pyinstaller --noconfirm main.spec
# Remove un-binded folder
rm -r ./dist/Husky/