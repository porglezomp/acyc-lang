def unimplemented(message=None):
    if message is None:
        raise Exception("Unimplemented")
    else:
        raise Exception("Unimplemented: " + message)


class ExpectError (Exception):
    def __init__(self, expected, got):
        message = "{}:{} expected `{}` got `{}`".format(
            got.line,
            got.col,
            expected,
            got
        )
        super(ExpectError, self).__init__(message)


def expect(got, expect):
    if type(expect) is str:
        if expect != got:
            raise ExpectError(expect, got)
    else:
        if not isinstance(got, expect):
            raise ExpectError(expect, got)
