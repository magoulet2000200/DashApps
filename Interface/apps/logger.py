import os

from datetime import datetime
from dash import html, dcc, callback, Output, Input, State


class CommLogger:
    logs = []
    jig_message = ""
    accept_line = int(os.environ.get("MAX_LOGS", 1000))
    
    @staticmethod
    def print_log(text, update=False, color=None):
        # global self.logs

        if len(CommLogger.logs) == 0:
            print("")
        
        if update:
            # global JIG_MESSAGE
            CommLogger.jig_message = text
        dt = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
        new_log = dt + text
        print(new_log)
        
        if color:
            new_log = html.P([dt, html.Span(text, style={'color': color})], className="text-log-line")
        else:
            new_log = html.P(new_log, className="text-log-line")

        CommLogger.logs.insert(0, new_log)
        while len(CommLogger.logs) >= CommLogger.accept_line:
            CommLogger.logs.pop()