# Install

* Clone this repository: `git clone https://github.com/nfagan/sc_games.git`
* Install [conda](https://www.anaconda.com/) if you don't already have it.
* If on macOS, open a terminal tab and verify that executing the command `conda info` does not produce an error.
* If on Windows, search the start menu for 'Anaconda prompt', and open it.
* Create a new empty environment with python 3.8: `conda create --name sc_magic python=3.8`
* Activate the environment: `conda activate sc_magic`
* Install psychopy: `pip install psychopy`

# Run

* If not already activated, activate the `sc_magic` environment: `conda activate sc_magic`
* Run a task, defined by the value of `TASK_TYPE` in `main.py`: `python main.py`
