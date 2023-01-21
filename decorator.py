def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return 'This contact doesnt exist, please try again.'

        except ValueError as exception:
            return exception.args[0]
        except IndexError:
            return 'This contact cannot be added, it already exists.'
        except TypeError:
            return 'Unknown command or parametrs, please try again.'
    return inner

