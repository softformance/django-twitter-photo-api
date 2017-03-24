import os
from crontab import CronTab

my_cron = CronTab(user='dmytro')
current_directory = os.getcwd()

# create new job
#dont forget chmox +x to scripts
job = my_cron.new(command='source ' + current_directory + '/bin/activate && python ' + current_directory + '/src/manage.py sync_by_app 1 >' + current_directory + '/syncCron.log 2>&1', comment='twitter_sync_tags')

# schedule created job
job.minute.every(10)

# write the job to the cron tab
my_cron.write()
