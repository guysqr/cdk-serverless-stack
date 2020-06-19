#!/bin/bash
source demo-config.ini

for ((i=1;i<=count;i++)); do
    echo "Pushing to ${name}-${i}"
    git push ${name}-${i}
done
