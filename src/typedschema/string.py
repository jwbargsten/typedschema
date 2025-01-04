import re


def camel_to_snake(name):
    # https://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-snake-case
    name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()


def jinja_replace(s, config, relaxed=False, delim=("{{", "}}")):
    """Jinja for poor people. A very simple
    function to replace variables in text using `{{variable}}` syntax.

    :param s: the template string/text
    :param config: a dict of variable -> replacement mapping
    :param relaxed: Don't raise a KeyError if a variable is not in the config dict.
    :param delim: Change the delimiters to something else.
    """

    def handle_match(m):
        k = m.group(1)
        if k in config:
            return config[k]
        if relaxed:
            return m.group(0)
        raise KeyError(f"{k} is not in the supplied replacement variables")

    return re.sub(re.escape(delim[0]) + r"\s*(\w+)\s*" + re.escape(delim[1]), handle_match, s)
