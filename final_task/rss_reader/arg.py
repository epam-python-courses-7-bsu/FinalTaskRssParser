import argparse


def parsargs():
    parser = argparse.ArgumentParser(description='Getting info from sites')
    parser.add_argument('source', type=str, help='RSS URL')

    parser.add_argument(
        '--limit',
        type=int, 
        help='Limit news topics if this parameter provided'
    )

    parser.add_argument(
        '--json',
        action='store_true', 
        help='Print result as JSON in stdout'
    )

    parser.add_argument(
        '--version',
        action='store_true',
        help='Print version of the application'      
    )

    parser.add_argument(
        '--verbose',
        action="store_true",
        help='Outputs verbose status messages'
    )

    args = parser.parse_args()
    
    return args

vers = 1.0