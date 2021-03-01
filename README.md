# IoT-Motion-Device-Manager

## Setup

Clone this repository.


```
pip3 install -r requirements.txt
```

Change `.env.example` file to `.env`:


Then you can run the following to run the Flask server:

```
python3 wsgi.py
```

## Testing

```
python -m unittest IoT_Manager.tests.tests_management
python -m unittest IoT_Manager.tests.tests_auth

```
