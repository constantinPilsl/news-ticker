APP_NAME := publisher

run:
	docker run -e TELEGRAM_NEWS_TICKER_DEV_BOT_TOKEN=$(TELEGRAM_NEWS_TICKER_DEV_BOT_TOKEN) --name $(APP_NAME) $(APP_NAME):latest

build:
	docker build -t $(APP_NAME) -f docker/Dockerfile .

cleanup:
	rm -r logs/application_logs.log

stop:
	docker stop $(APP_NAME); docker rm $(APP_NAME)
