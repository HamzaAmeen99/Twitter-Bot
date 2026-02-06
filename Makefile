.DEFAULT_GOAL := activate

activate:
	@cmd /K "myenv\Scripts\activate"

run:
	myenv\Scripts\python main.py
