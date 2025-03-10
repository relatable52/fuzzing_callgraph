FROM cifuzz/jazzer

RUN ln -sf /busybox/env /usr/bin/env

# Set user and group
ARG USER=jazzer
ARG GROUP=users
ARG UID=1000
ARG GID=100

# Delete user and group to ensure they do not exist
RUN OLD_USER=$(awk -F\: "\$3 == ${UID} {print \$1}" /etc/passwd); if [ ! -z "$OLD_USER" ]; then echo "delete user $OLD_USER"; deluser $OLD_USER; fi
RUN OLD_GROUP=$(awk -F\: "\$3 == ${GID} {print \$1}" /etc/group); if [ ! -z "$OLD_GROUP" ]; then echo "delete group $OLD_GROUP"; delgroup $OLD_GROUP; fi

# Add user and group
RUN addgroup --gid ${GID} ${GROUP}
RUN adduser --uid ${UID} -G ${GROUP} --shell /bin/sh -D ${USER}

# Switch to user
USER ${UID}:${GID}