#!/bin/bash

get_total_cameras() {
    python retrieve_images.py get_total_cameras
}

if [[ $# -eq 1 ]]; then
    TOTAL_CAMERAS=$1
else
    get_total_cameras
    TOTAL_CAMERAS=$(cat total_cameras.txt)
fi

# Check if TOTAL_CAMERAS is set and is a valid number
if ! [[ "${TOTAL_CAMERAS}" =~ ^[0-9]+$ ]]; then
    echo "Error: TOTAL_CAMERAS is not a valid number."
    exit 1
fi

# Server is rate limited to 100 requests per API call.
# Lower batch size slows down asynchronous processing.
BATCH_SIZE=100

for((i = 0; i < TOTAL_CAMERAS; i += BATCH_SIZE)); do
    IMAGES_LEFT_TO_RETRIEVE=$((TOTAL_CAMERAS-i))
    
    if [[ ${IMAGES_LEFT_TO_RETRIEVE} -lt ${BATCH_SIZE} ]]; then
        BATCH_SIZE=${IMAGES_LEFT_TO_RETRIEVE}
    fi

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
