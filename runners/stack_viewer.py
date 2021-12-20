import click
from prettytable import PrettyTable


class StackViewer:

    def __init__(self, service):
        """ Dump stack stats """
        self.service = service

    def view_commands(self):
        click.echo("<<< commands >>>")
        table = PrettyTable()
        table.field_names = ["id", "command", "startedAt", "finishedAt", "duration", "code", "stderr", "agent", "details"]
        username = self.service.get_connection().get('username')
        discovery = self.service.get_connection().get('homePageUrl')
        commands_response = self.service.get_commands().get('description')
        for agent_response in commands_response:
            commands = agent_response.get('description')
            if not isinstance(agent_response.get('description'), list):
                commands = []
            for cmd in commands:
                table.add_row(
                    [cmd.get('id'), cmd.get('command'), cmd.get('startedAt'), cmd.get('finishedAt'),
                     cmd.get('duration'), cmd.get('code'), cmd.get('err').replace("\r\n", " ").replace("\n", " ")[0:100],
                     agent_response.get('ip_port'),
                     f"curl -i -u {username}:****** -H IpAddr-Port:{agent_response.get('ip_port')} {discovery}agents/commands"])
        click.echo(table.get_string())

    def view_eureka_apps(self):
        click.echo("<<< eureka apps >>>")
        table = PrettyTable()
        table.field_names = ["appName", "ipAddr", "port", "securePort", "homePageUrl", 'healthCheckUrl',
                             'statusPageUrl']
        eureka_apps = self.service.get_eureka_apps().get('description')
        eureka_app_names = dict.keys(eureka_apps)
        for eureka_app_name in eureka_app_names:
            for eureka_app in eureka_apps.get(eureka_app_name):
                table.add_row(
                    [eureka_app_name, eureka_app.get('ipAddr'), eureka_app.get('port'), eureka_app.get('securePort'),
                     eureka_app.get('homePageUrl'), eureka_app.get('healthCheckUrl'),
                     eureka_app.get('statusPageUrl')])
        click.echo(table.get_string())
