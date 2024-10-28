
# AI-Powered Assistant with Code Execution

This project is an AI-powered assistant that can chat with users and execute Python code in a secure sandbox environment.

## Features

- User registration and authentication
- AI-powered chat using OpenAI's GPT-3.5 Turbo model
- Secure code execution in a Docker sandbox
- Rate limiting to prevent abuse
- Containerized application for easy deployment

## Prerequisites

- Docker
- Docker Compose
- Google Cloud SDK (for deployment)

## Setup

1. Clone the repository:
   ```
   git clone <repository-url>
   cd ai_powered_project
   ```

2. Create a `.env` file in the project root and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   DATABASE_URL=postgresql://username:password@host:port/database
   ```

3. Build and run the Docker containers:
   ```
   docker-compose up --build
   ```

4. The application will be available at `http://localhost:5000`

## Usage

1. Register a new user account
2. Log in with your credentials
3. Start chatting with the AI assistant
4. Use the code editor to write and execute Python code

## Security Notes

- The code execution is performed in a sandboxed Docker container with limited resources and network access.
- User passwords are hashed before being stored in the database.
- Rate limiting is implemented to prevent abuse of the AI chat and code execution features.

## Development

To run the application in development mode:

1. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

2. Set up the environment variables:
   ```
   export FLASK_APP=app.py
   export FLASK_ENV=development
   export OPENAI_API_KEY=your_openai_api_key_here
   export DATABASE_URL=postgresql://username:password@host:port/database
   ```

3. Run the Flask development server:
   ```
   flask run
   ```

## Testing

To run the unit tests:

```
python -m unittest test_app.py
```

## Deployment to Google Cloud Run

1. Install the Google Cloud SDK and initialize it:
   ```
   gcloud init
   ```

2. Set up a Google Cloud project and enable the necessary APIs (Cloud Run, Container Registry).

3. Build and push the Docker image to Google Container Registry:
   ```
   gcloud builds submit --tag gcr.io/[PROJECT-ID]/ai-powered-assistant
   ```

4. Deploy the application to Google Cloud Run:
   ```
   gcloud run deploy ai-powered-assistant --image gcr.io/[PROJECT-ID]/ai-powered-assistant --platform managed --region [REGION] --allow-unauthenticated --set-env-vars OPENAI_API_KEY=[YOUR_API_KEY],DATABASE_URL=[YOUR_DATABASE_URL]
   ```

5. Access your deployed application using the URL provided by Google Cloud Run.

## CI/CD

This project uses GitHub Actions for continuous integration and deployment. The workflow is defined in `.github/workflows/ci-cd.yml`. It includes the following steps:

1. Run tests
2. Build and push Docker image to GitHub Container Registry
3. Deploy to Google Cloud Run

To set up CI/CD:

1. Add the following secrets to your GitHub repository:
   - `GCP_SA_KEY`: Your Google Cloud service account key (JSON)
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `DATABASE_URL`: Your PostgreSQL database URL

2. Push your changes to the `main` branch to trigger the CI/CD pipeline.

## License

This project is licensed under the MIT License.
