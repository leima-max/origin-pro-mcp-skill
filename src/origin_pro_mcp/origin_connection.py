import win32com.client

_origin = None

def get_origin():
    global _origin
    if _origin is None:
        _origin = win32com.client.Dispatch("Origin.ApplicationSI")
    return _origin

def execute_labtalk(script: str) -> bool:
    o = get_origin()
    return o.Execute(script)

def get_lt_var(name: str) -> float:
    return get_origin().LTVar(name)

def get_lt_str(name: str) -> str:
    return get_origin().LTStr(name)
