"""Exception classes for VeriFactu."""


class PostException(Exception):
    """Exception during blockchain posting."""
    pass


class ClearPostException(Exception):
    """Exception during clearing post."""
    pass


class SendException(Exception):
    """Exception during sending."""
    pass


class UnexpectedHtmlException(Exception):
    """Exception for unexpected HTML content."""
    pass


class FaultException(Exception):
    """Exception for SOAP faults."""
    pass


class WriterException(Exception):
    """Exception during QR code writing."""
    pass