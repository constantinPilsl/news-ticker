REGION := europe-west3
PROJECT_ID := news-ticker-381212
ARTIFCATS_REPO := news-ticker
SERVICE_NAME := collector

run:
	docker run -e TELEGRAM_NEWS_TICKER_DEV_BOT_TOKEN=$(TELEGRAM_NEWS_TICKER_DEV_BOT_TOKEN) --name $(SERVICE_NAME) $(SERVICE_NAME):latest

build:
	docker build -t $(SERVICE_NAME) -f docker/Dockerfile .

cleanup:
	rm -r logs/application_logs.log

stop:
	docker stop $(SERVICE_NAME); docker rm $(SERVICE_NAME)
