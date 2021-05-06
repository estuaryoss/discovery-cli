import click
from prettytable import PrettyTable


class StackViewer:

    def __init__(self, service):
        """ Dump stack stats """
        self.service = service

    def view_deployments(self):
        click.echo("<<< deployments >>>")
        token = self.service.get_connection().get('token')
        discovery = self.service.get_connection().get('homePageUrl')
        deployments = self.service.get_deployments().get('description')
        table = PrettyTable()
        table.field_names = ["id", "container", "logs"]
        for deployment in deployments:
            if not isinstance(deployment, dict):
                break
            deployment_id = deployment.get('id')
            containers = deployment.get('containers')
            ip_port = deployment.get('ip_port')
            for container in containers:
                table.add_row([deployment_id, container,
                               f"curl -i -H Token:{token} -H IpAddr-Port:{ip_port} {discovery}deployers/deployments/logs/{deployment_id}"])
        click.echo(table.get_string())

    def view_active_commands(self):
        click.echo("<<< commands >>>")
        token = self.service.get_connection().get('token')
        discovery = self.service.get_connection().get('homePageUrl')
        commands = self.service.get_commands().get('description')
        table = PrettyTable()
        table.field_names = ["id", "command", "startedat", "finishedat", "duration", "code", 'agent', "details"]
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
                     cmd.get('commands').get(command_key).get('details').get('code'), cmd.get('ip_port'),
                     f"curl -i -H Token:{token} -H IpAddr-Port:{cmd.get('ip_port')} {discovery}agents/commanddetached"])
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
