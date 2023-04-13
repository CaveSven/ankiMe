#!/usr/bin/env bash

set -eux

##### Functions

usage()
{
    echo "usage: deploy.sh -h"
}

##### Main

while getopts "h" option; do
  case ${option} in
    h )
      usage
      exit 0
      ;;
    \? )
      echo "Invalid option: -$OPTARG" 1>&2
      usage
      exit 1
      ;;
  esac
done

##### Constants

CURRENT_TIMESTAMP=$(date +%s)
SCRIPT=$(readlink -f "$0")
SCRIPT_DIR=$(dirname "$SCRIPT")
LOCAL_PROJECT_ROOT="${SCRIPT_DIR}/.."
LOCAL_BUILD_DIR="${SCRIPT_DIR}/ankiMe"
LOCAL_DATA_OUT_DIR="${LOCAL_PROJECT_ROOT}/data_out"

source "$LOCAL_BUILD_DIR"/.env # sets DOMAIN

# shellcheck disable=SC2088
REMOTE_USER="admin"
REMOTE_HOME="/home/${REMOTE_USER}"
REMOTE_PROJECT_ROOT="${REMOTE_HOME}/ankiMe"
REMOTE_BKP_DIR="${REMOTE_HOME}/ankiMeBkp"
REMOTE_DATA_OUT_DIR="${REMOTE_PROJECT_ROOT}/data_out"
##### Functions

do-remote() {
  ssh -o IdentitiesOnly=yes "${REMOTE_USER}@${DOMAIN}" "$@"
}

backup-remote-db() {
  if do-remote "test -e ${REMOTE_DATA_OUT_DIR}"; then
    do-remote "rm -rf ${REMOTE_BKP_DIR} && mv ${REMOTE_DATA_OUT_DIR} ${REMOTE_BKP_DIR}"
    scp -r "admin@${DOMAIN}:${REMOTE_BKP_DIR}" "${LOCAL_DATA_OUT_DIR}/${CURRENT_TIMESTAMP}"
    rm -rf "${LOCAL_DATA_OUT_DIR}/latest" && ln -s "${LOCAL_DATA_OUT_DIR}/${CURRENT_TIMESTAMP}" "${LOCAL_DATA_OUT_DIR}/latest"
  fi
}

restore-remote-db() {
  if do-remote "test -e ${REMOTE_BKP_DIR}"; then
    do-remote "rm -rf ${REMOTE_DATA_OUT_DIR} && mv ${REMOTE_BKP_DIR} ${REMOTE_DATA_OUT_DIR}"
  fi
}

provision-remote() {
  do-remote "rm -rf ${REMOTE_PROJECT_ROOT}"
  scp -r "$LOCAL_BUILD_DIR" ${REMOTE_USER}@${DOMAIN}:${REMOTE_PROJECT_ROOT}
}

##### Provision remote

backup-remote-db
provision-remote
restore-remote-db

##### Launch

do-remote "docker compose -f ${REMOTE_PROJECT_ROOT}/docker-compose.yml up -d --build"
