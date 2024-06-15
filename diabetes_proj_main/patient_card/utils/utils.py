def group_by_date(measurements):
    grouped_dates = {}
    for measurement in measurements:
        date_key = measurement.date_of_measurement
        if date_key not in grouped_dates:
            grouped_dates[date_key] = []
        grouped_dates[date_key].append(measurement)
    return (grouped_dates, list(grouped_dates.items()))