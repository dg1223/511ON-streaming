#!/bin/bash

python retrieve_images.py get_total_cameras
TOTAL_CAMERAS=$(cat total_cameras.txt)

# Check if TOTAL_CAMERAS is set and is a valid number
if ! [[ "${TOTAL_CAMERAS}" =~ ^[0-9]+$ ]]; then
    echo "Error: TOTAL_CAMERAS is not a valid number."
    exit 1
fi

BATCH_SIZE=5

for((i = 0; i < TOTAL_CAMERAS; i += BATCH_SIZE)); do    
    START=$i
    LENGTH=${BATCH_SIZE}

    # Calculate batch number
    if [[ $i -eq 0 ]]; then
        BATCH_NUMBER=1
    elif [[ $i%5 -eq 0 ]]; then
        ((BATCH_NUMBER++))
    else
        :
    fi

    echo -e "\nBatch number: ${BATCH_NUMBER}"

    python retrieve_images.py fetch_images ${START} ${LENGTH}

done
