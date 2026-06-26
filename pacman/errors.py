from pathlib import Path
import inspect
import traceback


def format_error(message: object, file: str, line: int) -> str:
    return f"Error ({file}, line {line}): {message}"


def format_current_error(message: object) -> str:
    frame = inspect.currentframe()
    caller = frame.f_back if frame is not None else None

    if caller is None:
        return f"Error (unknown, line 0): {message}"

    file = Path(caller.f_code.co_filename).as_posix()
    return format_error(message, file, caller.f_lineno)


def format_exception_error(error: BaseException) -> str:
    trace = traceback.extract_tb(error.__traceback__)

    if not trace:
        return f"Error (unknown, line 0): {error}"

    last_frame = trace[-1]
    file = Path(last_frame.filename).as_posix()
    return format_error(error, file, last_frame.lineno)
