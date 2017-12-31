#!/bin/bash

# You probably need to update only this link
ELECTRUM_GIT_URL=git://github.com/vertcoin/electrum-vtc.git
BRANCH=master
NAME_ROOT=electrum-vtc
PYTHON_VERSION=3.5.4

if [ "$#" -gt 0 ]; then
    BRANCH="$1"
fi

# These settings probably don't need any change
export WINEPREFIX=/opt/wine64
export PYTHONDONTWRITEBYTECODE=1
export PYTHONHASHSEED=22

PYHOME=c:/python$PYTHON_VERSION
PYTHON="wine $PYHOME/python.exe -OO -B"


# Let's begin!
cd `dirname $0`
set -e

cd tmp

if [ -d "electrum-vtc-git" ]; then
    # GIT repository found, update it
    echo "Pull"
    cd electrum-vtc-git
    git checkout $BRANCH
    git pull
    cd ..
else
    # GIT repository not found, clone it
    echo "Clone"
    git clone -b $BRANCH $ELECTRUM_GIT_URL electrum-vtc-git
fi

cd electrum-vtc-git
VERSION=`git describe --tags`
echo "Last commit: $VERSION"
popd

rm -rf $WINEPREFIX/drive_c/electrum-vtc
cp -r electrum-vtc-git $WINEPREFIX/drive_c/electrum-vtc
cp electrum-vtc-git/LICENCE .

# add python packages (built with make_packages)
cp -r ../../../packages $WINEPREFIX/drive_c/electrum-vtc/

# add locale dir
cp -r ../../../lib/locale $WINEPREFIX/drive_c/electrum-vtc/lib/

# Build Qt resources
wine $WINEPREFIX/drive_c/Python27/Lib/site-packages/PyQt4/pyrcc4.exe C:/electrum-vtc/icons.qrc -o C:/electrum-vtc/lib/icons_rc.py
wine $WINEPREFIX/drive_c/Python27/Lib/site-packages/PyQt4/pyrcc4.exe C:/electrum-vtc/icons.qrc -o C:/electrum-vtc/gui/qt/icons_rc.py
wine $WINEPREFIX/drive_c/Python27/Lib/site-packages/PyQt4/pyrcc4.exe C:/electrum-vtc/icons.qrc -o C:/electrum-vtc/lib/icons_rc.py
wine $WINEPREFIX/drive_c/Python27/Lib/site-packages/PyQt4/pyrcc4.exe C:/electrum-vtc/icons.qrc -o C:/electrum-vtc/gui/vtc/icons_rc.py
wine $WINEPREFIX/drive_c/Python27/Lib/site-packages/PyQt4/pyrcc4.exe C:/electrum-vtc/style.qrc -o C:/electrum-vtc/lib/style_rc.py
wine $WINEPREFIX/drive_c/Python27/Lib/site-packages/PyQt4/pyrcc4.exe C:/electrum-vtc/style.qrc -o C:/electrum-vtc/gui/vtc/style_rc.py

cd ..

rm -rf dist/

# build standalone and portable versions
wine "C:/python$PYTHON_VERSION/scripts/pyinstaller.exe" --noconfirm --ascii --name $NAME_ROOT-$VERSION -w deterministic.spec

# set timestamps in dist, in order to make the installer reproducible
pushd dist
find  -type f  -exec touch -d '2000-11-11T11:11:11+00:00' {} +
popd

# build NSIS installer
# $VERSION could be passed to the electrum.nsi script, but this would require some rewriting in the script iself.
wine "$WINEPREFIX/drive_c/Program Files (x86)/NSIS/makensis.exe" /DPRODUCT_VERSION=$VERSION electrum.nsi

cd dist
mv electrum-vtc-setup.exe $NAME_ROOT-$VERSION-setup.exe
cd ..

echo "Done."
md5sum dist/electrum*exe
