#!/bin/sh

DOCROOT_URL=smb://YOUR/SERVER/PATH
ZOT_DIR=$(mktemp -d)
TARG=/Volumes/YOUR/LOCAL/MOUNT/POINT

if [ ! -d "${TARG}" ] ; then
    echo "mount ${TARG} not found--mounting ${DOCROOT_URL}..."
    osascript -e "tell application \"Finder\" to mount volume \"${DOCROOT_URL}\""
fi

echo "creating site in ${ZOT_DIR}"

zotsite export -o ${ZOT_DIR}
# bail when the generation fails (i.e. Zotero is running and DB is locked);
# otherwise rsync will delete the deployed site
if [ $? -ne 0 ] ; then
    echo "website generation error"
    exit 1
fi
rsync -rltpgoDuv --delete ${ZOT_DIR}/ ${TARG}

if [ -d ${ZOT_DIR} ] ; then
    rm -r ${ZOT_DIR}
fi
