from origin_pro_mcp.origin_connection import execute_labtalk, get_lt_var, get_lt_str

def test_execute_labtalk_simple():
    execute_labtalk("double __mcp_test = 42;")
    assert get_lt_var("__mcp_test") == 42.0

def test_execute_labtalk_string():
    execute_labtalk('string __mcp_str$ = "hello";')
    assert get_lt_str("__mcp_str$") == "hello"
