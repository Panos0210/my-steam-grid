#!/bin/bash
set -e  # exit if any command fails

# Repo info
REPO="https://github.com/Panos0210/my-steam-grid/archive/refs/heads/main.zip"
OUTPUT="grid.zip"

# Get username
USERNAME=${SUDO_USER:-$USER}
USERDATA_PATH="/home/$USERNAME/.local/share/Steam/userdata/"

echo "Downloading Grid..."
wget -q -O "$OUTPUT" "$REPO"

echo "Extracting Grid..."
unzip -q "$OUTPUT" -d extracted_repo

CONFIG_FOLDER_PATH="extracted_repo/my-steam-grid-main/config"
if [ ! -d "$CONFIG_FOLDER_PATH" ]; then
    echo "Error: 'config' folder not found in the extracted ZIP!"
    exit 1
fi

for folder_name in "$USERDATA_PATH"*/; do
    folder_name=$(basename "$folder_name")
    if [[ "$folder_name" =~ ^[0-9]+$ ]]; then
        DEST_PATH="$USERDATA_PATH$folder_name/config"
        mkdir -p "$DEST_PATH"
        cp -r "$CONFIG_FOLDER_PATH/"* "$DEST_PATH/"
        echo "Copied 'config' folder to: $DEST_PATH"
    fi
done

echo "Cleaning up..."
rm -rf extracted_repo
rm -f "$OUTPUT"

echo "Cleanup complete. All done!"
