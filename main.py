#! /usr/bin/python
# -*- coding: utf-8 -*-

import random
import time
import win32com.client
import os
from class_buildings import Building

def play_script(w):
    w.iimInit("", 1)
    w.iimPlay("OgameAuto\\ConnexionToAccountTest")
    time.sleep(1)


def creating_build_order():
    tab = []
    with open('buildorder', 'r') as build_order:
        for line in build_order.readlines():
            current_line = line.split(' ')
            if line.replace('\n', '') and current_line.__len__() == 4:
                tab.append((current_line[1], int(current_line[3].replace('\n', ''))))
    return iter(tab)


def is_construction(w):
    play_script(w)
    w.iimPlay("OgameAuto\\CheckBuildingInConstruction")
    no_construction = False if 'Aucun' in open('current_building.txt', 'r').read() else True
    return no_construction


def is_technology(w):
    play_script(w)
    w.iimPlay("OgameAuto\\CheckTechnologyInResearch")
    technology = False if 'Aucune' in open('current_technology.txt', 'r').read() else True
    return technology


def processing_build_order(w, current_item, build_order, dico, ressources, installations):
    print("Processing {}".format(current_item[0]))

    construction = is_construction(w)
    while construction:
        print('A building is currently being build')
        os.remove('current_building.txt')
        time.sleep(60 * random.randint(1, 10))
        construction = is_construction(w)
    os.remove('current_building.txt')

    current_building = Building(current_item)
    current_building.create_macro_check_availability(dico)
    w.iimPlay('OgameAuto\\CheckBuilding\\Check{}FactoryAvailable.iim'.format(current_building.nom))
    time.sleep(2)
    developper = open('developper.txt', 'r').read()
    test_developper = True if 'class=\"on\"' in developper else False
    while not test_developper:
        print('Not enough ressources')
        os.remove('developper.txt')
        time.sleep(60 * random.randint(1, 60))
        w.iimPlay('OgameAuto\\CheckBuilding\\Check{}FactoryAvailable.iim'.format(current_building.nom))
        developper = open('developper.txt', 'r').read()
        test_developper = True if 'class=\"on\"' in developper else False
    os.remove('developper.txt')

    try:
        w.iimPlay("OgameAuto\\UpgradeBuilding\\{}".format(dico[current_item[0]][1]))
        print('{} done'.format(current_item[0]))
        next_item = next(build_order)
        time.sleep(5)
        processing_build_order(w, next_item, build_order, dico, ressources, installations)

    except StopIteration:
        print('Build Finished')


def create_dico():
    dico = {'Solar': ('CheckSolarFactoryAvailable', 'UpSolarFactory', '4', (75, 30, 0), 1.5),
            'Metal': ('CheckMetalFactoryAvailable', 'UpMetalFactory', '1', (60, 15, 0), 1.5),
            'Crystal': ('CheckCristalFactoryAvailable', 'UpCristalFactory', '2', (48, 24, 0), 1.6),
            'Deuterium': ('CheckDeuteriumFactoryAvailable', 'UpDeuteriumFactory', '3', (225, 75, 0), 1.5),
            'Fusion': ('CheckFusionFactoryAvailable', 'UpFusionFactory', '5', (900, 360, 180), 1.8),
            'Robotics': ('CheckRobotsFactoryAvailable', 'UpRobotsFactory', '1', (400, 120, 200), 2),
            'Research': ('CheckLabFactoryAvailable', 'UpLabFactory', '3', (200, 400, 200), 2)}

    ressources = {'Solar Plant', 'Metal Mine', 'Crystal Mine', 'Deuterium Synthesizer', 'Fusion'}

    installations = {'Research Lab', 'Robotics Factory'}

    return dico, ressources, installations


def choose_place_in_build_order(build_order):
    place = input('Choose place in BO : ')
    for x in range(int(place) - 1):
        next(build_order)

def clean_directory():
    for x in os.listdir('.'):
        if '.txt' in x:
            os.remove(x)

def main():
    w = win32com.client.Dispatch("imacros")
    clean_directory()
    if os.path.exists('developper.txt'): os.remove('developper.txt')
    if os.path.exists('current_building.txt'): os.remove('current_building.txt')
    build_order = creating_build_order()
    choose_place_in_build_order(build_order)
    dico, ressources, installations = create_dico()
    processing_build_order(w, next(build_order), build_order, dico, ressources, installations)
    print(is_technology(w))

if __name__ == '__main__':
    main()
