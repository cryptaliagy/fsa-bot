FROM ubuntu:focal

WORKDIR /app

RUN apt-get update

RUN DEBIAN_FRONTEND="noninteractive" apt-get install python3-dev python3-pip graphviz graphviz-dev pkg-config gcc -y --no-install-recommends

COPY . /app

COPY ./.env /app

RUN python3 -m pip install .

CMD ["fsa-bot"]
