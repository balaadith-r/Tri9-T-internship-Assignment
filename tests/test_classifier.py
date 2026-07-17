from parser.classifier import HeadingClassifier
from parser.models import RawBlock


def test_classifies_heading():

    classifier = HeadingClassifier()

    blocks = [
        RawBlock(
            block_id=1,
            page=1,
            text="1 Device Overview",
            bbox=(0, 0, 100, 20),
            font_size=14,
            font_name="Arial-Bold",
            is_bold=True,
        )
    ]

    result = classifier.classify(blocks)

    assert len(result) == 1
    assert result[0].type == "heading"
    assert result[0].section_number == "1"
    assert result[0].heading == "Device Overview"
    assert result[0].level == 1


def test_classifies_paragraph():

    classifier = HeadingClassifier()

    blocks = [
        RawBlock(
            block_id=2,
            page=1,
            text="The CT200 is a compact controller.",
            bbox=(0, 0, 100, 20),
            font_size=11,
            font_name="Arial",
            is_bold=False,
        )
    ]

    result = classifier.classify(blocks)

    assert len(result) == 1
    assert result[0].type == "paragraph"


def test_nested_heading_level():

    classifier = HeadingClassifier()

    blocks = [
        RawBlock(
            block_id=3,
            page=1,
            text="2.3.1 Battery Life",
            bbox=(0, 0, 100, 20),
            font_size=14,
            font_name="Arial-Bold",
            is_bold=True,
        )
    ]

    result = classifier.classify(blocks)

    assert result[0].type == "heading"
    assert result[0].section_number == "2.3.1"
    assert result[0].level == 3