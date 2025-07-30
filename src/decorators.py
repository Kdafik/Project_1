from functools import wraps


def log(filename="../logs/default.log"):
    def decorator(function):
        @wraps(function)
        def wrapped(*args, **kwargs):
            log_str = function.__name__
            try:
                result = function(*args, **kwargs)
                log_str += " ok"
                if filename == "":
                    print(log_str)
                else:
                    with open(filename, "w") as log_file:
                        log_file.write(log_str)
                return result
            except Exception as e:
                log_str += f" error: {e}. Inputs: {args}, {kwargs}"
                if filename == "":
                    print(log_str)
                else:
                    with open(filename, "w") as log_file:
                        log_file.write(log_str)
                raise e
        return wrapped
    return decorator
