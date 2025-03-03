import readline
import datetime
import signal
import time 
import os 
from termcolor import colored 
from dataclasses import dataclass 

@dataclass
class User:
    name: str
    color: str 
    prefix: str

users = [
    User(name='name1', color='light_magenta', prefix='/'), 
    User(name='name2', color='cyan', prefix='+')
]

history_path = 'history.txt'

# The log history is stored as a file, each chat message on its own line. Each  
# line has the format "{timestamp}|{user}|{content}\n". 
if os.path.isfile(history_path):
    with open(history_path, 'r') as history_file: 
        history = [
            line.strip().split('|') 
            for line in history_file.readlines()
        ]
else:
    history = [] 

def display(timestamp, user, content, extranewline=False):
    """ Displays a line of text. """ 
    if isinstance(user, str):
        user = next((u for u in users if u.name == user), None) or users[0]
    timestamp = datetime.datetime.fromtimestamp(float(timestamp)) 
    strtime = timestamp.strftime('%A, %Y %B %d, %I:%M%p')
    uname = f'{user.prefix}{user.name}'
    print(f'{colored(uname, user.color)} | {strtime}')
    print(content)
    print()
    if extranewline: 
        print() 

# Display the last 10 messages in the log.
for message in history[-10:]:
    display(*message, extranewline=True)
print('---') 

# Catch stop signals and write the updated history.
def write_history(): 
    print(
        f'Writing {len(history)} messages to `{history_path}`... ', 
        end='', 
        flush=True
    )
    with open(history_path, 'w') as history_file: 
        for line in history:
            if len(line) >= 3: 
                history_file.write(f'{line[0]}|{line[1]}|{line[2]}\n')
    print('done')
def handler_stop(signum, frame):
    write_history()
    exit(0) 
signal.signal(signal.SIGINT, handler_stop) 
signal.signal(signal.SIGTERM, handler_stop) 

# Get previous user message.
if len(history) > 0:
    sender = (
        next((u for u in users if u.name == history[-1][1]), None) or 
        users[0]
    )
else: 
    sender = users[0] 

# Get messages as stream.
while True: 
    content = input('> ')
    if len(content) == 0: 
        break
    
    # Get username of who posted this (or same as previous user)
    for user in users:
        if content[0] == user.prefix:
           sender = user
           content = content[1:]
           break
    
    # Remove the last line we displayed.
    CURSOR_UP = '\033[F'
    ERASE_LINE = '\033[K'
    print(CURSOR_UP + ERASE_LINE)
    
    message = (str(int(time.time())), sender.name, content)
    history.append(message)
    display(*message)

write_history()
