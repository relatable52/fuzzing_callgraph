import javalang


def get_method_start_end(method_node, tree):
    startpos = None
    endpos = None
    startline = None
    endline = None
    for path, node in tree:
        if startpos is not None and method_node not in path:
            endpos = node.position
            endline = node.position.line if node.position is not None else None
            break
        if startpos is None and node == method_node:
            startpos = node.position
            startline = node.position.line if node.position is not None else None
    return startpos, endpos, startline, endline


def get_method_text(
    codelines, startpos, endpos, startline, endline, last_endline_index
):
    if startpos is None:
        return "", None, None, None
    else:
        startline_index = startline - 1
        endline_index = endline - 1 if endpos is not None else None

        # 1. check for and fetch annotations
        if last_endline_index is not None:
            for line in codelines[(last_endline_index + 1) : (startline_index)]:
                if "@" in line:
                    startline_index = startline_index - 1
        meth_text = "<ST>".join(codelines[startline_index:endline_index])
        meth_text = meth_text[: meth_text.rfind("}") + 1]

        # 2. remove trailing rbrace for last methods & any external content/comments
        # if endpos is None and
        if not abs(meth_text.count("}") - meth_text.count("{")) == 0:
            # imbalanced braces
            brace_diff = abs(meth_text.count("}") - meth_text.count("{"))

            for _ in range(brace_diff):
                meth_text = meth_text[: meth_text.rfind("}")]
                meth_text = meth_text[: meth_text.rfind("}") + 1]

        meth_lines = meth_text.split("<ST>")
        meth_text = "".join(meth_lines)
        last_endline_index = startline_index + (len(meth_lines) - 1)

        return (
            meth_text,
            (startline_index + 1),
            (last_endline_index + 1),
            last_endline_index,
        )


JAVA_TO_JVM_TYPE = {
    "byte": "B",
    "char": "C",
    "double": "D",
    "float": "F",
    "int": "I",
    "long": "J",
    "short": "S",
    "boolean": "Z",
    "void": "V",
}


def type_to_descriptor(type_node):
    """
    Converts a javalang type node to its JVM descriptor.
    """
    if type_node is None:
        return "V"  # void return type
    type_name = type_node.name
    descriptor = ""
    if type_name in JAVA_TO_JVM_TYPE:
        descriptor += JAVA_TO_JVM_TYPE[type_name]
    else:
        # Object type
        descriptor += type_name.replace(".", "/")
    return descriptor
