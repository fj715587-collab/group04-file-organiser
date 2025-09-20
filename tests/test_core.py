def test_smoke(tmp_path):
    p = tmp_path / "sample.txt"
    p.write_text("hello")
    assert p.exists()
