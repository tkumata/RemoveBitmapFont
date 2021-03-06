# Howto Install Fontforge.

## For Raspberry Pi 3 Jessie

1. sudo vi /etc/dphys-swapfile
```
CONF_SWAPSIZE=2048
```
1. sudo systemctl stop dphys-swapfile
1. sudo systemctl start dphys-swapfile
1. sudo apt-get update
1. sudo apt-get upgrade
1. sudo apt-get install build-essential curl git m4 ruby texinfo libbz2-dev libcurl4-openssl-dev libexpat-dev libncurses-dev zlib1g-dev libglib2.0 libglib2.0-dev
1. git clone https://github.com/fontforge/fontforge.git
1. cd fontforge
1. ./bootstrap && ./configure --enable-pyextension --without-x [^1]
1. make
1. sudo make install
1. add 'export LD\_LIBRARY\_PATH=/usr/local/lib:$LD\_LIBRARY\_PATH' to your .bashrc [^2]

### Result

![Screenshot](./images/rpi3ff-ss.png)

## For Windows Subsystem Linux (Bash on Windows)

1. Install [linuxbrew](http://linuxbrew.sh)
1. ln -s \`which gcc\` \`brew --prefix\`/bin/gcc-5.4
1. brew install -vd fontforge [^3]
1. add 'export LD\_LIBRARY\_PATH=/home/linuxbrew/.linuxbrew/lib:$LD\_LIBRARY\_PATH' to your .bashrc

### Result

![Screenshot](./images/wslff-ss.png)

Windows だけで完結するのが嬉しい。[^4]

-----

[^1]: ラズパイでは libxdmcp, xproto 諸々ライブライなどインストールできないので --without-x を付けて CLI の fontforge にする必要がある。

[^2]: configure のオプションに --prefix=/usr を入れた場合、この行は恐らく不必要。

[^3]: libxml2 の make check でエラーが起きるので「2: ignore」を選択してください。make check 自体がおかしいだけでバイナリは正常です。もし symlink error が起きたらやはり「2: ignore」を選んでください。どうも Mac 用に /Applications に fontforge.app の symlink を張ろうとして失敗するようです。"-vd" 付けないとエラー時に選択が出てきません。なお、既にインストールしていたら、

brew upgrade -vd fontforge

[^4]: WSL から /mnt/c/*/ に mv || cp できるので大変便利。
