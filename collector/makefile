APP_NAME := collector

run-dev:
	uvicorn main:app --reload

test:
	python -m unittest test

cleanup:
	rm -r logs/application_logs.log

build:
	docker build -t $(APP_NAME) -f docker/Dockerfile .

run:
	docker run --name $(APP_NAME) -p 8000:8000 $(APP_NAME):latest

stop:
	docker stop $(APP_NAME); docker rm $(APP_NAME)
