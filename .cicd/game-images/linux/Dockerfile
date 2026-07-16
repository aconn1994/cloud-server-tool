# Set base image and info
FROM ubuntu:latest

USER root
ARG PORTS=NULL

# Attach Shell
SHELL ["/bin/bash", "-c"]

EXPOSE ${PORTS}

# Install Dependencies
RUN apt-get update && apt-get -y install python3-pip

ARG CICD_PATH=.cicd/python/cst_cicd
ARG CST_PATH=lib/python/cloud_server_tool
ARG RUNNER_FILE=game_setup_runner.py

# Add cst_game directory
WORKDIR /home/gameuser
COPY ${CICD_PATH}/runners/${RUNNER_FILE} ${CST_PATH}/dist/cloud_server_tool-0.1.0-py3-none-any.whl /home/gameuser/
COPY tmp/assets /home/gameuser/assets/

RUN pip install cloud_server_tool-0.1.0-py3-none-any.whl --break-system-packages

#CMD ["python3", "-u", "game_setup_runner.py", "--module-name", "cst_game.games.arma_three.setup", "--operating-system", "linux", "--debug"]
# python3 -u game_setup_runner.py --module-name cst_game.games.arma_three.setup --operating-system linux --debug --local