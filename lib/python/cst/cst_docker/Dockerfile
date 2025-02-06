# Build Args
ARG IMAGE=NULL
ARG PORTS=NULL
ARG INSTALL_DEPENDENCIES=NULL
ARG STEAM_USERNAME_ARG=NULL
ARG STEAM_PASSWORD_ARG=NULL

# Set base image and info
FROM ${IMAGE}:latest

# Attach Shell
SHELL ["/bin/bash", "-c"]

# Port Forwarding
EXPOSE ${PORTS}

# Update Ubuntu to latest version/Install additional dependencies
RUN apt-get update &&  \
    apt-get -y install  \
    python3  \
    wget  \
    ${INSTALL_DEPENDENCIES}

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



# todo, works exclusively for Steam platform, need to abstract games outside of steam
WORKDIR /home/gameuser/steamcmd
RUN wget -qO- "http://media.steampowered.com/installer/steamcmd_linux.tar.gz" | tar zxf - -C /home/gameuser/steamcmd
RUN chmod 777 /home/gameuser/steamcmd
RUN chmod 777 /home/gameuser/steamcmd/linux32/steamcmd

# Run install.py
WORKDIR /home/gameuser
#CMD ["python3", "cst_game/install.py"]