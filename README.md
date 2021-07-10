# Kronikarz.Api [![GitHub license](https://img.shields.io/github/license/KronikarzIO/Kronikarz.Api)](https://github.com/KronikarzIO/Kronikarz.Api/blob/master/LICENSE)


[Kronikarz.Api](https://github.com/Blazevarjo/Pokedex.Api) is a REST Api that was built to serve data for [Kronikarz.Frontend](https://github.com/KronikarzIO/Frontend). This app consists of endpoints to determine family tree with detailed information about family tree. User can add data about mariages, timeline events and files to person who belongs to family tree. There is also built-in authentication to allow users to get only permitted family trees informations.

# Table of contents
- [Technologies](#technologies)
- [Installation](#installation)
- [Usage](#usage)
- [Status](#status)
- [License](#license)

# Technologies

- Python
- Django REST framework 
- PostgreSQL

[Here](requirements.txt) you can check all dependencies.

## Installation
### Prerequisites

Docker is required to run the app locally.

### Setup

1. Build and run the docker container.
```bash
docker-compose up
```
App is now available at http://127.0.0.1:8000/.
Documentation is available at: 
- redoc : http://127.0.0.1:8000/redoc/
- swagger : http://127.0.0.1:8000/swagger/

## Usage

1. Authentication endpoints used to register, login, logout, check current authentication status and get csrf protection token. <br/>
<img src="https://user-images.githubusercontent.com/46849151/125165080-ae904800-e195-11eb-85c7-864191e516c7.png" width=400/> <br/>
2. Events endpoint(CRUD) for getting information about important events in the timeline of the person. <br/>
<img src="https://user-images.githubusercontent.com/46849151/125165112-d8496f00-e195-11eb-8816-a82dd003934c.png" width=400/> <br/>
3. Family trees endpoint(CRUD) for getting information about family tree name, people who belongs to it and relations between them. <br/>
<img src="https://user-images.githubusercontent.com/46849151/125165121-e13a4080-e195-11eb-996c-d65d07cca393.png" width=400/> <br/>
4. Mariages endpoint(CRUD) for getting information about mariages between people. <br/>
<img src="https://user-images.githubusercontent.com/46849151/125165127-eac3a880-e195-11eb-8474-582d89e18b39.png" width=400/> <br/>
5. Medias endpoint(CRUD) for getting files stored by user and profile picture. <br/>
<img src="https://user-images.githubusercontent.com/46849151/125165138-f44d1080-e195-11eb-9f0c-34ab8c83930e.png" width=400/> <br/>
6. Persons endpoint(CRUD) for getting detailed data about person. <br/>
<img src="https://user-images.githubusercontent.com/46849151/125165145-fdd67880-e195-11eb-91bc-a17666f18fec.png" width=400/> <br/>

## Status

Currently, the app is considered as finished and there are no plans to do any updates on it.

## License

[MIT](LICENSE)

