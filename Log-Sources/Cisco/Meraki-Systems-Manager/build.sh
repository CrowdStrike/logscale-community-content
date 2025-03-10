set -e

VERSION=$(grep version src/manifest.yaml | grep -o "\d*\.\d*\.\d*")
PACKAGENAME=$(grep -o "^name: .*" src/manifest.yaml | awk -F": " '{print $2}' | sed 's/\//--/g')

# Figure out the archive name.
ARCHIVE=$PACKAGENAME--${VERSION}.zip

# Delete anything that might already be here
rm -f $ARCHIVE

# Remove DS_Store files.
find . -name .DS_Store -exec rm -f {} \;

# Create a new zip archive
(
  cd src
  zip -r ../$ARCHIVE \
    manifest.yaml \
    actions \
    alerts \
    queries \
    parsers \
    dashboards \
    data \
    scheduled-searches \
    view-interactions \
    README.md
)

echo Created package $ARCHIVE
