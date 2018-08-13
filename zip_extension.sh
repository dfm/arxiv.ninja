#!/bin/sh

set -e

EXTENSION=arxiv.ninja
SRC=extension

# Set working directory to location of this script
cd $(dirname $(readlink -m "$0"))

VERSION=$(grep '"version":' "$SRC"/manifest.json | sed 's/.*"\([0-9.]*\)".*/\1/')
OUT="$EXTENSION"-"$VERSION"

# Create a zip file that can be uploaded to Firefox Addons or the Chrome Web Store
rm -f "$OUT"
cd "$SRC"
zip -r -FS ../"$OUT".zip *
echo Created .zip web extension: "$OUT".zip

