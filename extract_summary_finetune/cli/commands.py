import click

@click.group()
def main_cli():
    """ extract_summary_finetune """
    pass


from .cmd_run import cli as summary
main_cli.add_command(summary())