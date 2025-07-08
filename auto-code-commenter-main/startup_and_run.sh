#!/bin/bash

# GIT CLONE the code commenter and install the dependencies
git clone --branch v1.0.0 https://github.com/Manav-Khandurie/auto-code-commenter.git && mv -f auto-code-commenter/app code-auto-commenter && rm -rf auto-code-commenter && pip install -r code-auto-commenter/requirements.txt

# RUN THE code-auto-commenter with appropriate config file and target repo
python -m code-auto-commenter.cli --config ai-commenter.yaml  --src src/game