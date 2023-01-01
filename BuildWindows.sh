pyinstaller Platformy.py -F --clean -y
rm Platformy.spec
rm -r build
cd dist
mv Platformy Platformy_WIN
# chmod 755 Platformy_WIN