"""
Unit tests for the utility functions in app/core/utils.py.
"""
import pytest
from datetime import datetime
from decimal import Decimal
import uuid
from enum import Enum

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID
from app.core.utils import json_serializer
from app.models.base import BaseModel as SQLAlchemyBaseModel

def test_json_serializer_with_sqlalchemy_model():
    """
    Ensures that an object inheriting from SQLAlchemyBaseModel is serialized to its ID.
    """
    # Create a simple mock class that simulates a SQLAlchemy model instance
    class MockModel(SQLAlchemyBaseModel):
        __tablename__ = 'mock_table' # Required for SQLAlchemy models
        id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
        
    test_id = uuid.uuid4()
    mock_instance = MockModel(id=test_id)
    
    assert json_serializer(mock_instance) == str(test_id)

def test_json_serializer_with_datetime():
    """
    Ensures that datetime objects are correctly serialized to their ISO 8601 string representation.
    """
    now = datetime.now()
    assert json_serializer(now) == now.isoformat()

def test_json_serializer_with_uuid():
    """
    Ensures that UUID objects are correctly serialized to their string representation.
    """
    test_uuid = uuid.uuid4()
    assert json_serializer(test_uuid) == str(test_uuid)

def test_json_serializer_with_decimal():
    """
    Ensures that Decimal objects are correctly serialized to their string representation.
    """
    test_decimal = Decimal("123.45")
    assert json_serializer(test_decimal) == "123.45"

def test_json_serializer_with_enum():
    """
    Ensures that Enum members are correctly serialized to their value.
    """
    class TestEnum(Enum):
        MEMBER_A = "value_a"

    assert json_serializer(TestEnum.MEMBER_A) == "value_a"

def test_json_serializer_with_unsupported_type():
    """
    Ensures that a TypeError is raised when an unserializable object is passed.
    This confirms the function's error handling for unexpected types.
    """
    class UnsupportedType:
        pass

    with pytest.raises(TypeError):
        json_serializer(UnsupportedType())

