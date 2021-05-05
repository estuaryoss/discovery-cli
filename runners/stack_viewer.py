import click
from prettytable import PrettyTable


class StackViewer:

    def __init__(self, service):
        """ Dump stack stats """
        self.service = service

    def view_deployments(self):
        click.echo("<<< deployments >>>")
        deployments = self.service.get_deployments().get('description')
        click.echo(deployments)

    def view_active_commands(self):
        click.echo("<<< commands >>>")
        commands = self.service.get_commands().get('description')
        table = PrettyTable()
        table.field_names = ["id", "command", "startedat", "finishedat", "duration", "code", "details",
                             'agent']
        for cmd in commands:
            if cmd.get('commands') is None:
                break
            command_keys = list(cmd.get('commands').keys())
            for command_key in command_keys:
                table.add_row(
                    [cmd.get('id'), command_key,
                     cmd.get('commands').get(command_key).get('startedat'),
                     cmd.get('commands').get(command_key).get('finishedat'),
                     cmd.get('commands').get(command_key).get('duration'),
                     cmd.get('commands').get(command_key).get('details').get('code'),
                     f"curl -i -H Token:{self.service.get_connection().get('token')} {cmd.get('homePageUrl')}commanddetached",
                     cmd.get('ip_port')])
        click.echo(table.get_string())

    def view_eureka_apps(self):
        click.echo("<<< eureka apps >>>")
        eureka_apps = self.service.get_eureka_apps().get('description')
        table = PrettyTable()
        table.field_names = ["appName", "ipAddr", "port", "securePort", "homePageUrl", 'healthCheckUrl',
                             'statusPageUrl']
        eureka_app_names = dict.keys(eureka_apps)
        for eureka_app_name in eureka_app_names:
            for eureka_app in eureka_apps.get(eureka_app_name):
                table.add_row(
                    [eureka_app_name, eureka_app.get('ipAddr'), eureka_app.get('port'), eureka_app.get('securePort'),
                     eureka_app.get('homePageUrl'), eureka_app.get('healthCheckUrl'),
                     eureka_app.get('statusPageUrl')])
        click.echo(table.get_string())
