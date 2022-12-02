# build windows release
# in pyCharme terminal run: ./build_win_release.sh
printf "Version: v"
read VERSION

pyinstaller.exe onefile-pyinstaller.spec

mkdir -p dist/out
rm dist/out/*
cp dist/MB-investigator.exe dist/out/MB-investigator-v$VERSION.exe
cp README.md dist/out/README.txt
cp LICENSE dist/out/LICENSE.txt

cd dist/out || exit
7z a ../MB-investigator-v$VERSION.zip ./*
cd ../..

printf "DONE"
