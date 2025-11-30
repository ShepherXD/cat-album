# Cat Album
A web application built with Vue.js and FastAPI to show cat images with LLM-based classification technique on cat breeds. 

## Demo


## Quick Start
### 1. Apply a Gemini API KEY from Google AI Studio (Free)
https://ai.google.dev/gemini-api/docs/api-key#api-keys
### 2. Setup an AWS-compatible Object Storage Service, E.g. Cloud Flare (Free) 
https://www.cloudflare.com/developer-platform/products/r2/
Ensure that you have already allow public domain access
### 3. Setup .env and Run Docker
```
# Add Environment (replace <PLACEHOLDER> to yours)
cat <<EOF > ./backend/.env
AWS_ENDPOINT="<Your Object Storage Endpoint e.g. https://xxxxxxx.r2.cloudflarestorage.com>"
AWS_ACCESS_KEY_ID="<Your Access Key>"
AWS_SECRET_ACCESS_KEY="<Your Secret Access Key>"
AWS_PUBLIC_DOMAIN="<Your Object Storage Domain>"
AWS_BUCKET_NAME="<Your Bucket Name>"
GEMINI_API_KEY="<Your Gemini API KEY>"
EOF

# Start Docker Service in Developerment Environment
docker compose --profile dev up --build

# Or Start Docker Service in Production Environment
docker compose --profile prod up --build
```

