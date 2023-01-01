pyinstaller Game.py -F -w --clean -y --target-architecture x86_64 -i icon.icns --debug all
rm Game.spec
rm -r build
# cd dist
# mv Game Platformy_MAC
# chmod 755 Platformy_MAC