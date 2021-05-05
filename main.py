#!/usr/bin/env python3

import click

__author__ = "Catalin Dinuta"

import yaml

from about import properties
from model.config_loader import ConfigLoader
from runners.discovery import Discovery
from runners.stack_viewer import StackViewer
from service.eureka import Eureka
from service.restapi_service import RestApiService
from utils.io_utils import IOUtils


@click.command()
@click.option('--token', prompt='token', hide_input=True,
              help='The authentication token that will be sent via \'Token\' header. '
                   'Use \'None\' if estuary-agent is deployed unsecured')
@click.option('--protocol', help='The protocol with which the estuary-agent was deployed. Default is http. E.g. https')
@click.option('--cert', help='The certificate with which the estuary-discovery was deployed. E.g. https/cert.pem')
@click.option('--file', help='The yaml file path on disk. Default is "./config.yaml"')
def cli(token, protocol, cert, file):
    print(f"CLI version: {properties.get('version')}\n")
    connection = {
        "homePageUrl": None,
        "token": token,
        "protocol": protocol if protocol is not None else "http",
        "cert": cert if cert is not None else "https/cert.pem"
    }

    service = RestApiService(connection)
    file_path = file if file is not None else "config.yaml"

    config_loader = ConfigLoader(yaml.safe_load(IOUtils.read_file(file=file_path, type='r')))
    config = config_loader.get_config()
    eureka_server = config.get('eureka')
    eureka = Eureka(eureka_server)
    discovery_apps = eureka.get_type_eureka_apps('discovery')
    discoveries = [discovery_app.get('homePageUrl') for discovery_app in discovery_apps]
    if config.get('discovery'):
        discoveries = config.get('discovery')

    services = []
    for discovery in discoveries:
        connection['homePageUrl'] = discovery
        service = RestApiService(connection)
        services.append(service)

    # check if can connect
    for service in services:
        try:
            service.ping()
        except Exception as e:
            raise BaseException(f"Could not connect to the discovery "
                                f"{connection.get('homePageUrl')}. Error: {e.__str__()}")

    for service in services:
        Discovery.get_discovery_info(service=service)

    click.echo(f"Printing stack stats. Configuration file '{file_path}'")

    for service in services:
        stack_viewer = StackViewer(service)
        stack_viewer.view_deployments()
        stack_viewer.view_active_commands()
        stack_viewer.view_eureka_apps()

    exit_code = 0
    click.echo(f"Global exit code: {exit_code}\n")


if __name__ == "__main__":
    cli()
