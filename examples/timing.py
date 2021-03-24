import timy

PATH = "/foo/bars"
LOOPS = 500_000
ROUTES = {("", "foo", None): True}


def if_else(path):
    parts = path.split("/")
    if parts[0] == "":
        if parts[1] == "foo":
            if len(parts) == 2:
                return ROUTES[(parts[0], parts[1], None)]
    return False


def and_parts(path):
    parts = path.split("/")
    if parts[0] == "" and parts[1] == "foo" and len(parts) == 2:
        return ROUTES[(parts[0], parts[1], None)]
    return False


def path_grab(path):
    parts = path.split("/")
    return ROUTES[(parts[0], parts[1], None)]


@timy.timer(loops=LOOPS)
def do_if_else():
    if_else(PATH)


@timy.timer(loops=LOOPS)
def do_and_parts():
    and_parts(PATH)


@timy.timer(loops=LOOPS)
def do_path_grab():
    path_grab(PATH)


do_if_else()
do_and_parts()
do_path_grab()
