<b><h1>Welcome to Platformy!</h1></b>
<h2>My online platforming game!</h2>
  In this game, you navigate various puzzles and challenges to reach the end of the level. Platformy isn't as heavily about the platforming as it is the level creation and sharing.
<img src="https://superarcherg.com/images/PlatformyPromo.png">

#MacOS
```shell
$ /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
$ brew install git
$ git clone https://github.com/SuperArcherG/Platformy
$ cd Platformy
$ sudo sh install.sh
$ sudo python3 Game.py
```

#Linux

```shell
$ sudo apt update
$ sudo apt upgrade
$ sudo apt install git
$ git clone https://github.com/SuperArcherG/Platformy
$ cd Platformy
$ sudo sh install.sh
$ sudo python3 Game.py
```

NOTE: if you recieve an error when running `$ sudo sh install.sh` you may need to do the next steps:
```
$ sudo apt install nano
$ nano install.sh
```
Add "--break-system-packages" to the end

hit Ctrl + o
press enter
hit Ctrl + x

Now try the next steps again

#Windows

##NOT SUPPORTED YET


#Uninstalling

```shell
$ sudo sh cleanup.sh
$ sudo sh uninstall.sh
$ cd ..
$ sudo rm -r Platformy
```

Removing Homebrew on <b>MacOS</b>:

`/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/uninstall.sh)"`
