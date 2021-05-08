from datetime import date, datetime, timedelta
import re


def titleToFileName(value):
    return re.sub(r'[^а-яА-Яa-zA-Z0-9_\s]', '', value)


def convertDate(value):
    correctDay = re.compile(r'(\d{2})\.(\d{2})\.(\d{4})')
    if re.match(correctDay, value):
        result = re.match(correctDay, value)
        return str(date(int(result.group(3)), int(result.group(2)), int(result.group(1))))

    currentDate = datetime.today()

    minutePattern = re.compile(r'(\d{1,2})\s[м]')
    if re.match(minutePattern, value):
        minutes = timedelta(minutes=int(re.match(minutePattern, value).group(1)))
        return str((currentDate - minutes).date())

    hourPattern = re.compile(r'(\d{1,2})\s[ч]')
    if re.match(hourPattern, value):
        hours = timedelta(hours=int(re.match(hourPattern, value).group(1)))
        return str((currentDate - hours).date())

    dayPattern = re.compile(r'(\d{1,2})\s[д]')
    if re.match(dayPattern, value):
        days = timedelta(int(re.match(dayPattern, value).group(1)))
        return str((currentDate - days).date())
