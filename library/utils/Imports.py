# -*- coding: utf-8 -*-

"""
    File name: projectileConfig.py
    Author: Grégory LARGANGE
    Date created: 17/11/2021
    Last modified by: Grégory LARGANGE
    Date last modified: 17/11/2021
    Python version: 3.8.1
"""


from random import randint


class Imports:
    @staticmethod
    def extract_text(text_file_path):
        lines = []
        with open(text_file_path, "r") as txtf:
            for _ in txtf:
                currentLine = txtf.readline().rstrip("\n")
                lines.append(currentLine)
        txtf.close()

        return lines

    @classmethod
    def random_name(cls, text_file_path):
        names_list = cls.extract_text(text_file_path)
        return names_list[randint(0, len(names_list) - 1)]
