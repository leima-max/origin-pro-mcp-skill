import json

from origin_pro_mcp.origin_connection import get_origin
from origin_pro_mcp.tools.worksheet import import_csv_to_worksheet, list_worksheets

def setup_function():
    o = get_origin()
    o.Execute("doc -s; doc -n;")

def test_create_worksheet():
    o = get_origin()
    name = o.CreatePage(2, "TestWks", "origin")
    assert name == "TestWks"

def test_put_and_get_data():
    o = get_origin()
    o.CreatePage(2, "DataTest", "origin")
    o.PutWorksheet("[DataTest]Sheet1", [1.0, 2.0, 3.0], 0, 0)
    o.PutWorksheet("[DataTest]Sheet1", [4.0, 5.0, 6.0], 0, 1)
    data = o.GetWorksheet("[DataTest]Sheet1")
    assert data == ((1.0, 4.0), (2.0, 5.0), (3.0, 6.0))

def test_find_worksheet():
    o = get_origin()
    o.CreatePage(2, "ColTest", "origin")
    wks = o.FindWorksheet("[ColTest]Sheet1")
    assert wks is not None

def test_import_csv_respects_book_name(tmp_path):
    csv_path = tmp_path / "sample.csv"
    csv_path.write_text("Bias,Dark,Light\n0,0.02,0.11\n1,0.08,0.42\n", encoding="utf-8")

    result = import_csv_to_worksheet(str(csv_path), book_name="CsvBook", delimiter=",")
    assert result == "Imported to workbook: CsvBook"

    o = get_origin()
    assert o.GetWorksheet("[CsvBook]Sheet1") == ((0.0, 0.02, 0.11), (1.0, 0.08, 0.42))
    pages = json.loads(list_worksheets())
    assert {"book": "CsvBook", "type": "workbook"} in pages
    assert not [page for page in pages if page["type"] == "graph"]
