from useconf import export_path

_hide_SQL_URL: str = "postgresql+asyncpg://postgres:root@localhost/fast"
_hide_SESSION_SECRET_KEY = "qQWEdqwdwqefASDQF4qw4h3ofv3vw3oervwg532gg5"
_hide_ADMIN_PANEL: tuple[str, str, str] = ("user", "password", "emal")

host = "0.0.0.0"
port = 8080

EXPORT_PATH = [
    export_path(
        namefile="__env.env",
        path="./test",
        template="""
SQL_URL = $$(sql_url)$$
SESSION_SECRET_KEY = $$(session_secret_kry)$$
ADMIN_PANEL = $$(admin_panel)$$
"""[1:], kwargs={
            "sql_url": _hide_SQL_URL,
            "session_secret_kry": _hide_SESSION_SECRET_KEY,
            "port": port,
        }
    )
]
