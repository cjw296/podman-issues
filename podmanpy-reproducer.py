from pathlib import Path

import click
import podman
from podman.errors import ImageNotFound


@click.group()
def cli():
    pass


@cli.command()
def postgres_container(
        image="docker.io/library/postgres",
        tag='latest'
):
    client = podman.from_env()
    image_tag = f'{image}:{tag}'
    try:
        client.images.get(image_tag)
    except ImageNotFound:
        client.images.pull(image, tag=tag)
    container = client.containers.run(
        image_tag,
        ports={'5432/tcp': 0},
        detach=True,
        auto_remove=True,
    )
    container = client.containers.get(container.id)
    port = int(container.ports[f'5432/tcp'][0]['HostPort'])
    print(f'postgres running and exposed on localhost:{port}')
    container.stop(timeout=0)


CLICKHOUSE_CONFIG = str((Path(__file__).parent / 'config').absolute())


@cli.command()
def clickhouse_container(
        image='docker.io/clickhouse/clickhouse-server',
        tag='latest'
):
    client = podman.from_env()
    image_tag = f'{image}:{tag}'
    try:
        client.images.get(image_tag)
    except ImageNotFound:
        client.images.pull(image, tag=tag)
    container = client.containers.run(
        image_tag,
        ports={'9000/tcp': 0},
        detach=True,
        auto_remove=True,
        volumes={CLICKHOUSE_CONFIG: {'bind': '/etc/clickhouse-server/config.d/', 'mode': 'ro'}},
    )
    container = client.containers.get(container.id)
    port = int(container.ports[f'9000/tcp'][0]['HostPort'])
    print(f'clickhouse running and exposed on localhost:{port}')
    container.stop(timeout=0)


@cli.command()
@click.pass_context
def all(ctx):
    "Run all cases"
    ctx.invoke(postgres_container)
    ctx.invoke(clickhouse_container)


if __name__ == '__main__':
    cli()
