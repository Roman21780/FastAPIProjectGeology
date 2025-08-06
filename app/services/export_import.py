import pandas as pd
from fastapi import HTTPException
from io import BytesIO, StringIO
from typing import List, Dict
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)


def export_data(data: List[Dict], entity_name: str, format: str = "csv"):

    try:
        df = pd.DataFrame(data)
        if len(data) > settings.MAX_EXPORT_ROWS:
            raise ValueError(f"Превышено максимальное количество строк для экспорта: {settings.MAX_EXPORT_ROWS}")

        if format not in settings.EXPORT_FORMATS:
            raise ValueError(f"Неподдерживаемый формат экспорта. Доступные: {settings.EXPORT_FORMATS}")

        if format == "csv":
            output = StringIO()
            df.to_csv(output, index=False)
            content = output.getvalue()
            media_type = "text/csv"
            filename = f"{entity_name}.csv"
        elif format == "xlsx":
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False)
            content = output.getvalue()
            media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            filename = f"{entity_name}.xlsx"
        else:
            raise ValueError("Unsupported export format")

        return {
            "content": content,
            "media_type": media_type,
            "filename": filename
        }
    except Exception as e:
        logger.error(f"Export failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Export failed: {str(e)}")


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