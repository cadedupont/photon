# Photon
Software Engineering project for CSCE 3513.

<p align="center">
   <img src="/res/splash.jpg"/>
</p>

# Details
We will be recreating the control console for the popular Photon laser tag game. The console controls the major functionality of the game. 

# Major Components
1. Graphical Console To Input Names
2. Database connection to store relevant user data.
3. UDP server to send and recieve information over a UDP/IP network to the individual laser tag units.
4. Game loop to count score and tally up game totals.

# Run Instructions
A Makefile is included to simplify the build process. Run the following commands in the root of the project's directory.

Install the project's required dependencies:

`make init`
or
`pip install -r requirements.txt`

Run the main Python script:

`make run`
or
`python src/main.py`

Remove compiled bytecode files:

`make clean`
or
`rm -rf src/__pycache__/`

# Contributors:
- Thomas Buser   | [@tjbuser](https://github.com/tjbuser)
- Sophia Forrester | [@asophiaforrester](https://github.com/asophiaforrester)
- Cade DuPont | [@cadedupont](https://github.com/cadedupont)
- Grace Schmidt | [@GraceSchmidt1](https://github.com/GraceSchmidt1)
- Uyen Thi My Ho | [@uho2003](https://github.com/uho2003)
- Vishal Jeyam | [@vjeyam](https://github.com/vjeyam)
