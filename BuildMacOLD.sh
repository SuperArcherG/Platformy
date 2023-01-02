
pyinstaller Game.py -D -w --clean -y --target-architecture x86_64 -i icon.icns
rm Game.spec
rm -r build
# cd dist
# mv Game Platformy_MAC
# chmod 755 function Platformy_MAC 
