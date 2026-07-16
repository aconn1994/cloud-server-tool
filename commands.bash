# Manual bootstrap for an Arma 3 dedicated server on an Ubuntu EC2 instance.
#
# Run these as the default `ubuntu` user. Provisioning (apt, user creation)
# needs sudo; the game server itself runs as the non-root `gameuser` so that
# all game files are owned by that account (avoids the root-owned-file
# permission problems). The security group must allow inbound UDP 2302-2306
# (2303 = Steam query, 2304 = Steam master) so the server shows in the
# in-game Server Browser and not only via Direct Connect.

set -euo pipefail

GAME_USER="gameuser"
GAME_HOME="/home/${GAME_USER}"
S3_BUCKET="s3://cst-resources"
WHL="cloud_server_tool-0.1.0-py3-none-any.whl"
ASSET_PATH="${S3_BUCKET}/game_assets/arma_three/assets"

# ---- 1. System provisioning (root, one-time) ----
# lib32gcc-s1 is required by the 64-bit Arma 3 server binary and by SteamCMD.
sudo dpkg --add-architecture i386
sudo apt-get update
sudo apt-get install -y python3-pip awscli curl lib32gcc-s1

# ---- 2. Create the dedicated non-root game user ----
if ! id "${GAME_USER}" >/dev/null 2>&1; then
  sudo adduser --disabled-password --gecos "" "${GAME_USER}"
fi

# ---- 3. Pull the tool + assets from S3 into the game user's home ----
sudo -u "${GAME_USER}" mkdir -p "${GAME_HOME}/assets"
sudo aws s3 cp "${S3_BUCKET}/whl/${WHL}" "${GAME_HOME}/${WHL}"
sudo aws s3 cp "${S3_BUCKET}/whl/game_setup_runner.py" "${GAME_HOME}/game_setup_runner.py"
sudo aws s3 cp "${ASSET_PATH}/mod-list.html" "${GAME_HOME}/assets/mod-list.html"
sudo aws s3 cp "${ASSET_PATH}/server.cfg" "${GAME_HOME}/assets/server.cfg"
sudo aws s3 cp "${ASSET_PATH}/server.Arma3Profile" "${GAME_HOME}/assets/server.Arma3Profile"
sudo aws s3 cp "${ASSET_PATH}/server.vars.Arma3Profile" "${GAME_HOME}/assets/server.vars.Arma3Profile"
sudo chown -R "${GAME_USER}:${GAME_USER}" "${GAME_HOME}"

# ---- 4. Install the tool for the game user ----
sudo -u "${GAME_USER}" -H bash -lc \
  "pip install --user --break-system-packages --force-reinstall '${GAME_HOME}/${WHL}'"

# ---- 5. Launch ----
# Credentials are prompted (password hidden) and exported to the environment,
# so they never land in shell history/logs or in the server process arguments
# (SteamCMDClient reads STEAM_USERNAME / STEAM_PASSWORD directly). First run
# installs SteamCMD + game + mods, places the config/profile, and creates the
# steamclient.so symlinks the server needs to register with Steam. Add
# --expedite-launch on later runs to skip installs.
read -rp "Steam username: " STEAM_USERNAME
read -rsp "Steam password: " STEAM_PASSWORD; echo

sudo -u "${GAME_USER}" -H \
  STEAM_USERNAME="${STEAM_USERNAME}" STEAM_PASSWORD="${STEAM_PASSWORD}" \
  bash -lc "cd '${GAME_HOME}' && python3 -u game_setup_runner.py \
    --module-name cst_game.games.arma_three.setup \
    --operating-system linux \
    --debug \
    --kwargs dlcs=ws"

# ---- Copy server logs to S3 (optional) ----
# sudo aws s3 cp "${GAME_HOME}/steamcmd/arma_three/server_console.log" "${S3_BUCKET}/logs/server_console.log"
