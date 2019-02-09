# srtrail
Python library to edit SpeedRunners trails.

Use `pip` to install:

    $ pip install srtrail
    
Below is some sample code to get you started. This will open a trail, and make a copy of it.

```py
from srtrail import trail

srt = srtrail.Trail()
srt.load('trail.srt')
srt.save('copy.srt')
```

Once you have the trail, you will need to place it in the `{USER}/Documents/SavedGames/SpeedRunners/CEngineStorage/AllPlayers/Trails/Local/Import/` directory, where `{USER}` is the name of the account you are logged into on your PC. Then, simply start the game and you can use/edit/publish your trail.
