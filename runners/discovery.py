import click


class Discovery:
    @staticmethod
    def get_discovery_info(service):
        response = service.about()
        description = response.get('description')
        if not isinstance(description, dict):
            raise Exception(f"{description}")
        click.echo(f"\nDiscovery Info\n{description}\n")
