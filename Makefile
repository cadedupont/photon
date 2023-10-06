init: requirements.txt
	pip install -r requirements.txt

run: main.py
	python src/main.py

clean:
	rm -rf __pycache__/