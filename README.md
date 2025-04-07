# lfs-bookstore

## Steps to setup the virtual enviroment and starting the flask server

1. Create a python virtual environment
   ```zsh
   python3 -m venv .venv
   ```
2. Activate the virtual environment
   1. some IDEs does this automatically, but from a unix terminal can it be done like this:
   ```zsh
   . .venv/bin/activate
   ```
3. Download the pip dependencies
   ```zsh
   pip install -r requirements.txt
   ```
4. Run the flask server
   ```zsh
   flask --app app run
   ```