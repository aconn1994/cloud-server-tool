#!/bin/sh

ssh-keygen -A

# shellcheck disable=SC2068
exec /usr/sbin/sshd -D -e $@