#!/usr/bin/env python

import pdfquery
from pdfquery.cache import FileCache
import os

from lxml import etree

class pdfWrapper:

    __tmpDir = '/tmp/'

    def __findPlaytimePercentage(self, pdf):
        pdf.load(self.numPages - 1) # index of last page
        title = pdf.pq('LTTextLineHorizontal:contains("Playtime Percentage")')
        if not title:
            pdf.load(self.numPages-2,self.numPages-1)
            title = pdf.pq('LTTextLineHorizontal:contains("Playtime Percentage")')
            self.numPages = 2
        else:
            self.numPages = 1
        return pdf

    def __identifyTeams(self):
        config = [
        ('with_formatter', 'text'),
        ('team1', 'LTTextLineHorizontal:overlaps_bbox("400, 710, 475, 725")'),
        ('team2', 'LTTextLineHorizontal:overlaps_bbox("130, 710, 210, 725")')
        ]
        teams = self.pdf.extract(config)
        return teams

    def __init__(self, filename, scrape_target):
        self.scrape_target = scrape_target
        try:
            os.makedirs(self.__tmpDir)
        except OSError:
            if not os.path.isdir(self.__tmpDir):
                raise
        pdf = pdfquery.PDFQuery(filename, parse_tree_cacher=FileCache(self.__tmpDir))
        self.numPages = pdf.doc.catalog['Pages'].resolve()['Count']
        if self.scrape_target is 'PLAYTIME_PERCENTAGE':
            self.pdf = self.__findPlaytimePercentage(pdf)
            self.teams = self.__identifyTeams()
