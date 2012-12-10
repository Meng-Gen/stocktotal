import datetime

def get_last_month():
    today = datetime.date.today()
    first = datetime.date(day=1, month=today.month, year=today.year)
    last_month = first - datetime.timedelta(days=1)
    return datetime.date(day=1, month=last_month.month, year=last_month.year)
    
def get_this_month():
    today = datetime.date.today()
    return datetime.date(day=1, month=today.month, year=today.year)

def get_yesterday():
    return datetime.date.today() - datetime.timedelta(days=1)

def get_last_month_by(someday):
    first = datetime.date(day=1, month=someday.month, year=someday.year)
    last_month = first - datetime.timedelta(days=1)
    return datetime.date(day=1, month=last_month.month, year=last_month.year)

def get_this_month_by(someday):
    return datetime.date(day=1, month=someday.month, year=someday.year)
    
def get_last_year_by(someday):
    first = datetime.date(day=1, month=someday.month, year=someday.year)
    assert first.day is 1
    return datetime.date(day=1, month=first.month, year=first.year-1)

def get_this_quarter():
    this_month = get_this_month()
    quarter = int((this_month.month + 2)/3)
    return datetime.date(day=this_month.day, month=quarter * 3, year=this_month.year)

def get_last_quarter():
    last_three_months = get_this_month()
    for i in range(3):
        last_three_months = get_last_month_by(last_three_months)
    quarter = int((last_three_months.month + 2)/3)
    return datetime.date(day=last_three_months.day, month=quarter * 3, year=last_three_months.year)

def get_last_four_quarter():
    last_three_months = get_this_month()
    for i in range(12):
        last_three_months = get_last_month_by(last_three_months)
    quarter = int((last_three_months.month + 2)/3)
    return datetime.date(day=last_three_months.day, month=quarter * 3, year=last_three_months.year)    
    
def get_this_quarter_by(someday):
    this_month = get_this_month_by(someday)
    quarter = int((this_month.month + 2)/3)
    return datetime.date(day=this_month.day, month=quarter * 3, year=this_month.year)
    
def get_last_quarter_by(someday):
    last_three_months = get_this_month_by(someday)
    for i in range(3):
        last_three_months = get_last_month_by(last_three_months)
    quarter = int((last_three_months.month + 2)/3)
    return datetime.date(day=last_three_months.day, month=quarter * 3, year=last_three_months.year)
       