"""
Unit tests for the utility functions in app/core/utils.py.
"""
import pytest
from datetime import datetime
from decimal import Decimal
import uuid
from enum import Enum
from app.core.utils import json_serializer

def test_json_serializer_with_sqlalchemy_model():
    """
    Ensures that an object that behaves like a SQLAlchemy model is serialized to its ID.
    """
    # Create a simple mock object that "ducks" as a SQLAlchemy model instance.
    # It just needs to have an `id` attribute.
    class MockModel:
        def __init__(self, id):
            self.id = id
            
    test_id = uuid.uuid4()
    mock_instance = MockModel(id=test_id)
    
    # We also need to check the `isinstance` check in the serializer.
    # To do that, we can temporarily patch what 'SQLAlchemyBaseModel' is.
    from app.core import utils
    # This is a bit of advanced testing, but it's the most correct way.
    # We are temporarily pretending our MockModel is an instance of SQLAlchemyBaseModel.
    original_base = utils.SQLAlchemyBaseModel
    utils.SQLAlchemyBaseModel = MockModel
    
    assert json_serializer(mock_instance) == str(test_id)

    # Clean up the patch
    utils.SQLAlchemyBaseModel = original_base

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

