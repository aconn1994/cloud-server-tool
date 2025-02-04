FROM cst-base

COPY /local_env/ssh_entrypoint/entrypoint.sh /entrypoint.sh

RUN apt-get update --allow-insecure-repositories && \
    apt-get -y install openssh-server openrc xauth && \
    mkdir /var/run/sshd && \
    sed -i s/#PermitRootLogin.*/PermitRootLogin\ yes/ /etc/ssh/sshd_config && \
    sed -i s/AllowTcpForwarding.*/AllowTcpForwarding\ yes/ /etc/ssh/sshd_config && \
    sed -i s/X11Forwarding.*/X11Forwarding\ yes/ /etc/ssh/sshd_config && \
    sed -i s/#X11UseLocalhost.*/X11UseLocalhost\ yes/ /etc/ssh/sshd_config && \
    echo 'root:root' | chpasswd && \
    chmod g+rwx /entrypoint.sh

RUN pip install --no-cache-dir pydevd-pycharm pipenv

EXPOSE 22

ENTRYPOINT ["/entrypoint.sh"]
