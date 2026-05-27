from origin_pro_mcp.origin_connection import get_origin, execute_labtalk
import pytest

pytestmark = pytest.mark.origin

def setup_function():
    o = get_origin()
    o.Execute("doc -s; doc -n;")
    o.CreatePage(2, "StyleData", "origin")
    o.PutWorksheet("[StyleData]Sheet1", [1.0, 2.0, 3.0], 0, 0)
    o.PutWorksheet("[StyleData]Sheet1", [1.0, 4.0, 9.0], 0, 1)
    o.CreatePage(3, "StyleGraph", "origin")
    execute_labtalk('plotxy iy:=[StyleData]Sheet1!(1,2) plot:=202 ogl:=[StyleGraph]Layer1;')

def test_set_font():
    execute_labtalk('win -a StyleGraph;')
    success = execute_labtalk('xb.fsize = 14;')
    assert success

def test_set_line_width():
    execute_labtalk('win -a StyleGraph;')
    success = execute_labtalk('set %C -w 2000;')
    assert success
