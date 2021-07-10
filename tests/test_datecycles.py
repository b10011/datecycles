from datecycles import datecycles
import arrow
import datetime
import holidays as pyholidays


def take_max(iterator, count, verbose=False):
    res = []

    try:
        for _ in range(count):
            val = next(iterator)
            if verbose:
                print("ITERATOR VALUE:", val)
            res.append(val)
    except StopIteration:
        pass

    return res


def test_count():
    """
    Count shouldn't be affected by Nth day of month
    """

    assert len(list(datecycles(1, "month", day=1, count=12))) == 12
    assert len(list(datecycles(1, "month", day=31, count=12))) == 12

    start = arrow.get(2021, 7, 10)
    assert (
        len(list(datecycles(1, "month", day=1, start=start, count=12))) == 12
    )
    assert (
        len(list(datecycles(1, "month", day=31, start=start, count=12)))
        == 12
    )

    start = arrow.get(2021, 7, 1)
    assert (
        len(list(datecycles(1, "month", day=1, start=start, count=12))) == 12
    )
    assert (
        len(list(datecycles(1, "month", day=31, start=start, count=12)))
        == 12
    )

    start = arrow.get(2021, 7, 31)
    assert (
        len(list(datecycles(1, "month", day=1, start=start, count=12))) == 12
    )
    assert (
        len(list(datecycles(1, "month", day=31, start=start, count=12)))
        == 12
    )


def test_start_end_length():
    """
    datecycles should only return ranges between start and end
    """

    start = arrow.get(2021, 7, 10)
    end = arrow.get(2022, 7, 1)
    assert (
        len(list(datecycles(1, "month", day=1, start=start, end=end))) == 12
    )

    start = arrow.get(2021, 7, 1)
    end = arrow.get(2022, 7, 1)
    assert (
        len(list(datecycles(1, "month", day=1, start=start, end=end))) == 13
    )


def test_start_end_count_length():
    """
    Count should be overridden by end if end comes first
    """

    start = arrow.get(2021, 7, 31)
    end = arrow.get(2021, 9, 30)
    assert (
        len(
            list(
                datecycles(1, "month", day=1, start=start, end=end, count=12)
            )
        )
        == 2
    )
    assert (
        len(
            list(
                datecycles(
                    1, "month", day=31, start=start, end=end, count=12
                )
            )
        )
        == 3
    )


def test_units():
    """
    Nth of x should work for any x
    """

    start = arrow.get(2021, 7, 10)
    res = take_max(datecycles(10, "day", start=start, count=7), 100)
    assert res == [
        arrow.get(2021, 7, 10),
        arrow.get(2021, 7, 20),
        arrow.get(2021, 7, 30),
        arrow.get(2021, 8, 9),
        arrow.get(2021, 8, 19),
        arrow.get(2021, 8, 29),
        arrow.get(2021, 9, 8),
    ]

    start = arrow.get(2021, 7, 10)
    res = take_max(datecycles(2, "week", start=start, count=4), 100)
    assert res == [
        arrow.get(2021, 7, 10),
        arrow.get(2021, 7, 24),
        arrow.get(2021, 8, 7),
        arrow.get(2021, 8, 21),
    ]

    start = arrow.get(2021, 7, 10)
    res = take_max(datecycles(2, "month", day=1, start=start, count=3), 100)
    assert res == [
        arrow.get(2021, 8, 1),
        arrow.get(2021, 10, 1),
        arrow.get(2021, 12, 1),
    ]

    start = arrow.get(2021, 6, 30)
    res = take_max(datecycles(2, "month", day=30, start=start, count=6), 100)
    assert res == [
        arrow.get(2021, 6, 30),
        arrow.get(2021, 8, 30),
        arrow.get(2021, 10, 30),
        arrow.get(2021, 12, 30),
        arrow.get(2022, 2, 28),
        arrow.get(2022, 4, 30),
    ]

    start = arrow.get(2021, 6, 30)
    res = take_max(datecycles(2, "month", day=31, start=start, count=6), 100)
    assert res == [
        arrow.get(2021, 6, 30),
        arrow.get(2021, 8, 31),
        arrow.get(2021, 10, 31),
        arrow.get(2021, 12, 31),
        arrow.get(2022, 2, 28),
        arrow.get(2022, 4, 30),
    ]

    start = arrow.get(2021, 7, 10)
    res = take_max(datecycles(2, "year", day=1, start=start, count=3), 100)
    assert res == [
        arrow.get(2021, 8, 1),
        arrow.get(2023, 8, 1),
        arrow.get(2025, 8, 1),
    ]

    start = arrow.get(2021, 6, 30)
    res = take_max(datecycles(10, "year", day=31, start=start, count=6), 100)
    assert res == [
        arrow.get(2021, 6, 30),
        arrow.get(2031, 6, 30),
        arrow.get(2041, 6, 30),
        arrow.get(2051, 6, 30),
        arrow.get(2061, 6, 30),
        arrow.get(2071, 6, 30),
    ]


