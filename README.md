# riteSnicKerz
## Project Janus
Bayan Berri, Terry Guan, Brian Leung, Yuyang Zhang

Welcome to Project Janus. Our project is a website to simplify the course selection. Users will be able to look at a course directory along with their transcript to streamline the selection process. There will also be a programming changing aspect to the website.

proto0: [http://206.189.231.92/](http://206.189.231.92/)

## Instruction to Run Website Locally?

### Dependencies
1. Python 2.7
   ```bash
   $ sudo apt install python2.7
   ```
2. SQLite3
   ```bash
   $ sudo apt install sqlite3
   ```
3. Pip
   ```bash
   $ sudo apt install python-pip
   ```

### Setup

0. Create and activate a virtual environment 
   ```bash
   $ virtualenv <name>
   $ . <name>/bin/activate
   ```
1. Install all the dependencies
   ```bash
   $ pip install flask flask_sqlalchemy
   ```
2. Clone this repository
   ```bash
   $ git clone https://github.com/bberri1205/riteSnicKerz.git janus
   $ cd janus/janus
   ```
3. Launch the app
   ```bash
   $ python __init__.py
   ```
4. Open a browser window and go to `http://localhost:5000`
