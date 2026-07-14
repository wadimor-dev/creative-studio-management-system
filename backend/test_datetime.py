from datetime import datetime, timezone, timedelta

def check_datetime():
    now = datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None)
    st = datetime.now().replace(tzinfo=timezone.utc)
    try:
        diff = now - st
        print(diff)
    except Exception as e:
        print("Error:", type(e), e)

if __name__ == "__main__":
    check_datetime()
