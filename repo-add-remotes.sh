#!/bin/bash
source demo-config.ini

for ((i=1;i<=count;i++)); do
    echo "Adding remote ${name}-${i}"
    git remote add ${name}-${i} codecommit::ap-southeast-2://${name}-${i}
done
