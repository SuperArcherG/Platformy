import os
import urllib.request

pathToZip = os.path.join("assets.zip")
urllib.request.urlretrieve(
    "https://superarcherg.com/Platformy/assets.zip", pathToZip)
