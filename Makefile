init: requirements.txt
	pip install -r requirements.txt

run: src/main.py
	python src/main.py

clean:
	rm -rf src/__pycache__/