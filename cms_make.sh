#!/bin/bash

PROJECT=$1

usage()
{
cat << EOF
usage: $0 options
OPTIONS:
   cms_make [project_name]      project_name: NAME OF PROJECT
EOF
}

virtualenv venv
source venv/bin/activate
djangocms -p ./$PROJECT $PROJECT
