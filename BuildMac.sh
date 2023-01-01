pyinstaller Platformy.py -F --clean -y
rm Platformy.spec
rm -r build
cd dist
mv Platformy Platformy_MAC
chmod 755 Platformy_MAC