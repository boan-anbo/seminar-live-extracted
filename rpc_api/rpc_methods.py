from modernrpc.core import rpc_method


@rpc_method
def add(a, b):
    """
    This method adds two numbers together
    :param a: test
    :param b:
    :return:
    """
    # This is my method
    print("test")
    return {"Result": a + b }
