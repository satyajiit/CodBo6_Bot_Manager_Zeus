from zeus_cod_bo6_bot_manager.backend.handlers.misc_handlers import get_hwid, copy_to_clipboard
from zeus_cod_bo6_bot_manager.backend.handlers.servers_handler import get_servers, add_servers, check_server_health, delete_servers, \
    send_commands_to_target_vm, fetch_logs_from_servers
from zeus_cod_bo6_bot_manager.backend.utils.misc_utils import open_url_browser


def register_routes(app):
    app.add_url_rule("/getDeviceHwId", view_func=get_hwid, methods=["GET"])
    app.add_url_rule("/getServers", view_func=get_servers, methods=["GET"])
    app.add_url_rule("/copyToClipboard", view_func=copy_to_clipboard, methods=["POST"])
    app.add_url_rule("/addServers", view_func=add_servers, methods=["POST"])
    app.add_url_rule("/deleteServers", view_func=delete_servers, methods=["POST"])
    app.add_url_rule("/checkServerHealth", view_func=check_server_health, methods=["POST"])
    app.add_url_rule("/openUrlOnBrowser", view_func=open_url_browser, methods=["POST"])
    app.add_url_rule("/sendDashboardCommands", view_func=send_commands_to_target_vm, methods=["POST"])
    app.add_url_rule("/sendGamePadCommandToServers", view_func=send_commands_to_target_vm, methods=["POST"])
    app.add_url_rule("/tailLogs", view_func=fetch_logs_from_servers, methods=["POST"])