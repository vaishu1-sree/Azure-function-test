import logging
import azure.functions as func
from datetime import datetime
import mycode

app = func.FunctionApp()

# -----------------------------
# HTTP Trigger: /api/add?a=5&b=10
# -----------------------------
@app.route(route="add", auth_level=func.AuthLevel.ANONYMOUS)
def add(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Processing HTTP add request")

    a = req.params.get("a")
    b = req.params.get("b")

    if not a or not b:
        try:
            body = req.get_json()
            a = a or body.get("a")
            b = b or body.get("b")
        except ValueError:
            pass

    try:
        a_i = int(a)
        b_i = int(b)
    except (TypeError, ValueError):
        return func.HttpResponse(
            "Provide integers 'a' and 'b' as query params or JSON body.",
            status_code=400
        )

    result = mycode.add_numbers(a_i, b_i)
    return func.HttpResponse(str(result), status_code=200, mimetype="text/plain")


# -----------------------------
# Timer Trigger: one-time run
# -----------------------------
# CRON: second minute hour day month day-of-week
# Runs at 16:25 UTC on 21 Aug (2025, and every year after unless removed)
@app.schedule(schedule="0 00 20 21 8 *",
              arg_name="timer",
              run_on_startup=False,
              use_monitor=True)
def scheduledtask(timer: func.TimerRequest) -> None:
    utc_time = datetime.utcnow().isoformat()
    logging.info(f"Scheduled task fired at {utc_time} UTC")

    # Example: use your add_numbers function
    result = mycode.add_numbers(5, 10)
    logging.info(f"Timer trigger executed add_numbers(5, 10) = {result}")
