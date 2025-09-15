#!/bin/bash
set -e

echo "[INFO] Installing Docker..."
apt-get update -y && apt-get install -y docker.io

echo "[INFO] Logging in to Docker Hub..."
echo "$DOCKERHUB_TOKEN" | docker login -u "$DOCKERHUB_USERNAME" --password-stdin

echo "[INFO] Building Docker image..."
docker build -t $DOCKERHUB_USERNAME/monitor:latest .

echo "[INFO] Pushing image to Docker Hub..."
docker push $DOCKERHUB_USERNAME/monitor:latest

echo "[SUCCESS] Image pushed to Docker Hub as $DOCKERHUB_USERNAME/monitor:latest"
