#!/bin/bash

# Update system packages
echo "Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install required system dependencies
echo "Installing system dependencies..."
sudo apt install -y python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools python3-venv git

# Install Docker if not already installed
if ! [ -x "$(command -v docker)" ]; then
    echo "Installing Docker..."
    sudo apt install -y apt-transport-https ca-certificates curl software-properties-common
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
    sudo apt update
    sudo apt install -y docker-ce
    sudo systemctl enable docker
    sudo systemctl start docker
    sudo usermod -aG docker $USER
    echo "Docker installed successfully!"
else
    echo "Docker is already installed."
fi

# Create application directory
echo "Creating application directory..."
mkdir -p ~/financial_platform

# Copy files to application directory
echo "Setting up application files..."
cp app.py ~/financial_platform/
cp requirements.txt ~/financial_platform/
cp config.toml ~/financial_platform/
cp Dockerfile ~/financial_platform/

# Navigate to application directory
cd ~/financial_platform

# Build Docker image
echo "Building Docker image..."
docker build -t financial_platform .

# Run Docker container
echo "Starting Docker container..."
docker run -d --name financial_platform -p 8080:8080 --restart always financial_platform

echo "Setup completed successfully!"
echo "Financial Intelligence Platform is now running at http://<your-server-ip>:8080"
