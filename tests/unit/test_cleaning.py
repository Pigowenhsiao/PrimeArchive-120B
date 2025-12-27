from src.services.cleaner import clean_text


def test_cleaning_removes_page_lines():
    text = "Page 1\nContent line\n2\n"
    cleaned = clean_text(text)
    assert "Page 1" not in cleaned
    assert "2" not in cleaned
    assert "Content line" in cleaned
