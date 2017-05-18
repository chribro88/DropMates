import os
import json
import datetime

import logging

logger = logging.getLogger('stats')


def read_json(fname):
    logger.info("Reading json: %s" % fname)
    if not os.path.isfile(fname):
        logger.warning("File not found: %s" % fname)
        quit()

    with open(fname, "r") as fp:
        logger.debug("Opened file for reading")
        try:
            data = json.load(fp)
            return data['data']
        except:
            logger.warning("Invalid json file")
            quit()


def write_json(data, fname):
    logger.info("Writing data to json: %s" % fname)
    with open(fname, 'w') as fp:
        logger.debug("Opened")
        json.dump({
            'version': '0.1',
            'date_written': datetime.datetime.now().isoformat(),
            'data': data
        }, fp, indent=4)

        fp.close()
