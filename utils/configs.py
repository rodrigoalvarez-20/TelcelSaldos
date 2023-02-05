from configparser import ConfigParser
import os

cfg = ConfigParser()

def get_mongo_creds():
    cfg.read(f"{os.getcwd()}/config.cfg")
    
    if cfg.has_option("MONGO", "HOST") and cfg.has_option("MONGO", "USER") and cfg.has_option("MONGO", "PASSWORD") and cfg.has_option("MONGO", "DB"):
        user = cfg.get("MONGO", "USER")
        pwd = cfg.get("MONGO", "PASSWORD")
        host = cfg.get("MONGO", "HOST")
        db = cfg.get("MONGO", "DB")

        return user, pwd, host, db
    else:
        print("Config file error: MONGO options not found")
        return None

def get_config(section, key):
    cfg.read(f"{os.getcwd()}/config.cfg")

    if cfg.has_option(section, key):
        return cfg.get(section, key)
    else:
        print("Config file error: [{}]:[{}] options not found".format(section, key))
        return None
