bin/sh

sudo apt install npm
sudo apt update
sudo apt upgrade
sudo apt list | grep node
sudo apt list | grep npm
# If curl is not install, sudo apt-get install curl
## - Need to test for this
# Check https://github.com/nvm-sh/nvm for the latest version
## - Need automated way to get "latest"
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.35.3/install.sh | exec bash
# Expected output is "nvm"
command -v nvm
# Shows installed versions
nvm ls
nvm install node
nvm install --lts
# Shows installed versions and which wone is current
nvm ls
node --version
npm --version
