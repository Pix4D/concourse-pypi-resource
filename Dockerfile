FROM python:3-alpine3.6
COPY dist/concourse-pypi-resource-*.tar.gz .
RUN pip install --upgrade pip==18.1 && \
    apk add --no-cache --virtual .build-deps gcc musl-dev libffi-dev libressl-dev && \
    pip install concourse-pypi-resource-*.tar.gz && \
    apk del .build-deps gcc musl-dev libffi-dev libressl-dev && \
    mkdir -p /opt/resource && \
    for script in check in out; do ln -sv $(which $script) /opt/resource/; done
ENV PIP_DISABLE_PIP_VERSION_CHECK=1