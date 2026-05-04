# LaTeX Compiler API

A FastAPI-based API that compiles LaTeX code to PDF. If compilation fails, it returns the error message.

## Features

- Compile LaTeX (.tex) files to PDF
- Error handling with detailed error messages
- Dockerized for easy deployment
- Uses TeX Live Full for complete LaTeX support

## API Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

You can test the API endpoints directly from the Swagger UI.

## Running Locally

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Make sure TeX Live is installed on your system.

3. Run the server:
   ```bash
   uvicorn app:app --reload
   ```

4. Open http://localhost:8000/docs for API documentation (Swagger UI) or http://localhost:8000/redoc for ReDoc.

## Docker

Build and run with Docker:

```bash
# Build the image (this will take some time due to texlive-full size ~5GB)
docker build -t latex-compiler .

# Run the container
docker run -p 8000:8000 latex-compiler
```

## Hosting

The application is containerized, so you can deploy it to any container hosting service like:
- AWS ECS/Fargate
- Google Cloud Run
- Azure Container Instances
- DigitalOcean App Platform
- Heroku (with heroku.yml)

## Example Usage

Using curl:

```bash
curl -X POST "http://localhost:8000/compile" \
     -H "accept: application/pdf" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@example.tex" \
     --output compiled.pdf
```

## Error Handling

If LaTeX compilation fails, the API returns a 400 status with the error message from pdflatex.