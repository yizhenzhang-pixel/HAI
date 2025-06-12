from crontab import CronTab

cron = CronTab(user=True)

# 清除旧任务（包含 main.py 的）
for job in cron:
    if "main.py" in job.command:
        cron.remove(job)

# 添加新任务（只添加一次）
command =  '/Users/wooton/PycharmProjects/PythonProject3/.venv/bin/python /Users/wooton/PycharmProjects/PythonProject3/智能日报系统-终端版/main.py >> /Users/wooton/Desktop/daily_log.txt 2>&1'
job = cron.new(command=command, comment='📩 每日智能日报')
job.setall('0 10 * * *')

cron.write()
print("✅每天早上10点自动发送日报")