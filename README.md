# ASS 1

## Install

Make a virtual environment
```
virtualenv env
```

Open the environment:

```
source env/scripts/activate
```

Install dependencies:

```
pip install -r requirements.txt
```

## Set Up
Make sure you are in the `server/` directory, then run:

```
python dbmanager.py create_db
```

## Running

### Running the server

```
cd server 
python server.py
```

### Running the client

```
cd client/
python app.py
```



