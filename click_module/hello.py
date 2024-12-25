# pylint:disable
import click

# @click.command()
# def hello():
#     click.echo(click.style("Alert!!!", bg="white", fg='red'))
#     # print("Hello World!!")


@click.command()
@click.option('--count', default=1, help='Numbe of greetings')
@click.option('--name', prompt='Your name', help='Name of the person to greet')
def greet(count, name):
    for x in range(count):
        click.echo(click.style(f"Hello {name}!!", fg='blue'))

    click.echo(click.style('ATTENTION', blink=True, bold=True))
    click.echo('Hello World!', err=True)





if __name__ == '__main__':
    # hello()
    greet()