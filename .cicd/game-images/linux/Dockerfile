# Set base image and info
FROM ubuntu

# Set Game lib args
#ARG GAME_MODULE=cst_game.games.arma_three.setup
#ARG OS=linux

# Attach Shell
SHELL ["/bin/bash", "-c"]

USER root

# Install Dependencies
RUN apt-get update && apt-get -y install python3-pip

# Install UV
#ENV UV_TOOL_BIN_DIR=/bin
#COPY --from=ghcr.io/astral-sh/uv:0.6.12 /uv /uvx /bin/

ARG CICD_PATH=.cicd/python/cst_cicd
ARG CST_PATH=lib/python/cloud_server_tool
ARG RUNNER_FILE=game_setup_runner.py

# Add cst_game directory
WORKDIR /home/gameuser
COPY ${CICD_PATH}/runners/${RUNNER_FILE} ${CST_PATH}/dist/cloud_server_tool-0.1.0-py3-none-any.whl /home/gameuser/

RUN pip install cloud_server_tool-0.1.0-py3-none-any.whl --break-system-packages
#    python3 -u ${RUNNER_FILE} --module-name ${GAME_MODULE} --operating-system ${OS} --debug

#CMD ["python3", "-u", "game_setup_runner.py", "--module-name", "cst_game.games.arma_three.setup", "--operating-system", "linux", "--debug"]
# python3 -u game_setup_runner.py --module-name cst_game.games.arma_three.setup --operating-system linux --debug