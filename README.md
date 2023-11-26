# Football event data analysis using python

## Introduction

## Installation steps

Once you have cloned this repo on to your machine, create a python virtual environment using `python -m venv .venv` and activate with `source .venv/bin/activate` (.venv can be replaced with a name of your choice). When running the virtual environment, install the requirements using `pip install -r requirements.txt`. You will now be able to run the code.

In order to document the code streamlits magic commands have been disabled, so that the documentation isn't written directly to the webpage. To disable [magic](https://docs.streamlit.io/library/api-reference/write-magic/magic) commands, go the the .streamlit folder in your home directory (`cd ~/.streamlit`) and add the following code to the config.toml file (create the file yourself if it does not already exist)

```
[runner]
magicEnabled = false
```

Although not essential, this code works best when the data is stored on your local machine. When developing the code it was designed to work with the data from [this repo](https://github.com/statsbomb/open-data). At the moment, some features may not work if the data is being accessed from the statsbomb api.

## Running the code

You can run the program using the command `streamlit run src/1_🏠_Home.py` from the project's root directory (use tab to autcomplete the name of the file).

If you have not downloaded the data from the github repo linked above, then before running the code you will need to change the filepath variable to the empty string `''`. This configures the program to use the statsbomb api rather than search for the data locally. If you have downloaded the data, and have cloned both this repo and the data repo into the same parent directory (git directory) then the filepath should work. If not, you will need to replace the filepath variable with the path to your local copy of the data.
