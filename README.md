# a door bell
An mp3 player with a web api to act as a door bell
### Install:

* [Python3](https://www.python.org/) 
* [Pipenv](https://pypi.org/project/pipenv/)
* [VLC](https://www.videolan.org/vlc/)
* `git clone git@github.com:kacao/doorbell.git && cd doorbell`
* `pipenv install -r packages`

### Run

* `pipenv run python3 main.py --port 8080 --dir './media'`

### Api

* Play a media file: `POST /api` body: `{"action": "play", "file": "doorbell-1.mp3"}`
* Stop playing: `POST /api` body: `{"action": "stop"}`
* Is playing?: `GET /api` param: `action=is_playing`

