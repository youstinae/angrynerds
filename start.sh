#!/bin/sh


# FakeSMTP Website
# http://nilhcem.com/FakeSMTP/index.html

# to output emails in a directory
# java -jar fakeSMTP-2.0.jar -o output_directory_name

# to output email in memory
# java -jar ./tools/fakeSMTP-2.0.jar -m -s -p 2525 --output-dir temp &

# Start Flask
# export FLASK_CONFIG=dev
export FLASK_DEBUG=1
flask run