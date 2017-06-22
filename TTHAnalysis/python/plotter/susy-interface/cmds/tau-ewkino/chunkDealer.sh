#!/bin/bash

INPUT="$1"
ACTION="$2"
PREFIX="$3"

if [ "${INPUT}" == "help" ]; then
    echo "USAGE: ${0} chunksFolder [check|merge] prefix"
    echo "Default prefix: evVarFriend"
    exit 0
fi

if [ "${PREFIX}" == "" ]; then
    PREFIX="evVarFriend"
fi

CMD="$CMSSW_BASE/src/CMGTools/TTHAnalysis/macros/leptons/friendChunkAdd.sh ${PREFIX}"

if [ "${ACTION}" == "check" ]; then
    CMD="$CMSSW_BASE/src/CMGTools/TTHAnalysis/macros/leptons/friendChunkCheck.sh -z ${PREFIX} "
fi

cd ${INPUT}

echo "Running: ${CMD}"
sh ${CMD} > /tmp/datemp.temp

# Too lazy to find the awk parameter that keeps the part before the delimiter, so just used reverse
cat /tmp/datemp.temp | rev | awk -F'knuhc.' '{print $NF}' | rev | uniq | sed s/evVarFriend_// 

#if [ "${ACTION}" == "merge" ]; then
#    mkdir chunks
#    mv *.chunk*root chunks/
#fi

cd -
exit 0
