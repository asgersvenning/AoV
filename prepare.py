import os
from datetime import datetime
from argparse import ArgumentParser

if __name__ == "__main__":
    parser = ArgumentParser("prep-aov")
    parser.add_argument("-y", "--year", type=int, default=None, required=False)
    parser.add_argument("-d", "--day", type=int, nargs="+", default=None, required=False)
    args = parser.parse_args()
    year, days = args.year, args.day
    current = [int(p) for p in datetime.today().strftime('%Y-%m-%d').split("-")]
    if year is None:
        year = current[0]
    if days is None:
        days = current[2]
    if isinstance(days, int):
        days = [days]
    for day in days:
        year, day = f'{year}', f'{day:0>2}'
        
        # Files to create
        script_path = os.path.join(year, f'{day}.py')
        input_path, test_path = [os.path.join(year, "inputs", f'{day}.{tp}') for tp in ["input", "test"]]
        files = [script_path, input_path, test_path]

        # Make directories if necessary
        os.makedirs(os.path.dirname(input_path), exist_ok=True)

        # Make file(s)
        for file in files:
            if os.path.exists(file):
                print(file, "already exists, skipping.")
            else:
                open(file, "a").close()

        

