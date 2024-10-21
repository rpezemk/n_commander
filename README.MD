# howto
To start venv type:
```
python3 -m venv .venv
```
Activate it using 
```
source .venv/bin/activate
```
NOTE: On MacOS, especially if you use zsh with powerline, activating does not modify your
PS1 variable so you may not know if you are really inside venv. to do this 
```
echo $VIRTUAL_ENV
```
You may also check `which python3` - if this shows you system python it means you are not
inside venv environment.


Then to install requirements:
```
pip install -r requirements.txt
```
To start ncommander:
```
(.venv) john@localjohn:~/.../$ python ncommander.py
```
