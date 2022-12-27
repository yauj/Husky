#!/bin/bash
cp -rf ./dist/Husky.app/Contents/Resources/data/ ./data
find ./data -name .DS_Store -delete
pyinstaller --noconfirm main.spec
rm -r ./dist/Husky/