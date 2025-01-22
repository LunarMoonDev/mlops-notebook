import click
from datetime import datetime

from score import ride_duration_prediction

@click.command()
@click.option('--taxi_type', required=True, help='Type of the taxi')
@click.option('--run_id', required=True, help='Unique ID for the run')
@click.option('--year', required=True, help='Year of the input data')
@click.option('--month', required=True, help='Month of the input data')
def run(taxi_type, run_id, year, month):
    click.echo(f"Taxi type: {taxi_type}")
    click.echo(f"Run ID: {run_id}")
    click.echo(f"Year: {year}")
    click.echo(f"Month: {month}")
    
    ride_duration_prediction(
        taxi_type=taxi_type,
        run_id=run_id,
        run_date=datetime(year=int(year), month=int(month), day=1)
    )

if __name__ == '__main__':
    run()