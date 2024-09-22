#!/bin/sh
# @meta {desc: 'zotsite export deployment', date: '2024-09-22'}


# This script "deploys" an exported website using `zotsite` to a webserver
# that also runs a samba server.
#
# Usage:
# 1. Update the DOCROOT_URL and TARG variables below
# 2. Remove the `--delete` flag to rsync during testing (careful)!
# 3. Add back the `--delete` flag and optionally add to cron
#
# Paul Landes (9/22/2024)


DOCROOT_URL=smb://YOUR/SERVER/PATH
TARG=/Volumes/YOUR/LOCAL/MOUNT/POINT
ZOT_DIR=$(mktemp -d)

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
# `--delete` is very destructive (careful)!
rsync -rltpgoDuv --delete ${ZOT_DIR}/ ${TARG}

if [ -d ${ZOT_DIR} ] ; then
    rm -r ${ZOT_DIR}
fi
