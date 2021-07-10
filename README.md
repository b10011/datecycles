# datecycles

Simple library for complicated date cycling rules

[PyPI](https://pypi.org/project/datecycles/)

[GitHub](https://github.com/b10011/datecycles)

## Installation

```bash
pip install --upgrade datecycles
```

## "Documentation"

Currently there is no proper documentation, but the code is somewhat commented,
there are examples at the end of this README, there are bunch of tests and
here's explanations for the parameters:

```python3
datecycles(
    every_n,
    unit,
    day=None,
    weekday=None,
    start=None,
    end=None,
    count=None,
    shift_to_workday=None,
    country=None,
    holidays=None,
    tzinfo=None,
)
```

`every_n: int` defines the cycle interval.

`unit: str` defines the interval unit / cycle duration. Allowed values:
`"day", "week", "month", "year"`.

`day: Optional[int]` defines the day of month that is requested. Cannot be used
with `weekday`.

`start: Optional[arrow.arrow.Arrow]` defines the minimum date.

`end: Optional[arrow.arrow.Arrow]` defines the maximum date. Can be used with
`count`.

`count: Optional[int]` defines maximum number of results returned. Can be used
with `end`.

`shift_to_workday: Optional[str]` defines how to handle results that are at
weekends or holidays. `"next"` finds the next workday, `"previous"` finds the
previous workday, `"skip"` skips the result completely, `None` returns the
result as is without shifting the date.

`country: str` defines the country to be used for holidays. Allowed values
are those that can be found in Python
[holidays](https://github.com/dr-prodigy/python-holidays) library. For example,
`holidays.Finland` and `holidays.FI` both exist so values `"Finland"` and `"FI"`
are both valid values.

`holidays: Union[dict, list]` defines the holidays. Can't be used with
`country`. If some custom holidays must be combined with country's holidays,
see [holidays](https://github.com/dr-prodigy/python-holidays) documentation
regarding adding custom holidays.

`tzinfo: str` defines the timezone used in results. `start` and `end` must also
have the same timezone that's defined here. Allowed values are those that
[arrow](https://github.com/arrow-py/arrow) accepts as a timezone.

## Usage

Importing:

```python3
# Import the function
from datecycles import datecycles
```

### Example 1

Cycle every month on 2nd day, starting from 2021-07-10, take 5 first results

```python3
datecycles(
    1,
    "month",
    day=2,
    start=arrow.get(2021, 7, 10),
    count=5
)

# [<Arrow [2021-08-02T00:00:00+00:00]>,
#  <Arrow [2021-09-02T00:00:00+00:00]>,
#  <Arrow [2021-10-02T00:00:00+00:00]>,
#  <Arrow [2021-11-02T00:00:00+00:00]>,
#  <Arrow [2021-12-02T00:00:00+00:00]>]
```

### Example 2

Cycle every month on first friday, starting from 2021-07-10 until end of year

```python3
datecycles(
    1,
    "month",
    weekday=(0, False, "friday"),
    start=arrow.get(2021, 7, 10),
    end=arrow.get(2021, 12, 31)
)

# [<Arrow [2021-08-06T00:00:00+00:00]>,
#  <Arrow [2021-09-03T00:00:00+00:00]>,
#  <Arrow [2021-10-01T00:00:00+00:00]>,
#  <Arrow [2021-11-05T00:00:00+00:00]>,
#  <Arrow [2021-12-03T00:00:00+00:00]>]
```

### Example 3

Cycle every month on first friday that appears in a full week, starting from
2021-07-10 until end of year

```python3
datecycles(
    1,
    "month",
    weekday=(0, True, "friday"),
    start=arrow.get(2021, 7, 10),
    end=arrow.get(2021, 12, 31)
)

# [<Arrow [2021-08-06T00:00:00+00:00]>,
#  <Arrow [2021-09-10T00:00:00+00:00]>,
#  <Arrow [2021-10-08T00:00:00+00:00]>,
#  <Arrow [2021-11-05T00:00:00+00:00]>,
#  <Arrow [2021-12-10T00:00:00+00:00]>]
```

### Example 4

Cycle every 3rd month on last friday that appears in a full week, starting from
2021-09-01, take 4 first results

```python3
datecycles(
    3,
    "month",
    weekday=(-1, True, "friday"),
    start=arrow.get(2021, 9, 1),
    count=4
)

# [<Arrow [2021-09-24T00:00:00+00:00]>,
#  <Arrow [2021-12-24T00:00:00+00:00]>,
#  <Arrow [2022-03-25T00:00:00+00:00]>,
#  <Arrow [2022-06-24T00:00:00+00:00]>]
```

### Example 5

Cycle every 3rd month on last friday that appears in a full week, starting from
2021-09-01, take 4 first results, in case the result is a weekend day or
holiday in Finland, go to the next workday

```python3
datecycles(
    3,
    "month",
    weekday=(-1, True, "friday"),
    start=arrow.get(2021, 9, 1),
    count=4,
    shift_to_workday="next",
    country="Finland"
)

# [<Arrow [2021-09-24T00:00:00+00:00]>,
#  <Arrow [2021-12-27T00:00:00+00:00]>,
#  <Arrow [2022-03-25T00:00:00+00:00]>,
#  <Arrow [2022-06-27T00:00:00+00:00]>]
```
