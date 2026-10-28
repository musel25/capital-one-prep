## Reference solution

Paste this code above the supplied tests and runner.

```python
import csv
import io

GESTURES = ('rock', 'fire', 'scissors', 'snake', 'human', 'tree', 'wolf', 'sponge', 'paper', 'air', 'water', 'dragon', 'devil', 'lightning', 'gun')
SCORES = 'winner,loser\nrock,fire\nrock,scissors\nrock,snake\nrock,human\nrock,tree\nrock,wolf\nrock,sponge\nfire,scissors\nfire,snake\nfire,human\nfire,tree\nfire,wolf\nfire,sponge\nfire,paper\nscissors,snake\nscissors,human\nscissors,tree\nscissors,wolf\nscissors,sponge\nscissors,paper\nscissors,air\nsnake,human\nsnake,tree\nsnake,wolf\nsnake,sponge\nsnake,paper\nsnake,air\nsnake,water\nhuman,tree\nhuman,wolf\nhuman,sponge\nhuman,paper\nhuman,air\nhuman,water\nhuman,dragon\ntree,wolf\ntree,sponge\ntree,paper\ntree,air\ntree,water\ntree,dragon\ntree,devil\nwolf,sponge\nwolf,paper\nwolf,air\nwolf,water\nwolf,dragon\nwolf,devil\nwolf,lightning\nsponge,paper\nsponge,air\nsponge,water\nsponge,dragon\nsponge,devil\nsponge,lightning\nsponge,gun\npaper,air\npaper,water\npaper,dragon\npaper,devil\npaper,lightning\npaper,gun\npaper,rock\nair,water\nair,dragon\nair,devil\nair,lightning\nair,gun\nair,rock\nair,fire\nwater,dragon\nwater,devil\nwater,lightning\nwater,gun\nwater,rock\nwater,fire\nwater,scissors\ndragon,devil\ndragon,lightning\ndragon,gun\ndragon,rock\ndragon,fire\ndragon,scissors\ndragon,snake\ndevil,lightning\ndevil,gun\ndevil,rock\ndevil,fire\ndevil,scissors\ndevil,snake\ndevil,human\nlightning,gun\nlightning,rock\nlightning,fire\nlightning,scissors\nlightning,snake\nlightning,human\nlightning,tree\ngun,rock\ngun,fire\ngun,scissors\ngun,snake\ngun,human\ngun,tree\ngun,wolf\n'


def _create_defeat_mapping(csv_text=SCORES):
    mapping = {}
    for row in csv.DictReader(io.StringIO(csv_text)):
        mapping.setdefault(row['winner'], set()).add(row['loser'])
    return mapping


def get_winner(player1, player2):
    for player in (player1, player2):
        if not isinstance(player, str) or player not in GESTURES:
            raise ValueError('unknown gesture')
    if player1 == player2:
        return 'Tie'
    mapping = _create_defeat_mapping()
    if player2 in mapping[player1]:
        winner, loser = player1, player2
    else:
        winner, loser = player2, player1
    return f'{winner} defeats {loser}'
```
