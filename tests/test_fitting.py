from origin_pro_mcp.origin_connection import get_origin, execute_labtalk, get_lt_var

def setup_function():
    o = get_origin()
    o.Execute("doc -s; doc -n;")

def test_linear_fit():
    o = get_origin()
    o.CreatePage(2, "FitData", "origin")
    o.PutWorksheet("[FitData]Sheet1", [1.0, 2.0, 3.0, 4.0, 5.0], 0, 0)
    o.PutWorksheet("[FitData]Sheet1", [2.1, 3.9, 6.1, 7.9, 10.1], 0, 1)

    # Set column designations: col(1)=X, col(2)=Y
    o.Execute("win -a FitData;")
    o.Execute("[FitData]Sheet1!col(1).type = 4;")
    o.Execute("[FitData]Sheet1!col(2).type = 1;")

    # Use fitlr for linear regression; fitlr.r is the correlation coefficient
    o.Execute("fitlr col(2);")
    r = get_lt_var("fitlr.r")
    r2 = r * r
    assert r2 > 0.99
