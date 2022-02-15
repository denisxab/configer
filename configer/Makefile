proj_name = "configer.bin"

# Скомпилировать проект
compile:
	python -m nuitka --follow-imports main.py -o $(proj_name) && mv $(proj_name) ..

debug:
	python -m nuitka main.py --follow-imports -o $(proj_name) --remove-output