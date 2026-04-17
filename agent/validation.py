# agent/validation.py

def validate_tool_call(name, args, available_tools):
    tool = next(
        (t for t in available_tools if t["function"]["name"] == name),
        None,
    )

    if tool is None:
        return False, f"Tool '{name}' is not available.", None

    params = tool["function"]["parameters"]
    schema_props = params.get("properties", {})
    required = set(params.get("required", []))
    allowed = set(schema_props.keys())

    unexpected = set(args.keys()) - allowed
    if unexpected:
        return False, (
            f"Unexpected arguments for '{name}': {unexpected}"
        ), tool

    missing = required - set(args.keys())
    if missing:
        return False, (
            f"Missing required arguments for '{name}': {missing}"
        ), tool

    return True, None, tool
