set -e

VERSION=$(grep version src/manifest.yaml | grep -o "\d*\.\d*\.\d*")
PACKAGENAME=$(grep -o "^name: .*" ./manifest.yaml | awk -F": " '{print $2}' | sed 's/\//--/g')

# Figure out the archive name.
ARCHIVE=$PACKAGENAME--${VERSION}.zip


# Delete anything that might already be here
rm -f ./$ARCHIVE

#Make Build Directory
mkdir build
cd build

#copy content and manifast to build directory
cp -R ../../Content/* .
cp ../manifest.yaml .
# Create a new zip archive
(

    zip -r ../$ARCHIVE \
	./manifest.yaml \
	./actions \
	./alerts \
	./queries \
	./parsers \
	./dashboards \
	./scheduled-searches \
	./README.md
)

cd ../
rm -rf build

echo Created package $ARCHIVE
