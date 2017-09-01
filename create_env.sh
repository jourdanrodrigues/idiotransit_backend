#!/usr/bin/env bash

PYTHON=""

if [ "${1}" != "" ]; then
    PYTHON="-p ${1}"
fi;


virtualenv ${PYTHON} --prompt="(idiotransit) " env
