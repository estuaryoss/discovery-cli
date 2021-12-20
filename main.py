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
@click.option('--username', prompt='username',
              help='The username used for the Basic authentication')
@click.option('--password', prompt='password', hide_input=True,
              help='The password used for the Basic authentication')
@click.option('--protocol', help='The protocol with which the estuary-discovery was deployed. '
                                 'Default is http. E.g. https')
@click.option('--cert', help='The certificate with which the estuary-discovery was deployed. E.g. https/cert.pem')
@click.option('--file', help='The yaml file path on disk. Default is "./config.yaml"')
def cli(username, password, protocol, cert, file):
    print(f"CLI version: {properties.get('version')}\n")

    file_path = file if file is not None else "config.yaml"

    config_loader = ConfigLoader(yaml.safe_load(IOUtils.read_file(file=file_path, type='r')))
    config = config_loader.get_config()
    config_eureka_servers = config.get('eureka')

    eureka_services = []
    discoveries = []

    if config_eureka_servers is not None:
        for config_eureka_server in config_eureka_servers:
            eureka_services.append(Eureka(config_eureka_server))

    try:
        for eureka_service in eureka_services:
            temp_discovery_apps = eureka_service.get_type_eureka_apps('discovery')
            for discovery_app in temp_discovery_apps:
                discoveries.append(discovery_app.get('homePageUrl'))
    except:
        click.echo("Unable to fetch the 'discovery' apps from Eureka server list")

    if config.get('discovery'):
        discoveries = config.get('discovery')

    services = []
    for discovery in discoveries:
        services.append(RestApiService({
            "homePageUrl": discovery,
            "username": username,
            "password": password,
            "protocol": protocol if protocol is not None else "http",
            "cert": cert if cert is not None else "https/cert.pem"
        }))

    # check if can connect
    for service in services:
        try:
            service.ping()
        except Exception as e:
            raise BaseException(f"Could not connect to the discovery "
                                f"{service.get_connection().get('homePageUrl')}. Error: {e.__str__()}")

    for service in services:
        Discovery.get_discovery_info(service=service)

    click.echo(f"Printing stack stats. Configuration file '{file_path}'\n")

    for service in services:
        click.echo(f"\nListing stack on Discovery service: {service.get_connection().get('homePageUrl')}\n")
        stack_viewer = StackViewer(service)
        stack_viewer.view_eureka_apps()
        stack_viewer.view_commands()

    exit_code = 0
    click.echo(f"Global exit code: {exit_code}\n")


if __name__ == "__main__":
    cli()
