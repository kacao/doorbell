# a door bell
An mp3 player with a web api to act as a door bell
### Install:

* [Python3](https://www.python.org/) 
* [Pipenv](https://pypi.org/project/pipenv/)
* [VLC](https://www.videolan.org/vlc/)
* `git clone git@github.com:kacao/doorbell.git && cd doorbell`
* `pipenv install -r packages`

### Run

* `pipenv run python3 main.py --host '*' --port 8080 --dir './media'`

### Api

* Play a media file: `POST /api/media/bell.mp3/play`
* Stop playing: `POST /api/media/stop`
* Is playing?: `GET /api/media/is_playing` response body: `{"result": true/false, "item": playing media file}`

### Docker image
For raspberry pi, use `kacao/doorbell:rpi`
```yaml
version: '3'
services:
  doorbell:
    container_name: doorbell
    image: kacao/doorbell:latest
    ports:
      - 8080:8080
    volumes:
      - ~/bells:/media
      - /dev/snd:/dev/snd
      - /dev/shm:/dev/shm
      - /etc/machine-id:/etc/machine-id
      - /var/lib/dbus:/var/lib/dbus
    environment:
      - HOST=*
      - PORT=8080
    privileged: true
```
