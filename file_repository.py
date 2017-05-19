import os
import json
import datetime

import logging
import pickle

logger = logging.getLogger('stats')


def read_json(fname):
    logger.info("Reading json: %s" % fname)
    if not os.path.isfile(fname):
        logger.warning("File not found: %s" % fname)
        return

    with open(fname, "r") as fp:
        logger.debug("Opened file for reading")
        try:
            data = json.load(fp)
            return data['data']
        except:
            logger.warning("Invalid json file")
            quit()


# POSSIBLY DEPRECATED
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


def write_pickle(data, fname):
    logger.info("Writing data to pickle: %s" % fname)
    with open(fname, 'wb') as fp:
        pickle.dump(data, fp)


def read_pickle(fname):
    logger.info("Reading data from pickle: %s" % fname)

    if not os.path.isfile(fname):
        logger.warning("File not found: %s" % fname)
        return

    with open(fname, "rb") as fp:
        data = pickle.load(fp)
    return data or None
