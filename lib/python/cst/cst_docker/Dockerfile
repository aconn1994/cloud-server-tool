# Set base image and info
FROM ubuntu:latest

# Build Args
ARG PORTS=NULL
ARG STEAM_USERNAME_ARG=NULL
ARG STEAM_PASSWORD_ARG=NULL
ARG LOCAL_GAME_DIR=arma_three

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
ENV STEAM_USERNAME=${STEAM_USERNAME_ARG}
ENV STEAM_PASSWORD=${STEAM_PASSWORD_ARG}
ENV LOCAL_GAME_DIR=${LOCAL_GAME_DIR}

# todo, works exclusively for Steam platform, need to abstract games outside of steam
WORKDIR /home/gameuser/steamcmd
RUN wget -qO- "http://media.steampowered.com/installer/steamcmd_linux.tar.gz" | tar zxf - -C /home/gameuser/steamcmd
RUN chmod -R 777 /home/gameuser
RUN chmod -R 777 /home/gameuser/steamcmd/linux32


# Run install.py
WORKDIR /home/gameuser
CMD ["python3", "cst_game/install.py"]