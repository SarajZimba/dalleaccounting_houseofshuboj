from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import pytz
from canteen.utils import create_student_bills  # Import your function

def schedule_job():
    # Nepal Timezone
    nepal_tz = pytz.timezone('Asia/Kathmandu')

    # Create a scheduler instance
    scheduler = BackgroundScheduler(timezone=nepal_tz)

    # # Schedule the job to run at the end of every month
    # scheduler.add_job(
    #     create_student_bills, 
    #     trigger='cron', 
    #     day='last',  # Runs on the last day of the month
    #     hour=23, 
    #     minute=59
    # )
    # Schedule the job to run at the end of every month
    scheduler.add_job(
        create_student_bills, 
        trigger='cron', 
        day=1,  # Runs on the last day of the month
        hour=14, 
        minute=50
    )

    # Start the scheduler
    scheduler.start()

    print("APSCHEDULER STARTED: Monthly bill creation scheduled")
