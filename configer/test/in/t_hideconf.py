def export(
        file_name: str,
        path_out: str,
        template: str,
        kwargs: dict[str, str],
        is_rewrite: bool = True,
): return file_name, path_out, template, kwargs, is_rewrite


_hide_SQL_URL: str = "postgresql+asyncpg://postgres:root@localhost/fast"
_hide_SESSION_SECRET_KEY = "qQWEdqwdwqefASDQF4qw4h3ofv3vw3oervwg532gg5"
_hide_ADMIN_PANEL: tuple[str, str, str] = ("user", "password", "emal")

host = "0.0.0.0"
port = 8080

env = export("__env.env", "./test", """
SQL_URL = $$(sql_url)$$
SESSION_SECRET_KEY = $$(session_secret_kry)$$
ADMIN_PANEL = $$(admin_panel)$$
"""[1:], {
    "sql_url": _hide_SQL_URL,
    "session_secret_kry": _hide_SESSION_SECRET_KEY,
    "admin_panel": _hide_ADMIN_PANEL,
    "port": port,
})

EXPORT_PATH = [env]
