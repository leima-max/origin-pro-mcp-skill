from origin_pro_mcp.origin_connection import get_origin, execute_labtalk
import pytest

pytestmark = pytest.mark.origin

def setup_function():
    o = get_origin()
    o.Execute("doc -s; doc -n;")

def test_create_graph_page():
    o = get_origin()
    name = o.CreatePage(3, "TestGraph", "origin")
    assert name == "TestGraph"

def test_plot_data():
    o = get_origin()
    o.CreatePage(2, "PlotData", "origin")
    o.PutWorksheet("[PlotData]Sheet1", [1.0, 2.0, 3.0, 4.0], 0, 0)
    o.PutWorksheet("[PlotData]Sheet1", [1.0, 4.0, 9.0, 16.0], 0, 1)
    o.CreatePage(3, "PlotGraph", "origin")
    success = execute_labtalk('plotxy iy:=[PlotData]Sheet1!(1,2) plot:=202 ogl:=[PlotGraph]Layer1;')
    assert success
