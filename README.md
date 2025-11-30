# AI-Powered Electrical Construction Calculator

## Overview
This project is an AI-driven electrical construction calculator designed to transform engineering workflows from manual calculations to automated, intelligent processes. It integrates real-time material pricing, NEC compliance checks, and automated quantity takeoffs.

## Key Features
- **Real-Time Material Engine**: Live pricing from 5,000+ suppliers, inventory availability, and regional cost adjustments.
- **AI-Powered Calculation Core**: Automated quantity takeoff from drawings, pattern recognition for cost trends, and dynamic recalculation.
- **Critical Data Sources**: Integration with NEC/NFPA database, IEEE standards, and utility standards.
- **AI Features**: Load flow analysis, material cost estimating, risk assessment, and labor hour prediction.

## Technology Stack
- **Backend**: Python (Flask), SQLAlchemy
- **Database**: SQLite (Development), PostgreSQL (Production)
- **AI Engine**: Custom algorithms for electrical calculations and cost estimation

## Setup and Installation

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Initialize Database**:
    ```bash
    python init_database.py
    ```

3.  **Run the Application**:
    ```bash
    python app.py
    ```

## Project Structure
- `app.py`: Main Flask application entry point.
- `ai_engine.py`: Core AI logic for cost estimation and risk analysis.
- `supplier_integration.py`: Integration with external supplier APIs.
- `enhanced_models.py`: Database models for the enhanced application.
- `config.py`: Application configuration.

## Usage
Access the dashboard at `http://localhost:5000` to view project metrics, manage projects, and perform calculations.