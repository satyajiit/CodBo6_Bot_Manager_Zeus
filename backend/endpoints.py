from backend.handlers.servers_handler import get_servers, add_servers

def register_routes(app):
    app.add_url_rule("/getServers", view_func=get_servers, methods=["GET"])
    app.add_url_rule("/addServers", view_func=add_servers, methods=["POST"])
    app.add_url_rule("/checkServerHealth", view_func=check_server_health, methods=["GET"])
    app.add_url_rule("/openUrlOnBrowser", view_func=open_url_browser, methods=["POST"])