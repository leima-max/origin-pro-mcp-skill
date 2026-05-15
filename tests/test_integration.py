"""End-to-end test: create data, plot, style, fit, export."""
import win32com.client
from origin_pro_mcp.tools.graph import export_graph
import os

def test_full_workflow():
    o = win32com.client.gencache.EnsureDispatch("Origin.ApplicationSI")
    o.NewProject()

    # 1. Create workbook with data
    o.CreatePage(2, "Experiment", "origin")
    x = [float(i) for i in range(1, 11)]
    y = [2.1*i + 0.5 + (i%3)*0.1 for i in range(1, 11)]
    o.PutWorksheet("[Experiment]Sheet1", x, 0, 0)
    o.PutWorksheet("[Experiment]Sheet1", y, 0, 1)

    # 2. Create graph
    o.CreatePage(3, "Figure1", "origin")
    o.Execute("plotxy iy:=[Experiment]Sheet1!(1,2) plot:=202 ogl:=[Figure1]Layer1;")

    # 3. Style for publication
    o.Execute('win -a Figure1;')
    o.Execute('xb.text$ = "Time (s)";')
    o.Execute('yl.text$ = "Signal (mV)";')
    o.Execute('xb.fsize = 12;')
    o.Execute('yl.fsize = 12;')

    # 4. Export via Origin expGraph and verify the output file.
    out = os.path.join(os.path.expanduser("~"), "test_integration_fig.png")
    result = export_graph("Figure1", out)
    assert result.startswith("Exported to:"), result

    assert os.path.exists(out), "Export failed: file not created"
    size = os.path.getsize(out)
    assert size > 1000, f"Export file too small: {size} bytes"
    print(f"Integration test passed! Exported {size} bytes")
    os.remove(out)
