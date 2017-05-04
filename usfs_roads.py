#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
This is a translation file for the US National Forest System Roads shapefile.
See a small sample (converted to GeoJSON) here: http://bl.ocks.org/d/1f2777005f18500730f2e500e377832c
The data can be obtained here: https://data.fs.usda.gov/geodata/edw/datasets.php
This is the link to the national file: https://data.fs.usda.gov/geodata/edw/edw_resources/shp/S_USA.RoadCore_FS.zip (395MB!)
'''

from osgeo import ogr

def cleaned_up(roadname):
    # TODO expand on this basic cleanup
    return roadname.title()


def filterTags(attrs):
    if not attrs:
        return
    tags = {}
    
    tags['highway'] = 'track'

    # Override highway type if it's a collector
    if 'FUNCTIONAL' in attrs:
        if 'COLLECTOR' in attrs['FUNCTIONAL']:
            tags['highway'] = 'unclassified'

    if 'OPER_MAINT' in attrs:
        if attrs['OPER_MAINT'][0] == '1':
            tags['access'] = 'official'
        elif attrs['OPER_MAINT'][0] == '2':
            tags['smoothness'] = 'very_bad'
        elif attrs['OPER_MAINT'][0] == '3':
            tags['smoothness'] = 'bad'
        elif attrs['OPER_MAINT'][0] == '4':
            tags['smoothness'] = 'intermediate'
        elif attrs['OPER_MAINT'][0] == '5':
            tags['smoothness'] = 'good'

    if 'NAME' in attrs:
        tags['name'] = cleaned_up(attrs['NAME'])

    if 'OPENFORUSE' in attrs:
        if attrs['OPENFORUSE'].strip() == 'ADMIN':
            tags['access'] = 'official'

    if 'LANES' in attrs:
         tags['lanes'] = attrs['LANES'][0]

    if 'SURFACE_TY' in attrs:
        if 'ASPHALT' in attrs['SURFACE_TY']:
            tags['surface'] = 'asphalt' 
        elif 'GRAVEL' in attrs['SURFACE_TY']:
            tags['surface'] = 'gravel' 
        else:
            tags['surface'] = 'dirt'

    # tags['source'] = 'US Forest Service, https://data.fs.usda.gov/geodata/edw/datasets.php'
    # this should go in the changeset

    return tags