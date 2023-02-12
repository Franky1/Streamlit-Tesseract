# Python **virtualenv** Setup

```shell
python -m pip install --upgrade pip
pip install --upgrade virtualenv
python -m venv venv
venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install --upgrade -r requirements-dev.txt
pip install --upgrade -r requirements.txt
# ......
deactivate.bat
```

> Last updated: 11.02.2023
