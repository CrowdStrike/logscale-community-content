set -e

VERSION=$(grep version src/manifest.yaml | grep -o "\d*\.\d*\.\d*")

# Figure out the archive name
ARCHIVE=logscale-community-content--rsyslog-rsyslog--${VERSION}.zip

# Delete anything that might already be here
rm -f Packages/$ARCHIVE

# Create a new zip archive
(
    cd src
    zip -r ../Packages/$ARCHIVE \
	manifest.yaml \
	actions \
	alerts \
	queries \
	parsers \
	dashboards \
	scheduled-searches \
	README.md
)

echo Created package $ARCHIVE