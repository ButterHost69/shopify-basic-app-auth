.PHONY: run, db_up, db_down

run:
	sudo .venv/bin/python3 -m uvicorn app.main:app --app-dir ./src --reload --port 80

db_up:
	sudo docker compose up

db_down:
	sudo docker compose down -v