import argparse

parser = argparse.ArgumentParser(description='Getting info from sites')

parser.add_argument('source', type=str, help='RSS URL')

parser.add_argument(
    '--limit',
    type=int, 
    default=1, 
    help='Limit news topics if this parameter provided'
)

parser.add_argument(
    '--json',
    action='store_true', 
    help='Print result as JSON in stdout'
)

args = parser.parse_args()