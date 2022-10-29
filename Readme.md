

# Rest Snake


![alt text](https://cdn3.emoji.gg/emojis/7991-yippee.gif)


A Snake game in PyGame for streamers. It exposes the controller as a rest api so it can be
controlled from discord, twitch or other live stream chats.

It is also easier to train using machine learning algorithms

# Install   

```bash
git clone https://github.com/QuantumNovice/streamer-snake.git
```
* Edit `config.toml`
* Run `python game.py`


# Usage
* control using arrow keys
* control by sending get request to `<host>:port` combination defined in `config.toml`


# API Details
| Path | Function |
|--|--|
|`/up`| Sends pygame UP |
|`/down`|Sends pygame DOWN|
|`/left`|Sends pygame LEFT|
|`/right`|Sends pygame RIGHT|
|`/score`|Retrieves game score|


# Default Path
`http://127.0.0.1:5000/`

# Example
`http://127.0.0.1:5000/up`

# Curl Example
```bash
curl http://127.0.0.1:5000/left
```
