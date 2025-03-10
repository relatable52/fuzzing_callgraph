#!/bin/sh

TIMEOUT=$1
MX=$2
shift 2

timeout --foreground $TIMEOUT \
  sbt -java-home /opt/jdk8u342-b07/jre -J-Xmx${MX} \
    "; project jcg_evaluation; $*" \
  | tee /log.txt