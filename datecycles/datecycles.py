import arrow
import holidays as pyholidays

weekdays = {
    "monday": 0,
    "tuesday": 1,
    "wednesday": 2,
    "thursday": 3,
    "friday": 4,
    "saturday": 5,
    "sunday": 6,
    "mon": 0,
    "tue": 1,
    "wed": 2,
    "thu": 3,
    "fri": 4,
    "sat": 5,
    "sun": 6,
    0: 0,
    1: 1,
    2: 2,
    3: 3,
    4: 4,
    5: 5,
    6: 6,
}

shift_units = {
    "day": "days",
    "week": "weeks",
    "month": "months",
    "year": "years",
    "days": "days",
    "weeks": "weeks",
    "months": "months",
    "years": "years",
}


def get_months_first_weekday(
    year, month, weekday, full_week=False, tzinfo=None
):
    weekday = weekdays[weekday]

    res = arrow.get(year, month, 1)

    shift = (weekday - res.weekday() + 7) % 7
    res = res.shift(days=shift)

    if full_week:
        start, end = res.span("week")
        if start.month != end.month:
            res = res.shift(weeks=1)

    return res


def get_months_last_weekday(
    year, month, weekday, full_week=False, tzinfo=None
):
    weekday = weekdays[weekday]

    res = arrow.get(year, month, 1).ceil("month").floor("day")

    shift = -((res.weekday() - weekday) % 7)
    res = res.shift(days=shift)

    if full_week:
        start, end = res.span("week")
        if start.month != end.month:
            res = res.shift(weeks=-1)

    return res


def datecycles(
    every_n,
    unit,
    day=None,
    weekday=None,
    shift_to_workday=None,
    start=None,
    end=None,
    count=None,
    country=None,
    holidays=None,
    tzinfo=None,
):
    # Validate input values

    if day is not None and weekday is not None:
        raise Exception("Day and weekday can't be both defined")

    if unit != "month" and weekday is not None:
        raise Exception("Weekday can only be defined when unit is month")

    if unit not in shift_units:
        raise Exception(
            "Invalid unit, allowed units: {}".format(shift_units.keys())
        )

    if day is not None and (not (1 <= day <= 31)):
        raise Exception(
            "Invalid day, only values in range [0, 31] are allowed"
        )

    if shift_to_workday is not None and shift_to_workday not in [
        "next",
        "previous",
        "skip",
    ]:
        raise Exception(
            "Invalid shift_to_workday value, arrowed values: next, previous, skip"
        )

    if start is None:
        start = arrow.get().floor("day").replace(tzinfo=tzinfo)

    # Get shift unit, resulting shift unit is used by arrow
    # (e.g. for months: .shift(months=2))
    shift_unit = shift_units[unit]

    # Holidays are read from holidays library. If country and shift_to_workday
    # are not defined, but holidays is, leave it as is for custom holiday
    # support
    if (
        country is not None
        and shift_to_workday is not None
        and holidays is None
    ):
        holidays = getattr(pyholidays, country)()
    elif holidays is None:
        holidays = dict()

    # How many unit shifts have been made already
    shifts = 0

    # How many values have been yielded
    yield_count = 0

    while True:
        # If day is not None, find the next occurance of that day. If start
        # month has less days than the requested day, move the day to the last
        # day of month
        # Otherwise just shift the start `shifts` times `every_n` amount using
        # `shift_unit` as the unit
        if day is not None:
            # If start day is less than desired day, go to next day in this
            # month
            # Otherwise take the day from next month
            if start.day <= day:
                max_day = start.ceil("month").floor("day").day
                res = start.replace(day=min(day, max_day))
            else:
                max_day = start.shift(months=1).ceil("month").floor("day").day
                res = start.shift(months=1).replace(day=min(day, max_day))

            # Shift n units
            res = res.shift(**{shift_unit: every_n * shifts})

            # Fix the day
            # This is needed when asked day exceeds start month's max day
            max_day = res.ceil("month").floor("day").day
            if res.day != day and res.day != max_day:
                res = res.replace(day=min(day, max_day))

        else:
            # Shift the start to next occurance
            res = start.shift(**{shift_unit: every_n * shifts})

        if unit == "month" and weekday is not None:
            # nth = order number for requested date
            # full_week = whether or not only full weeks are counted
            # dayofweek = monday/tuesday/.../mon/tue/.../0/1/...
            nth, full_week, dayofweek = weekday

            # If counting is started from the beginning of the month
            # Otherwise the counting is started from the end of the month
            if nth >= 0:
                # Get month's first occurance of requested weekday. This takes
                # into account whether or not the weekday must occur on a full
                # week.
                res = get_months_first_weekday(
                    res.year,
                    res.month,
                    dayofweek,
                    full_week=full_week,
                    tzinfo=tzinfo,
                ).shift(weeks=nth)
            else:
                # Get month's last occurance of requested weekday. This takes
                # into account whether or not the weekday must occur on a full
                # week.
                res = get_months_last_weekday(
                    res.year,
                    res.month,
                    dayofweek,
                    full_week=full_week,
                    tzinfo=tzinfo,
                ).shift(weeks=nth + 1)

            # If result is less than the required start date, increase shifts
            # by one and jump back to beginning of the loop
            if res < start.floor("day"):
                shifts += 1
                continue

        # If there was no result, stop iterating
        # This happens when the parameters are too strict and no dates can be
        # found.
        if res is None:
            return

        # If weekend/holiday results are not allowed, skip the days
        # forwards/backwards/completely.
        # next = find the next workday
        # previous = find the previous workday
        # skip = return nothing, jump to next iteration of the loop
        if shift_to_workday is not None:
            if shift_to_workday == "next":
                shift = 1
            elif shift_to_workday == "previous":
                shift = -1
            elif shift_to_workday == "skip":
                shift = 0
                if res.weekday() > 4 or res.date() in holidays:
                    shifts += 1
                    continue

            # Move the result day until a workday is found
            while shift != 0 and (res.weekday() > 4 or res.date() in holidays):
                res = res.shift(days=shift)

        # If end is defined and current result exceeds the end, then stop
        # iterating
        if end is not None and res > end.ceil("day"):
            return

        # Yield the result, increase yield count and initial shifts
        yield res
        yield_count += 1
        shifts += 1

        # If there has been requested number of yields, then stop iterating.
        # If count is not defined, yield_count never matches the None and will
        # yield new results infinitely.
        if count == yield_count:
            return
