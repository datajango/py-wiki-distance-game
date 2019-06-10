# wikipedia_game test

- Anthony L. Leotta

## Setup

I used Anaconda Python.  I noticed that Beautiful Soup uses a non-standard "import bs4".

```
conda env list
```

```
conda init --help
conda init cmd.exe
==> For changes to take effect, close and re-open your current shell. <==

conda create -n wikigame python anaconda`
conda activate wikigame
pip install -r requirements.txt
```

``
conda install --name wikigame autopep8
```

The Wikipedia game:

## Problem: 
	
  Given a starting page on Wikipedia, using connected pages, find a list of linked pages to a target page.

  For example, starting at the page: "Web Bot" and target page: "Tax Holiday". Web Bot has a link to the page "Barack Obama", which has a link to "Tax credit", which has a link to the page "Tax holiday", the end page. Therefore, the answer would be:

  Web Bot -> Barack Obama -> Tax credit -> Tax holiday

  I would run through this path way yourself to understand the problem:
  https://en.wikipedia.org/wiki/Web_Bot

## Instructions:

  We're looking for a Python program called "wikipedia_game.py" that takes a source page and target page as command line arguments and you give me the list of connected links from start to end. Please zip up the wikipedia_game.py program along with a requirements.txt (if you used any pip packages) and any other resources used to solve the problem. Try to make sure that after unzipping and installing any pip requirements that the python program will run in it's current directory. If you have a more advanced solution, for example using a database, please provide instructions to set it up.

  Given this input for the python pogram:
  python wikipedia_game.py "Web Bot" "Tax Holiday"
  We should get this output:
  Web Bot -> Barack Obama -> Tax credit -> Tax holiday

# Tips:

  - Any path can do but shorter will probably be easier
  - Run time can be long for unconnected pages
  - Feel free to use any python packages
  - Start with a closely connected pages
  - Normalizing page names and URL's is very helpful

Good luck!

 
# Testing 

```
python wikipedia_game.py "Autism" "Ancient Greek"
Autism -> Agoraphobia -> Ancient Greek

python wikipedia_game.py "Web Bot" "Tax Holiday"
5/21/2019 : Web Bot -> Barack Obama -> Tax credit -> Tax Holiday
5/23/2019 : Web Bot -> EBay -> Sales tax -> Tax Holiday

python wikipedia_game.py "Cold Spring Harbor Laboratory" "Bruce Stillman"
Cold Spring Harbor Laboratory -> Bruce Stillman

python wikipedia_game.py "Saturn V" "Ammonium perchlorate"
Saturn V -> Ares V -> Ammonium Perchlorate Composite Propellant -> Ammonium perchlorate

python wikipedia_game.py "Cold Spring Harbor Laboratory" "Saccharomyces cerevisiae"
Cold Spring Harbor Laboratory -> Bruce Stillman -> Saccharomyces cerevisiae
```

```
python wikipedia_game.py "2004 Indian Ocean earthquake"  "Tax Holiday"
python wikipedia_game.py "Barack Obama"  "Tax Holiday"
python wikipedia_game.py "Barack Obama"  "Tax credit"
python wikipedia_game.py "Tax credit"  "Tax Holiday"
python wikipedia_game.py "Cold Spring Harbor Laboratory" "Saccharomyces cerevisiae"
python wikipedia_game.py "Moog Synthesizer" "The Mamas and the Papas"
python wikipedia_game.py "Autism" "Asperger syndrome"
python wikipedia_game.py "Saturn V" "Pogo oscillation"
python wikipedia_game.py "Pogo oscillation" "Rocket engine"
python wikipedia_game.py "Saturn V" "Rocket engine"
python wikipedia_game.py "Saturn V" "Rocket propellant"
python wikipedia_game.py "Saturn V" "Deflagration to detonation transition"
```


```
python wikipedia_traverse.py "Web Bot"
```

