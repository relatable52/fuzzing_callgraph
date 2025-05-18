import javalang
import regex as re


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
    dimensions = len(type_node.dimensions) if hasattr(type_node, "dimensions") else 0
    descriptor = ""
    descriptor += "[" * dimensions
    if type_name in JAVA_TO_JVM_TYPE:
        descriptor += JAVA_TO_JVM_TYPE[type_name]
    else:
        # Object type
        descriptor += type_name.replace(".", "/") + ";"
    return descriptor


def get_method_signature(method_node, package_name, class_name):
    """
    Constructs the JVM-style method signature for methods and constructors.
    """
    if isinstance(method_node, javalang.tree.ConstructorDeclaration):
        method_name = "<init>"
        return_descriptor = "V"  # Constructors have no return type
    else:
        method_name = method_node.name
        return_descriptor = type_to_descriptor(method_node.return_type)

    param_descriptors = ""
    for param in method_node.parameters:
        param_descriptors += type_to_descriptor(param.type)

    descriptor = f"({param_descriptors}){return_descriptor}"
    class_path = f"{package_name}.{class_name}".replace(".", "/")
    return f"{class_path}.{method_name}:{descriptor}"


def shorten_jvm_descriptor(descriptor: str) -> str:
    method_path, method_desc = descriptor.split(":")
    params_raw, return_type = re.match(r"\((.*?)\)(.*)", method_desc).groups()

    # Match array or object types correctly
    token_pattern = re.compile(r"\[*L[^;]+;|\[*[BCDFIJSZ]")

    def shorten_type(t):
        if t.startswith("L"):  # Object type
            return t.split("/")[-1]
        elif t.startswith("[L"):  # Array of objects
            parts = t.split("/")
            class_name = parts[-1]
            dims = t.count("[")
            return "[" * dims + class_name
        else:  # Primitive or array of primitive
            return t

    param_tokens = token_pattern.findall(params_raw)
    simplified_params = [shorten_type(t) for t in param_tokens]

    # Ensure object types end with ';'
    def finalize(t):
        return t + ";" if t.startswith("L") and not t.endswith(";") else t

    finalized_params = [finalize(t) for t in simplified_params]

    new_params = "(" + "".join(finalized_params) + ")" + return_type
    return f"{method_path}:{new_params}"
