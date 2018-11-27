# InputFixer

This project aims to automatically fix buggy inputs to programs.


Assumptions:
    The code is correct -> that is, the only bug is in the input
## Quick Start

InputFixer automatically attempts to fixe buggy program inputs. The use case this program was designed for is the PythonTutor code base, though the user is welcome to make custom inFixTheory solvers as needed. Currently, the only theory inFix supports is an automatic program repair theory similar to GenProg. I hope to add additional theories in the near future. 

To get started, you will need to make a configuration file. This file is a json file that includes information such as if there are multiple sessions to repair, where the session(s) are located, which theory you are using for fixing, timeout information, and logging information, etc. I recommend using *generate\_config\_file.py* to generate your first config file.

Each session that is to be repaired must be in its own folder. What this folder must include is specified by the theory. For the genProg theory, this folder must have a file containing the bad input, and the program code. 

Once you have set up your sessions that you want to fix and you have made a config file, you are ready to run inFixer. To do so, type `python3 driver.py config\_file.json`.

For more complicated uses, you may have to create your own driver function.

## Project Structure:

What follows is a description of each file

### driver.py

A generic experiment runner using the other files. This is a good place to start making your own drivers.

### inFix\_config.py

This file contains the class `Config` which contains all of the necessary information about which theories are being used. Their is one `Config` object associated with any `Logger` object or any `InFix` object. In the vast majority of cases, there is only one `Config` per driver program.
