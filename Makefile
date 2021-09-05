PROJECT := examples-325001
APP_NAME := streamlit-demo
VERSION := 0.0.2
BASE_IMAGE := $(shell head -n1 Dockerfile | awk '{print $$2}')
TAG := gcr.io/$(PROJECT)/$(APP_NAME):$(VERSION)
CONTAINER_PORT := 8090
HOST_PORT := 8000
CID_FILE := .cid

.PHONY: build dive run deploy

all: build push deploy

build:
	docker build \
	--tag $(TAG) .

dive:
	dive build \
	--tag $(TAG) .

run:
	docker run \
		--rm \
		-d \
		--env "PORT=${CONTAINER_PORT}" \
		--publish $(HOST_PORT):${CONTAINER_PORT} \
		--cidfile=".cid" \
		$(TAG)

stop:
	docker container stop $(shell cat .cid)
	rm .cid

interactive:
	docker run \
		--rm \
		-it \
		--publish $(HOST_PORT):$(CONTAINER_PORT) \
		$(TAG) \
		bash

mounted:
	docker run \
		--rm \
		-it \
		-v $(shell pwd | sed 's/ /\\ /g'):/app \
		--workdir /app \
		--publish $(HOST_PORT):$(CONTAINER_PORT) \
		$(TAG) \
		bash
	
push:
	docker push $(TAG)

deploy: push
	gcloud run deploy $(APP_NAME) \
		--region australia-southeast1 \
		--image $(TAG)