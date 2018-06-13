# riteSnicKerz
## Project Janus
Bayan Berri, Terry Guan, Brian Leung, Yuyang Zhang

## Brief Description
Course selection has been known to be a chaotic and unpredictable process. Many mistakes are typically made in the process of selecting students: lack of a lunch period, core class, physical education class, automatic removal from a given spot in a class, and losing a spot in an AP to a student who is less qualified.  

We attempt to automate student selection into courses based on factors like overall average, subject average, recommendation, etc. By automating this process we remove many possibilities for human error. The online system will also diminish the need to be physically present at program changes.  

DO DROPLET Example: [http://206.189.231.92/](http://206.189.231.92/)
Domain server: [janus.stuycs.org](janus.stuycs.org)
LocalHost:

## Instructions to Run Website Locally

### Dependencies
1. flask
2. flask_sqlalchemy

### Setup

0. Create and activate a virtual environment
   ```bash
   $ virtualenv <name>
   $ . <name>/bin/activate
   ```
1. Install all the pip dependencies
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
4. Open a browser window and go to [http://localhost:5000](http://localhost:5000)
