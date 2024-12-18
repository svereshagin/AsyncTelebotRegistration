COMPOSE_FILE=docker-compose.yml

up:
	@docker-compose -f $(COMPOSE_FILE) up -d

down:
	@docker-compose -f $(COMPOSE_FILE) down

restart:
	@docker-compose -f $(COMPOSE_FILE) down
	@docker-compose -f $(COMPOSE_FILE) up -d

build:
	@docker-compose -f $(COMPOSE_FILE) build

ps:
	@docker-compose -f $(COMPOSE_FILE) ps

logs:
	@docker-compose -f $(COMPOSE_FILE) logs -f

clean:
	@docker-compose -f $(COMPOSE_FILE) down --rmi all --volumes --remove-orphans

app-shell:
	@docker-compose -f $(COMPOSE_FILE) exec app bash

postgres-shell:
	@docker-compose -f $(COMPOSE_FILE) exec postgres bash

test:
	@docker-compose -f $(COMPOSE_FILE) exec app pytest

help:
	@echo "Usage: make [command]"
	@echo "Commands:"
	@echo "  up             Поднять контейнеры"
	@echo "  down           Остановить и удалить контейнеры"
	@echo "  restart        Перезапустить контейнеры"
	@echo "  build          Собрать контейнеры"
	@echo "  ps             Показать статус контейнеров"
	@echo "  logs           Просмотр логов в реальном времени"
	@echo "  clean          Остановить контейнеры и удалить образы и тома"
	@echo "  app-shell      Запуск bash внутри контейнера app"
	@echo "  postgres-shell Запустить bash внутри контейнера postgres"
	@echo "  test           Запустить тесты"



# Создает шаблонный файл .pot из app.py (просканирует например app.py и найдёт места для переводов)
create_for_app_translate:
	xgettext -d messages -o src/middlewares/locales/messages.pot src/app/handlers.py --from-code UTF-8

# Создает файл для переводов
translate_file:
# Для русской локали (RU):
	msginit -l ru_RU.UTF-8 -o src/middlewares/locales/ru/LC_MESSAGES/messages.po -i src/middlewares/locales/messages.pot --no-translator
# Для итальянской локали (IT):
	msginit -l it_IT.UTF-8 -o src/middlewares/locales/it/LC_MESSAGES/messages.po -i src/middlewares/locales/messages.pot --no-translator
# Для английской локали (EN):
	msginit -l en_US.UTF-8 -o src/middlewares/locales/en/LC_MESSAGES/messages.po -i src/middlewares/locales/messages.pot --no-translator

# Компилирует переводы в .mo файлы
compile_translator_ru:
	msgfmt -o src/middlewares/locales/ru/LC_MESSAGES/messages.mo src/middlewares/locales/ru/LC_MESSAGES/messages.po

compile_translator_it:
	msgfmt -o src/middlewares/locales/it/LC_MESSAGES/messages.mo src/middlewares/locales/it/LC_MESSAGES/messages.po

compile_translator_en:
	msgfmt -o src/middlewares/locales/en/LC_MESSAGES/messages.mo src/middlewares/locales/en/LC_MESSAGES/messages.po