def test_skip_weekends():
    start = arrow.get(2021, 7, 1)
    res = take_max(
        datecycles(
            1, "month", day=10, start=start, count=10, shift_to_workday="next"
        ),
        100,
    )
    assert res == [
        arrow.get(2021, 7, 12),
        arrow.get(2021, 8, 10),
        arrow.get(2021, 9, 10),
        arrow.get(2021, 10, 11),
        arrow.get(2021, 11, 10),
        arrow.get(2021, 12, 10),
        arrow.get(2022, 1, 10),
        arrow.get(2022, 2, 10),
        arrow.get(2022, 3, 10),
        arrow.get(2022, 4, 11),
    ]

    start = arrow.get(2021, 7, 1)
    res = take_max(
        datecycles(
            2,
            "month",
            day=12,
            start=start,
            count=7,
            shift_to_workday="previous",
        ),
        100,
    )
    assert res == [
        arrow.get(2021, 7, 12),
        arrow.get(2021, 9, 10),
        arrow.get(2021, 11, 12),
        arrow.get(2022, 1, 12),
        arrow.get(2022, 3, 11),
        arrow.get(2022, 5, 12),
        arrow.get(2022, 7, 12),
    ]


def test_skip_weekends_and_holidays():
    # Test using python's holidays library
    start = arrow.get(2021, 7, 1)
    res = take_max(
        datecycles(
            1,
            "month",
            day=24,
            start=start,
            count=7,
            shift_to_workday="next",
            country="FI",
        ),
        100,
    )
    assert res == [
        arrow.get(2021, 7, 26),
        arrow.get(2021, 8, 24),
        arrow.get(2021, 9, 24),
        arrow.get(2021, 10, 25),
        arrow.get(2021, 11, 24),
        arrow.get(2021, 12, 27),
        arrow.get(2022, 1, 24),
    ]

    # Test using python's holidays library
    start = arrow.get(2021, 7, 1)
    res = take_max(
        datecycles(
            1,
            "month",
            day=24,
            start=start,
            count=7,
            shift_to_workday="previous",
            country="FI",
        ),
        100,
    )
    assert res == [
        arrow.get(2021, 7, 23),
        arrow.get(2021, 8, 24),
        arrow.get(2021, 9, 24),
        arrow.get(2021, 10, 22),
        arrow.get(2021, 11, 24),
        arrow.get(2021, 12, 23),
        arrow.get(2022, 1, 24),
    ]

    # Test with custom holidays (dict)
    start = arrow.get(2021, 7, 1)
    res = take_max(
        datecycles(
            1,
            "month",
            day=24,
            start=start,
            count=7,
            shift_to_workday="next",
            holidays={
                datetime.date(2021, 8, 24): None,
                datetime.date(2021, 9, 24): "anything",
                datetime.date(2021, 10, 24): -123,
            },
        ),
        100,
    )
    assert res == [
        arrow.get(2021, 7, 26),
        arrow.get(2021, 8, 25),
        arrow.get(2021, 9, 27),
        arrow.get(2021, 10, 25),
        arrow.get(2021, 11, 24),
        arrow.get(2021, 12, 24),
        arrow.get(2022, 1, 24),
    ]

    # Test with custom holidays (list)
    start = arrow.get(2021, 7, 1)
    res = take_max(
        datecycles(
            1,
            "month",
            day=24,
            start=start,
            count=7,
            shift_to_workday="next",
            holidays=[
                datetime.date(2021, 8, 24),
                datetime.date(2021, 9, 24),
                datetime.date(2021, 10, 24),
            ],
        ),
        100,
    )
    assert res == [
        arrow.get(2021, 7, 26),
        arrow.get(2021, 8, 25),
        arrow.get(2021, 9, 27),
        arrow.get(2021, 10, 25),
        arrow.get(2021, 11, 24),
        arrow.get(2021, 12, 24),
        arrow.get(2022, 1, 24),
    ]

    # Test with very default holidays combined with custom holidays
    start = arrow.get(2021, 7, 1)
    holidays = pyholidays.FI()
    holidays[datetime.date(2021, 9, 24)] = "custom"
    holidays[datetime.date(2021, 11, 24)] = "custom"
    holidays[datetime.date(2021, 11, 25)] = "custom"
    holidays[datetime.date(2021, 11, 26)] = "custom"
    res = take_max(
        datecycles(
            1,
            "month",
            day=24,
            start=start,
            count=7,
            shift_to_workday="next",
            holidays=holidays,
        ),
        100,
    )
    assert res == [
        arrow.get(2021, 7, 26),
        arrow.get(2021, 8, 24),
        arrow.get(2021, 9, 27),
        arrow.get(2021, 10, 25),
        arrow.get(2021, 11, 29),
        arrow.get(2021, 12, 27),
        arrow.get(2022, 1, 24),
    ]

    # Test with very default holidays combined with custom holidays
    # Skip those items completely that are also holidays or weekends
    start = arrow.get(2021, 7, 1)
    holidays = pyholidays.FI()
    holidays[datetime.date(2021, 9, 24)] = "custom"
    holidays[datetime.date(2021, 11, 24)] = "custom"
    holidays[datetime.date(2021, 11, 25)] = "custom"
    holidays[datetime.date(2021, 11, 26)] = "custom"
    res = take_max(
        datecycles(
            1,
            "month",
            day=24,
            start=start,
            count=5,
            shift_to_workday="skip",
            holidays=holidays,
        ),
        100,
    )
    assert res == [
        arrow.get(2021, 8, 24),
        arrow.get(2022, 1, 24),
        arrow.get(2022, 2, 24),
        arrow.get(2022, 3, 24),
        arrow.get(2022, 5, 24),
    ]


