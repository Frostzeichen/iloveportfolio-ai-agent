# AI Agent Server
This code is the Django version of the AI agent server which takes in text from a resume and returns an HTML file. Sample JSON and CSS can be found within the [resources](/resources) directory.

## Setup
The server requires a Claude API key to work. Enter this key in the `.env` file after running the following command:
```shell
cat .env.example > .env
```

Then to run the server, use the following commands:
```shell
pip install anthropic django python-dotenv
python manage.py runserver
```

## API Rules
### `POST /render`
Headers:
- `Content-Type`: `application/json`

Payload Body: string in JSON form

Returns: string in HTML form

Example:

```shell
curl -s -X POST http://127.0.0.1:8000/render/ -H "Content-Type: application/json" -d <insert JSON string payload here>
```
