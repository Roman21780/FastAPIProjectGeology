import os
import tempfile

import pandas as pd
from fastapi import HTTPException
from io import BytesIO, StringIO
from typing import List, Dict
import logging

from starlette.responses import FileResponse, StreamingResponse

from app.core.config import settings

logger = logging.getLogger(__name__)


def export_data(data: list[dict], entity_name: str, format: str = "csv"):
    """Export data to CSV or Excel format in memory without temp files"""
    try:
        df = pd.DataFrame(data)

        output = BytesIO()

        if format == "csv":
            content_type = "text/csv"
            df.to_csv(output, index=False)
            file_suffix = "csv"
        elif format == "xlsx":
            content_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False)
            file_suffix = "xlsx"
        else:
            raise ValueError(f"Unsupported format: {format}")

        output.seek(0)

        return StreamingResponse(
            output,
            media_type=content_type,
            headers={
                "Content-Disposition": f"attachment; filename={entity_name}_export.{file_suffix}"
            }
        )
    except Exception as e:
        logger.error(f"Export failed: {str(e)}", exc_info=True)
        raise


def import_data(file, model_type: str):
    try:
        if file.filename.endswith('.csv'):
            df = pd.read_csv(file.file)
        elif file.filename.endswith('.xlsx'):
            df = pd.read_excel(file.file)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format")

        # Валидация данных
        validate_import_data(df, model_type)

        # Преобразование в словари для вставки
        records = df.to_dict('records')
        return records
    except Exception as e:
        logger.error(f"Import failed: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Import failed: {str(e)}")


def validate_import_data(df: pd.DataFrame, model_type: str):
    # Реализация валидации в зависимости от типа модели
    required_columns = {
        "license": ["number", "issue_date", "expiration_date"],
        "field": ["name", "license_id"],
        "well": ["name", "depth", "status_id"]
    }

    if model_type not in required_columns:
        raise ValueError(f"Unknown model type: {model_type}")

    for col in required_columns[model_type]:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")