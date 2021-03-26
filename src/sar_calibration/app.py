import os
import sys
import logging
import click

# from snapista import Graph
from .calibration_s1 import graph_calibrate_s1

os.environ['_JAVA_OPTIONS'] = '-Xms24g -Xmx24g'

logging.basicConfig(
    stream=sys.stderr,
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)-8s %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)


@click.command()
@click.option("--safe", "safe", help="Path to Sentinel-1 SAFE folder")
def main(safe):

    logging.info(f"{safe} calibration")
    print(f"{safe} calibration")
    
    print('\nDefining the Graph')
    graph = graph_calibrate_s1(safe)

    print('\nView the Graph')
    logging.info(graph.view())
    
    print('\nExecute the Graph') 
    # graph.run() # default gpt_options=["-x", "-c", "1024M"]
    graph.run(gpt_options=["-x", "-c", "20000M"])

    logging.info("Hello World!")


if __name__ == "__main__":
    main()
