# Receipt Processor

## Overview
A Python Flask-based web service for processing receipts and calculating reward points based on specific rules.

## Features
- Process receipts and generate unique IDs
- Calculate reward points according to specified criteria
- In-memory storage of receipts and points
- RESTful API endpoints


## Installation

### Docker Setup
1. Build the Docker image:
   ```
   docker build -t receipt-processor .
   ```

2. Run the Docker container:
   ```
   docker run -p 5000:5000 receipt-processor
   ```

## API Endpoints

### Process Receipt
- **URL:** `/receipts/process`
- **Method:** POST
- **Payload:** Receipt JSON
- **Response:** JSON with receipt ID

### Get Points
- **URL:** `/receipts/{id}/points`
- **Method:** GET
- **Response:** JSON with total points

## Point Calculation Rules
- 1 point per alphanumeric character in retailer name
- 50 points for round dollar total
- 25 points for total multiple of 0.25
- 5 points per two items
- Special points for item descriptions
- 6 points for odd purchase days
- 10 points for purchases between 2-4 PM

## Testing
You can run tests using the command:
```
docker exec <container_id> pytest -v /home/app/test_app.py
```
