# AgenticRAG

A production-ready agentic RAG (Retrieval-Augmented Generation) application built with LangGraph. This app empowers an AI agent to intelligently use multiple tools-such as vector databases, and APIs-to answer complex questions by dynamically retrieving and combining information from various sources. Easily extensible and robust, this application is designed for real-world deployment.

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/BennisonDevadoss/AgenticRAG.git
cd AgenticRAG
```

### 2. Set up Conda on Your Machine

If you don't have Conda installed, follow the instructions in the official guide to set it up:

- [Conda Installation Guide](https://www.anaconda.com/docs/getting-started/miniconda/install)

Once Conda is installed, follow the steps below to set up your environment:

1. **Create the Conda environment**
   After installing Conda, create the environment for your project with the following command:

   ```bash
   conda env create --name agentic-rag python=3.11
   ```

2. **Activate the Conda environment**
   Activate the environment to start using it:

   ```bash
   conda activate agentic-rag
   ```

3. **Install dependencies**
   After activating the environment, install the required dependencies with `pip`:

   ```bash
   pip install -r requirements.txt
   ```

4. **Deactivate the environment**
   When you're done working, you can deactivate the environment with:

   ```bash
   conda deactivate
   ```

### 3. Set up environment variables

Copy the example environment file to create environment-specific configuration files for each environment (`staging`, `production`, `development`):

```bash
cp .env.example .env.staging
cp .env.example .env.production
cp .env.example .env.development
```

Edit each `.env.{environment_name}` file to configure your environment variables as needed.

### 4. Set the environment variable

Depending on the environment you want to run (e.g., local development, staging, or production), you'll need to set the `ENVIRONMENT` variable accordingly:

- **For local development** (this is typically what you'd use for your own development setup):

  ```bash
  export ENVIRONMENT=development
  ```

- **For staging** (this would be used when testing the app in a staging environment before deploying to production):

  ```bash
  export ENVIRONMENT=staging
  ```

- **For production** (this would be used when deploying the app to production):

  ```bash
  export ENVIRONMENT=production
  ```

### 5. Apply database migrations

Once you've set the correct environment, apply any pending database migrations using Alembic:

```bash
alembic upgrade head
```

### 6. Seed the database

Navigate to the `app/seeders/` directory and run the `seed.py` script to populate the database with initial data:

```bash
cd app/seeders/
python seed.py
cd ../
```

### 7. Run the application

You can run the application in either of the following ways depending on your preference:

**Option 1: Using inline environment variable (recommended for one-off runs)**

```bash
ENVIRONMENT=development python main.py
```

Replace `development` with `staging` or `production` based on your target environment.

**Option 2: Exporting the environment variable (persistent for the shell session)**

```bash
export ENVIRONMENT=development
python main.py
```

### When to use each environment:

- **Development (`development`)**: Use this environment for local development. It may include local configurations, debugging tools, and any settings specifically meant for developers working on the project.

- **Staging (`staging`)**: This environment is used for testing the application in a staging environment, which mimics the production environment but allows for testing new features and updates before going live.

- **Production (`production`)**: This environment is used when deploying the app to production. It should contain production-level configurations such as live database URLs, API keys, etc.
