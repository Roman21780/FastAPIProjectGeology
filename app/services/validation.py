from datetime import date
from pydantic import BaseModel, field_validator, model_validator, ValidationError
import re
from typing import Optional, Dict, Any, List
from app.core.logging import logger
import pandas as pd
from pandas import Series  # Правильный тип для строк DataFrame


class LicenseValidator(BaseModel):
    number: str
    issue_date: date
    expiration_date: date

    @field_validator('number')
    @classmethod
    def validate_license_number(cls, v: str) -> str:
        """Validate license number format (AA-YYYY-XXXX)"""
        if not re.match(r'^[A-Z]{2}-\d{4}-\d{4}$', v):
            logger.warning(f"Invalid license number format: {v}")
            raise ValueError('License number must be in format AA-YYYY-XXXX')
        return v

    @model_validator(mode='after')
    def validate_dates(self) -> 'LicenseValidator':
        """Check that expiration date is after issue date"""
        if self.expiration_date <= self.issue_date:
            logger.warning(
                f"Expiration date {self.expiration_date} must be after issue date {self.issue_date}"
            )
            raise ValueError('Expiration date must be after issue date')
        return self


class FieldValidator(BaseModel):
    name: str
    coordinates: Optional[str] = None

    @field_validator('coordinates')
    @classmethod
    def validate_coordinates(cls, v: Optional[str]) -> Optional[str]:
        """Validate coordinates format (lat,lon)"""
        if v is not None and not re.match(r'^-?\d+\.\d+,-?\d+\.\d+$', v):
            logger.warning(f"Invalid coordinates format: {v}")
            raise ValueError('Coordinates must be in format "lat,lon"')
        return v


class WellValidator(BaseModel):
    name: str
    depth: float
    status_id: int

    @field_validator('depth')
    @classmethod
    def validate_depth(cls, v: float) -> float:
        """Check that depth is positive"""
        if v <= 0:
            logger.warning(f"Invalid well depth: {v}")
            raise ValueError('Depth must be positive')
        return v


def validate_import_data(df: pd.DataFrame, model_type: str) -> None:
    """
    Validate imported data against Pydantic models

    Args:
        df: DataFrame with data to validate
        model_type: Type of model to validate against ('license', 'field', or 'well')

    Raises:
        ValueError: If validation fails with detailed error information
    """
    validators: Dict[str, Any] = {
        'license': LicenseValidator,
        'field': FieldValidator,
        'well': WellValidator
    }

    if model_type not in validators:
        raise ValueError(f"Unknown model type for validation: {model_type}")

    validator_class = validators[model_type]
    errors: List[Dict[str, Any]] = []

    for idx in range(len(df)):
        row: Series = df.iloc[idx]  # Правильный тип для строки DataFrame
        data: Dict[str, Any] = row.to_dict()
        try:
            validator_class.model_validate(data)
        except ValidationError as e:
            errors.append({
                'row': idx + 1,
                'error': str(e),
                'data': data.copy()
            })
            logger.error(f"Validation error in row {idx + 1}: {str(e)}")
        except Exception as e:
            errors.append({
                'row': idx + 1,
                'error': str(e),
                'data': data.copy()
            })
            logger.error(f"Unexpected error in row {idx + 1}: {str(e)}")

    if errors:
        error_info = {
            'message': 'Data validation failed',
            'errors': errors,
            'total_errors': len(errors)
        }
        logger.error(f"Validation failed: {error_info}")
        raise ValueError(error_info)