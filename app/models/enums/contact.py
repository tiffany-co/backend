import enum

class ContactType(str, enum.Enum):
    """
    Enum for contact types. This ensures that the 'type' field
    can only contain predefined values.
    """
    CUSTOMER = "customer"
    SUPPLIER = "supplier"
    INVESTOR = "investor"
    COLLEAGUE = "colleague"
