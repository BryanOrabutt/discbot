#!/usr/bin/env python
from os import mkdir, listdir
from os.path import isfile, isdir, join

KEY_FOLDER = "/home/bastion/discbot/keys"
BOT_FOLDER = "botdata"

def read_key(file):
    """
    Read a key file which contains bot tokens
    Return false if the key couldn't be read
    """
    try:
        with open(join(KEY_FOLDER, "{}.key".format(file)), 'r') as f:
            return f.read().strip("\n").strip("\r").replace("\n", "")
    except Exception:
        raise IOError("Can't read key")
    return False

def pre_text(string, lang=None):
    """
    Encapsulate a string inside a Markdown <pre> container
    """
    s = "```{}```"
    if lang is not None:
        s = s.format(lang+"\n{}")
    return s.format(string.rstrip().strip("\n").replace("\t", ""))

def bot_folder(bot_name):
    """
    Return the path to the bot's data folder
    ie: bot_folder("dumb-bot") -> botdata/dumb-bot
    """
    return join(BOT_FOLDER, bot_name)

def read_lines(file_name):
    """
    Read all the lines in a given file
    Shortcut to avoid clumping up of many with-blocks
    Handles the IO exception to return a blank list when no file is present
    """
    lines = []
    try:
        with open(file_name, "r") as f:
            lines = f.readlines()
    except Exception:
        pass
    return lines

def write_lines(file_name, lines):
    """
    Inverse of :read_lines, just do the opposite
    True if written, False otherwise
    """
    try:
        with open(file_name, "w") as f:
            f.writelines("\n".join([line.strip().replace("\n","") for line in lines
                               if line.strip().replace("\n","") != ""]))
    except Exception:
        return False
    return True
    

def create_filegen(bot_name):
    """
    Create a function which allows quick path joins
    to interact with files in a Bot's folder
    """
    def bot_file(filename):
        return join(BOT_FOLDER, bot_name, filename)
    return bot_file
