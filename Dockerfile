# Set base image and info
FROM ubuntu:latest

# Attach Shell
SHELL ["/bin/bash", "-c"]

# Port Forwarding
EXPOSE 2302/udp 2303/udp 2304/udp 2305/udp 2306/udp

# Update Ubuntu to latest version/Install additional dependencies
RUN apt-get update \
    && \
    apt-get install -y \
    lib32stdc++6 \
    lib32gcc-s1 \
    wget \
    python3

# Set Environment Variables
ENV DIR_STEAMCMD steamcmd
ENV DIR_LOCAL_GAME arma_three
ENV DIR_LOCAL_MOD mods
ENV DIR_KEYS_DIR keys
ENV DIR_STEAM_MOD_DOWNLOAD steamapps/workshop/content
ENV STEAM_USERNAME <your-steam-username>
ENV STEAM_PASSWORD <your-steam-password>
ENV GAME_SERVER_ID 233780
ENV GAME_WORKSHOP_ID 107410

# Create game user and configure server scripting entities
RUN useradd gameuser
WORKDIR /home/gameuser
# ADD /dist/ /home/gameuser
# RUN tar -xvzf server_config.tar.gz
# RUN rm server_config.tar.gz

# Add steamcmd directory
WORKDIR /home/gameuser/steamcmd
RUN wget -qO- "http://media.steampowered.com/installer/steamcmd_linux.tar.gz" | tar zxf - -C /home/gameuser/steamcmd
RUN chmod 777 /home/gameuser/steamcmd
RUN chmod 777 /home/gameuser/steamcmd/linux32/steamcmd

# Run Arma 3 install
WORKDIR /home/gameuser
# CMD ["python3", "install"]