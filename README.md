# PII Detection API

A Flask-based API service that uses transformer models to detect Personal Identifiable Information (PII) in text. This tool can identify various categories of PII such as social security numbers, email addresses, phone numbers, and more.

## Features

- Detects 29 different types of PII including:
  - Social Security Numbers
  - Email addresses
  - Phone numbers
  - Credit card numbers
  - Dates of birth
  - Names
  - Addresses
  - And more

- REST API interface for easy integration
- JSON response format with both raw output and structured data
- Cloud-ready with Docker support for deployment

## Installation

### Prerequisites

- Python 3.8+
- pip
- Optional: Docker (for containerized deployment)

### Local Setup

1. Clone the repository
```bash
git clone https://github.com/yourusername/pii-detection-api.git
cd pii-detection-api
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Run the application
```bash
python main.py
```

## Usage

### API Endpoints

#### POST /detect_pii

Detects PII in provided text.

**Request:**
```bash
curl -X POST http://localhost:8080/detect_pii \
  -H "Content-Type: application/json" \
  -d '{"text": "My SSN is 123-45-6789 and I was born on 01/15/1980. Contact me at john.doe@example.com"}'
```

**Response:**
```json
{
  "raw_output": "<social_security_number> : ['123-45-6789']\n<date_of_birth> : ['01/15/1980']\n<email> : ['john.doe@example.com']",
  "structured_pii": {
    "social_security_number": ["123-45-6789"],
    "date_of_birth": ["01/15/1980"],
    "email": ["john.doe@example.com"]
  }
}
```



#### GET /

Health check endpoint that confirms the API is running.

**Request:**
```bash
curl http://localhost:8080/
```

**Response:**
```json
{
  "service": "PII Detection API",
  "status": "active",
  "usage": "Send a POST request to /detect_pii with JSON data containing a \"text\" field"
}
```

## Deployment to Google Cloud Run

### Build and Deploy with gcloud CLI

1. Set your Google Cloud project ID and service name
```bash
PROJECT_ID=your-project-id
SERVICE_NAME=pii-detection-api
```

2. Build the container
```bash
gcloud builds submit --tag gcr.io/$PROJECT_ID/$SERVICE_NAME
```

3. Deploy to Cloud Run
```bash
gcloud run deploy $SERVICE_NAME \
  --image gcr.io/$PROJECT_ID/$SERVICE_NAME \
  --platform managed \
  --region us-central1 \
  --memory 2Gi \
  --cpu 1 \
  --timeout 300 \
  --allow-unauthenticated
```

### Alternative: Manual Deployment via Google Cloud Console

1. Enable the Cloud Run and Container Registry APIs in your Google Cloud project
2. Navigate to Cloud Run in the Google Cloud Console
3. Click "Create Service"
4. Choose "Continuously deploy from a repository" or "Deploy a revision from an existing container image"
5. Follow the prompts to build and deploy your container
6. Set the memory limit (recommend at least 2GB for this model)
7. Set CPU allocation (recommend at least 1 CPU)
8. Configure other settings as needed
9. Click "Create"

## Important Considerations

- The first request may be slow due to model loading (cold start)
- The ML model requires significant memory (2GB+)
- Consider authentication for production use
- Be aware of Cloud Run pricing if deploying to Google Cloud Run

## PII Categories Detected

The system can detect the following PII categories:
- `<pin>`
- `<api_key>`
- `<bank_routing_number>`
- `<bban>`
- `<company>`
- `<credit_card_number>`
- `<credit_card_security_code>`
- `<customer_id>`
- `<date>`
- `<date_of_birth>`
- `<date_time>`
- `<driver_license_number>`
- `<email>`
- `<employee_id>`
- `<first_name>`
- `<iban>`
- `<ipv4>`
- `<ipv6>`
- `<last_name>`
- `<local_latlng>`
- `<name>`
- `<passport_number>`
- `<password>`
- `<phone_number>`
- `<social_security_number>`
- `<street_address>`
- `<swift_bic_code>`
- `<time>`
- `<user_name>`

## License

[MIT License](LICENSE)

## Acknowledgements

This project uses the [betterdataai/PII_DETECTION_MODEL](https://huggingface.co/betterdataai/PII_DETECTION_MODEL) from Hugging Face.