def test_tzinfo():
    start = arrow.get(2021, 7, 10, tzinfo="Europe/Helsinki")
    res = take_max(
        datecycles(
            10, "day", start=start, count=7, tzinfo="Europe/Helsinki"
        ),
        100,
    )
    assert res == [
        arrow.get(2021, 7, 10, tzinfo="Europe/Helsinki"),
        arrow.get(2021, 7, 20, tzinfo="Europe/Helsinki"),
        arrow.get(2021, 7, 30, tzinfo="Europe/Helsinki"),
        arrow.get(2021, 8, 9, tzinfo="Europe/Helsinki"),
        arrow.get(2021, 8, 19, tzinfo="Europe/Helsinki"),
        arrow.get(2021, 8, 29, tzinfo="Europe/Helsinki"),
        arrow.get(2021, 9, 8, tzinfo="Europe/Helsinki"),
    ]

def test_weekday():
    # Test first thursday (full week is not required)
    start = arrow.get(2021, 7, 10)
    res = take_max(datecycles(1, "month", weekday=(0, False, "thursday"), start=start, count=3), 100)
    assert res == [
        arrow.get(2021, 8, 5),
        arrow.get(2021, 9, 2),
        arrow.get(2021, 10, 7),
    ]

    # Test first thursday (full week is required)
    start = arrow.get(2021, 7, 10)
    res = take_max(datecycles(1, "month", weekday=(0, True, "thursday"), start=start, count=3), 100)
    assert res == [
        arrow.get(2021, 8, 5),
        arrow.get(2021, 9, 9),
        arrow.get(2021, 10, 7),
    ]

    # Test second thursday (full week is required)
    start = arrow.get(2021, 7, 10)
    res = take_max(datecycles(1, "month", weekday=(1, True, "thursday"), start=start, count=3), 100)
    assert res == [
        arrow.get(2021, 7, 15),
        arrow.get(2021, 8, 12),
        arrow.get(2021, 9, 16),
    ]

    # Test second last thursday (full week is not required)
    start = arrow.get(2021, 7, 10)
    res = take_max(datecycles(1, "month", weekday=(-2, False, "thursday"), start=start, count=3), 100)
    assert res == [
        arrow.get(2021, 7, 22),
        arrow.get(2021, 8, 19),
        arrow.get(2021, 9, 23),
    ]

    # Test second last thursday (full week is required)
    start = arrow.get(2021, 7, 10)
    res = take_max(datecycles(1, "month", weekday=(-2, True, "thursday"), start=start, count=3), 100)
    assert res == [
        arrow.get(2021, 7, 15),
        arrow.get(2021, 8, 19),
        arrow.get(2021, 9, 16),
    ]
