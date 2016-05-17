#!/usr/bin/env python

import pdfquery
from pdfquery.cache import FileCache
import os

from lxml import etree

class pdfWrapper:

    __tmpDir = '/tmp/'

    # Magic numbers! magic numbers everywhere! Bah!
    def __buildRows(self):
        y0 = 681.62
        y1 = 691.62
        rows_team1 = []
        while y0 > 0 and y1 > 0:
            elements = self.pdf.pq('LTTextLineHorizontal:overlaps_bbox("%s, %s, %s, %s")' % (37.0, y0, 302.217, y1))
            rows_team1.append(elements)
            y0 = y0 - 14.5
            y1 = y1 - 14.5
        rows_team2 = []
        307.0, 681.656, 336.856, 691.656
        y0 = 681.656
        y1 = 691.656
        while y0 > 0 and y1 > 0:
            elements = self.pdf.pq('LTTextLineHorizontal:overlaps_bbox("%s, %s, %s, %s")' % (307.0, y0, 572.217, y1))
            rows_team2.append(elements)
            y0 = y0 - 14.8
            y1 = y1 - 14.8
        for r in rows_team2:
            print r.text()
        return {'team1': rows_team1, 'team2': rows_team2}

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
        ('team1', 'LTTextLineHorizontal:overlaps_bbox("130, 710, 210, 725")'),
        ('team2', 'LTTextLineHorizontal:overlaps_bbox("400, 710, 475, 725")')
        ]
        teams = self.pdf.extract(config)
        return teams

    def __identifyRosters(self):
        config = [
        ('with_formatter', 'text'),
        ('team1', 'LTTextLineHorizontal:overlaps_bbox("37.0, 48.02, 80.896, 691.62")'),
        ('team2', 'LTTextLineHorizontal:overlaps_bbox("307.0, 49.556, 350.624, 691.656")')
        ]
        rosters = self.pdf.extract(config)
        for k,v in rosters.iteritems():
            rosters[k] = zip(rosters[k].split()[::2],rosters[k].split()[1::2])
        return rosters

    def __identifyPositions(self):
        config = [
        ('with_formatter', 'text'),
        ('team1', 'LTTextLineHorizontal:overlaps_bbox("128.512, 48.02, 140.68, 691.62")'),
        ('team2', 'LTTextLineHorizontal:overlaps_bbox("399.952, 49.556, 412.12, 691.656")')
        ]
        positions = self.pdf.extract(config)
        for k,v in positions.iteritems():
            positions[k] = positions[k].split()
        return positions

    def __identifyOffenseStats(self):
        config = [
        ('with_formatter', 'text'),
        ('team1', 'LTTextLineHorizontal:overlaps_bbox("155, 0, 190, 692")'),
        ('team2', 'LTTextLineHorizontal:overlaps_bbox("399, 0, 412.12, 691.656")')
        ]
        positions = self.pdf.extract(config)
        for k,v in positions.iteritems():
            positions[k] = positions[k].split()
        return positions

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
            self.rosters = self.__identifyRosters()
            self.positions = self.__identifyPositions()
            self.rows = self.__buildRows()
