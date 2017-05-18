import os

import json

import datetime


def read_json(fname):
    if not os.path.isfile(fname):
        print("File not found: %s" % fname)
        quit()

    with open(fname, "r") as fp:
        try:
            data = json.load(fp)
            return data['data']
        except:
            print("Invalid json file")
            quit()


def write_json(data, fname):
    with open(fname, 'w') as fp:
        json.dump({
            'version': '0.1',
            'date_written': datetime.datetime.now().isoformat(),
            'data': data
        }, fp, indent=4)

        fp.close()
