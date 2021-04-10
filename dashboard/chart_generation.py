def get_chart_data(orders,timeseries):
    data = {}
    for order in orders:
        if timeseries=='daily':
            key = str(order.date_ordered.strftime('%B %d')) 
        elif timeseries == 'monthly':
            key = str(order.date_ordered.strftime('%B')) 
        if key in data:
            data[key] += order.get_cart_total
        else:
            data[key] = order.get_cart_total
    return data    