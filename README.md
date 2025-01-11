# How to run program

```
python3 src/main.py
```

## Development scripts

### How to convert Qt Designer UI to Python code

```
pyside6-uic src/ui/generated/PondUI.ui -o src/ui/generated/pond_ui.py
```

### How to convert resources to Python code

```
pyside6-rcc src/ui/resources/resources.qrc -o src/ui/resources/resources_rc.py
```
