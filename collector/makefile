REGION := europe-west3
PROJECT_ID := news-ticker-381212
ARTIFCATS_REPO := news-ticker
SERVICE_NAME := collector

run-dev:
	uvicorn main:app --reload

test:
	python -m unittest test

cleanup:
	rm -r logs/application_logs.log

build:
	docker build -t $(SERVICE_NAME) -f docker/Dockerfile .

run:
	docker run --name $(SERVICE_NAME) -p 8000:8000 $(SERVICE_NAME):latest

stop:
	docker stop $(SERVICE_NAME); docker rm $(SERVICE_NAME)

deploy:
	docker build -t $(REGION)-docker.pkg.dev/$(PROJECT_ID)/$(ARTIFCATS_REPO)/$(SERVICE_NAME) -f docker/Dockerfile .
	gcloud auth configure-docker $(REGION)-docker.pkg.dev
	docker push $(REGION)-docker.pkg.dev/$(PROJECT_ID)/$(ARTIFCATS_REPO)/$(SERVICE_NAME)
	gcloud run deploy --image $(REGION)-docker.pkg.dev/$(PROJECT_ID)/$(ARTIFCATS_REPO)/$(SERVICE_NAME) --platform managed --port 8000 --memory 512M --location=$(REGION)
