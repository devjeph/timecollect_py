import os
import logging
from config import settings
from services.google_sheets import GoogleSheetsService
from processing.pipeline import DataPipeline

def setup_logging():
    """
    Configures logging to file and console.
    """
    os.makedirs(settings.LOGS_DIR, exist_ok=True)

    if os.path.exists(settings.LOG_FILE_PATH):
        os.remove(settings.LOG_FILE_PATH)

    logging.basicConfig(
        level=settings.LOGGING_CONFIG["level"],
        format=settings.LOGGING_CONFIG["format"],
        handlers=[
            logging.FileHandler(settings.LOG_FILE_PATH),
            logging.StreamHandler()
        ]
    )

def main():
    """
    Initializes services and runs the data processing pipeline.
    """
    setup_logging()
    logging.info("🚀 Application starting...")

    # 1. Initialize Google Sheets Service
    sheets_service = GoogleSheetsService()

    # 2. Initialize Data Pipeline
    pipeline = DataPipeline(sheets_service)
    pipeline.run()

    logging.info("✅ Application finished successfully.")


if __name__ == "__main__":
    main()