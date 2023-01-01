pyinstaller Platformy.py -F -w --clean -y --target-architecture arm64 -i icon.icns --debu all
rm Platformy.spec
rm -r build
cd dist
mv Platformy Platformy_MAC
chmod 755 Platformy_MAC