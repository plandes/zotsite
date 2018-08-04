#!/bin/sh

DOCROOT_URL=smb://SERVER/PATH
ZOT_DIR=$(mktemp -d)
TARG=/v/docedit/zotero

if [ ! -d "${TARG}" ] ; then
    echo "mount ${TARG} not found--mounting ${DOCROOT_URL}..."
    osascript -e "tell application \"Finder\" to mount volume \"${DOCROOT_URL}\""
fi

echo "creating site in ${ZOT_DIR}"

zotsite export -o ${ZOT_DIR}
rsync -rltpgoDuv --delete ${ZOT_DIR}/ ${TARG}

if [ -d ${ZOT_DIR} ] ; then
    rm -r ${ZOT_DIR}
fi
