Secure Data API Application (FastAPI + PostgreSQL + Render) - 

A secure, API-key–protected data service built with FastAPI, PostgreSQL, and SQLAlchemy, and deployed on Render.
This project provides authenticated endpoints to create and fetch structured data for use in external applications.

Features - 
1. Fast, asynchronous API using FastAPI
2. API Key authentication for secure access
3. PostgreSQL + SQLAlchemy ORM for persistence
4. Cloud deployment using Render Web Service + Managed PostgreSQL
5. Easy seeding and local setup
6. Fully compatible with Postman, mobile apps, and external integrations

Tech Stack -
Python 3.10+
FastAPI
Uvicorn
SQLAlchemy
PostgreSQL (Render Managed DB)
psycopg2-binary

Project Structure -
.
├── main.py
├── models.py
├── database.py
├── seed_data.py
├── requirements.txt
└── README.md

Getting Started:
1. Clone the Repository
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>

2. Install Dependencies
pip install -r requirements.txt

3. Environment Variable
The application requires the following environment variable:
DATABASE_URL=<postgres_connection_string>
On Render, this is created automatically.

Running the Application Locally
Start the development server:
uvicorn main:app --reload


API Docs available at:

http://127.0.0.1:8000/docs

Seeding the Database

Render's free tier does not support jobs or shell execution, so seeding must be done locally.

Step 1 — Get Render Database URL

Render Dashboard → PostgreSQL → External Database URL

Step 2 — Set Environment Variable

Windows:

setx DATABASE_URL "postgres://..."


Mac/Linux:

export DATABASE_URL="postgres://..."

Step 3 — Run the Seed Script
python seed_data.py


This inserts sample records directly into the Render PostgreSQL instance.

Deploying to Render
1. Push Code to GitHub
git add .
git commit -m "Initial commit"
git push origin main

2. Create Render Services
A. Create PostgreSQL Database

Go to Render → New → PostgreSQL

Choose Free Tier

Copy the Internal and External connection URLs

B. Deploy the Web Service

Render → New → Web Service

Select your GitHub repo

Configure:

Setting	Value
Runtime	Python
Build Command	(leave blank)
Start Command	uvicorn main:app --host 0.0.0.0 --port $PORT
C. Add Environment Variable

Render → Web Service → Environment → Add:

DATABASE_URL=<internal postgres url>


Click Save → Deploy.

API Usage
API Base URL
https://your-render-service.onrender.com

API Key
014dk58dba90olkd4

1. Get All Items

GET /items

Headers:

X-API-Key: 014dk58dba90olkd4


Example (Postman):

GET https://your-render-service.onrender.com/items

2. Get Item by Key

GET /items/{item_key}

Example:

GET https://your-render-service.onrender.com/items/item1
X-API-Key: 014dk58dba90olkd4

3. Create Item

POST /items

Example:

POST https://your-render-service.onrender.com/items?key=item4&name=New+Item&description=test
X-API-Key: 014dk58dba90olkd4

Security Notes

Store API keys in environment variables in production

Rotate keys periodically

Never expose DB credentials in code or GitHub

HTTPS enforced automatically by Render

Troubleshooting
“No data returned”

Seed the database using seed_data.py with Render’s DB URL.

“Database connection refused”

Use the internal DB URL for Render Web Service.

“Module psycopg2 not found”

Ensure psycopg2-binary is included in requirements.txt.

"Server not starting on Render"

Verify Start Command:

uvicorn main:app --host 0.0.0.0 --port $PORT

Future Enhancements

JWT authentication

Rate limiting (per key)

Pagination & filtering

Admin dashboard

Custom API key management

License

MIT License.

Contributions

Pull requests are welcome.
For significant changes, please open an issue first to discuss what you would like to change.
