#!/bin/bash

./tvmaze2xml.py
mythfilldatabase --refresh 1 --file --sourceid 1 --xmlfile ./xmltv.xml
