pyinstaller Platformy.py -F -c --clean -y --target-architecture x86_64 -i assets/images/icon.icns
rm Platformy.spec
rm -r build
cd dist
mv Platformy Platformy_MAC
chmod 755 Platformy_MAC