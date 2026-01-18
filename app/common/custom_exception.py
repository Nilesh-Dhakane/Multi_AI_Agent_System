import os
import sys
from typing import Optional

class CustomException(Exception):
    """
    Custom exception that enriches error information
    without performing logging.
    """

    def __init__(
        self,
        message: str,
        error: Optional[Exception] = None
    ):
        super().__init__(message)
        self.error = error
        self.detailed_message = self._build_detailed_message(message, error)

    @staticmethod
    def _build_detailed_message(
        message: str,
        error: Optional[Exception]
    ) -> str:

        if error and error.__traceback__:
            tb = error.__traceback__
            filename = os.path.basename(tb.tb_frame.f_code.co_filename)
            lineno = tb.tb_lineno
            original_error = str(error)
        else:
            filename = "UNKNOWN_FILE"
            lineno = "UNKNOWN_LINE"
            original_error = "UNKNOWN_ERROR"

        return (
            f"Message: {message} | "
            f"File: {filename} | "
            f"Line: {lineno} | "
            f"Original Error: {original_error}"
        )

    def __str__(self):
        return self.detailed_message
