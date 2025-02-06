# Build Args
ARG PORTS=NULL
ARG STEAM_USERNAME_ARG=NULL
ARG STEAM_PASSWORD_ARG=NULL

# Set base image and info
FROM ubuntu:latest

# Attach Shell
SHELL ["/bin/bash", "-c"]

# Port Forwarding
EXPOSE ${PORTS}

# Update Ubuntu to latest version/Install additional dependencies
RUN apt-get update && apt-get -y install python3 wget lib32gcc-s1 lib32stdc++6

# Add game directory
RUN useradd gameuser
WORKDIR /home/gameuser

# Set Environment Variables
# Steam
ENV STEAM_USERNAME ${STEAM_USERNAME_ARG}
ENV STEAM_PASSWORD ${STEAM_PASSWORD_ARG}
ENV DIR_STEAMCMD steamcmd
ENV DIR_LOCAL_GAME arma_three
ENV DIR_LOCAL_MOD mods
ENV DIR_KEYS_DIR keys
ENV DIR_STEAM_MOD_DOWNLOAD steamapps/workshop/content
ENV GAME_SERVER_ID 233780
ENV GAME_WORKSHOP_ID 107410

ARG CST_GAME_PATH=lib/python/cst/cst_game
COPY ${CST_GAME_PATH} /home/gameuser/

# todo, works exclusively for Steam platform, need to abstract games outside of steam
WORKDIR /home/gameuser/steamcmd
RUN wget -qO- "http://media.steampowered.com/installer/steamcmd_linux.tar.gz" | tar zxf - -C /home/gameuser/steamcmd
RUN chmod -R 777 /home/gameuser
RUN chmod -R 777 /home/gameuser/steamcmd/linux32


# Run install.py
WORKDIR /home/gameuser
#CMD ["python3", "cst_game/install.py"]