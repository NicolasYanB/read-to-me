#!/bin/bash

mkdir /tts
model_path=/tts/tts_models--multilingual--multi-dataset--xtts_v2
mkdir $model_path
declare -a model_files=(
  "https://coqui.gateway.scarf.sh/hf-coqui/XTTS-v2/main/model.pth"
  "https://coqui.gateway.scarf.sh/hf-coqui/XTTS-v2/main/config.json"
  "https://coqui.gateway.scarf.sh/hf-coqui/XTTS-v2/main/vocab.json"
  "https://coqui.gateway.scarf.sh/hf-coqui/XTTS-v2/main/hash.md5"
  "https://coqui.gateway.scarf.sh/hf-coqui/XTTS-v2/main/speakers_xtts.pth"
)

for url in "${model_files[@]}"; do
  wget -P $model_path $url
done