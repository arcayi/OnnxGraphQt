#!/bin/bash

SCRIPT_DIR=$(cd $(dirname $0)/..; pwd)
echo "SCRIPT_DIR=$SCRIPT_DIR"
docker build -t onnxgraphqt $SCRIPT_DIR -f docker/Dockerfile --progress plain