\# 🌿 TrailLens AI



\*\*A Gemma-powered outdoor exploration companion built with FastAPI and Python.\*\*



TrailLens AI is an AI-powered project designed to help people explore outdoor activities and plan nature-focused adventures. It uses Google's Gemma open-weight model to generate AI responses for outdoor exploration.



This project is being developed for the \*\*Hacktoberfest 2026 Open-Source AI Challenge — Week 1: Touch Grass\*\*.



\## ✨ Features



\* \*\*AI-powered exploration:\*\* Integrates Gemma to generate responses for outdoor-related queries.

\* \*\*FastAPI backend:\*\* Provides REST API endpoints for the application's features.

\* \*\*Observation management:\*\* Includes an observation-related API module.

\* \*\*Sprint missions:\*\* Includes APIs for sprint mission management.

\* \*\*Sprint sessions:\*\* Includes APIs for managing sprint sessions.

\* \*\*User management:\*\* Includes a user-related API module.

\* \*\*Interactive API documentation:\*\* Explore and test available endpoints through FastAPI Swagger UI.



\## 🛠️ Tech Stack



\* \*\*Language:\*\* Python

\* \*\*Backend framework:\*\* FastAPI

\* \*\*AI model:\*\* Google Gemma

\* \*\*Data validation:\*\* Pydantic schemas

\* \*\*API documentation:\*\* OpenAPI / Swagger UI



The database configuration and other dependencies are defined in the project source code and `requirements.txt`.



\## 📁 Project Structure



```text

TraiLens--AI/

├── main.py

├── database.py

├── dependency.py

├── models.py

├── schema.py

├── requirements.txt

├── routers/

│   ├── observations.py

│   ├── sprint\_mission.py

│   ├── sprint\_session.py

│   └── user.py

└── services/

&#x20;   ├── \_\_init\_\_.py

&#x20;   ├── gemma.py

&#x20;   ├── observations.py

&#x20;   ├── sprint\_mission.py

&#x20;   ├── sprint\_session.py

&#x20;   ├── test\_gemma.py

&#x20;   └── user.py

```



\## 🚀 Getting Started



\### Prerequisites



\* Python installed on your system

\* Git

\* Access to the Gemma model through the provider or runtime configured in the project



\### 1. Clone the repository



```bash

git clone https://github.com/MUBARAK-53/TraiLens--AI.git

```



\### 2. Navigate to the backend directory



```bash

cd TraiLens--AI

```



\### 3. Create a virtual environment



\*\*Windows PowerShell\*\*



```powershell

python -m venv venv

.\\venv\\Scripts\\Activate.ps1

```



\### 4. Install dependencies



```bash

python -m pip install --upgrade pip

pip install -r requirements.txt

```



\### 5. Configure environment variables



Configure the credentials and settings required by your Gemma integration and database configuration.



Keep private API keys, database passwords, and other secrets in a local `.env` file or environment variables as appropriate for your implementation. Never commit real credentials to GitHub.



\### 6. Start the FastAPI server



```bash

uvicorn main:app --reload

```



\### 7. Open the API documentation



Once the server starts, visit:



\* \*\*Swagger UI:\*\* http://127.0.0.1:8000/docs

\* \*\*ReDoc:\*\* http://127.0.0.1:8000/redoc



Use Swagger UI to inspect the endpoints registered by the application and test the available API operations.



\## 🤖 How Gemma Is Used



Gemma is the open-weight AI model integrated into TrailLens AI. The project's Gemma service is located at:



```text

services/gemma.py

```



This service forms the AI integration layer. It can be used by the application to process supported inputs and generate AI responses.



The exact model version, inference provider, and configuration depend on the implementation in the source code.



\## 🌍 Why Open-Source AI Matters



Open-weight AI models make it possible for developers to inspect model options, experiment with different deployment approaches, and adapt applications to their requirements.



For TrailLens AI, Gemma provides an opportunity to build an outdoor-focused AI companion without making a closed-model API the only possible architecture.



Depending on the chosen deployment, open-weight models can also provide greater control over model hosting, data handling, and experimentation.



\## 🧪 Testing



The repository includes a Gemma-related test module:



```text

services/test\_gemma.py

```



Review the test implementation and configure the required environment variables before running it.



\## 🔮 Future Improvements



Potential improvements include:



\* Personalized outdoor activity recommendations

\* Trail and nature exploration planning

\* Location-aware recommendations using appropriate data sources

\* Improved error handling and automated tests

\* Deployment and performance monitoring

\* A frontend for interacting with the AI assistant



These are planned possibilities, not claims that all features are already implemented.



\## 🏆 Hacktoberfest 2026



This project is being developed for the \*\*Hacktoberfest Open-Source AI Challenge — Week 1: Touch Grass\*\*, which encourages developers to build with open-source AI and help people spend more time outdoors.



Challenge: https://dev.to/challenges/hacktoberfest-week1-2026-10-05



\## 👨‍💻 Author



\*\*MUBARAK-53\*\*



GitHub: https://github.com/MUBARAK-53



\## 📄 License



A license has not yet been specified. A license should be selected and added to the repository before others redistribute or reuse the code.



