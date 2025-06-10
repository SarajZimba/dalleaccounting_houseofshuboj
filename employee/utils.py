import nepali_datetime

from datetime import datetime 


# def convert_nepali_to_eng(date):

#     leave_date_from = date
#     leave_date_from = datetime.strptime(leave_date_from, "%Y-%m-%d").date()
#     year = leave_date_from.year
#     month = leave_date_from.month
#     day = leave_date_from.day
#     nepali_date = nepali_datetime.date(year, month, day).to_datetime_date()
#     print(nepali_date)




# convert_nepali_to_eng("2025-01-24")
# def convert_eng_to_nepali(date):

#     leave_date_from = date
#     leave_date_from = datetime.strptime(leave_date_from, "%Y-%m-%d").date()
#     year = leave_date_from.year
#     month = leave_date_from.month
#     day = leave_date_from.day
#     nepali_date = nepali_datetime.date.from_datetime_date(datetime.date(year, month, day))
#     print(nepali_date)


from datetime import datetime, date
import nepali_datetime

def convert_eng_to_nepali(date_str):
    leave_date_from = datetime.strptime(date_str, "%Y-%m-%d").date()
    year = leave_date_from.year
    month = leave_date_from.month
    day = leave_date_from.day
    nepali_date = nepali_datetime.date.from_datetime_date(date(year, month, day))
    print(nepali_date)
    month = nepali_date.strftime("%B")
    year = nepali_date.strftime("%Y")
    print(month)

    return year, nepali_date
# Example usage
# convert_eng_to_nepali("2025-01-24")



# convert_eng_to_nepali("2025-01-24")