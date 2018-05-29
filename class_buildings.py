#! /usr/bin/python
# -*- coding: utf-8 -*-

import win32com.client
import time
import os

"""Dictionnary for the specificty of any of the buildings:
Column 1: IMacros to check if sufficient ressources to building this building is available
Column 2: IMacros to upgrade the building
Column 3: Positional variable of the building on html page needed to build the macros
Column 4: Base materials for lvl 1 buildings, needed for calculate cost for any building level
Column 5: Multiplier for needed ressources, depend on kind of building
"""

dico = {'Solar': ('CheckSolarFactoryAvailable', 'UpSolarFactory', '4', (75, 30, 0), 1.5),
            'Metal': ('CheckMetalFactoryAvailable', 'UpMetalFactory', '1', (60, 15, 0), 1.5),
            'Crystal': ('CheckCristalFactoryAvailable', 'UpCristalFactory', '2', (48, 24, 0), 1.6),
            'Deuterium': ('CheckDeuteriumFactoryAvailable', 'UpDeuteriumFactory', '3', (225, 75, 0), 1.5),
            'Fusion': ('CheckFusionFactoryAvailable', 'UpFusionFactory', '5', (900, 360, 180), 1.8),
            'Robotics': ('CheckRobotsFactoryAvailable', 'UpRobotsFactory', '1', (400, 120, 200), 2),
            'Research': ('CheckLabFactoryAvailable', 'UpLabFactory', '3', (200, 400, 200), 2)}

ressources = {'Solar', 'Metal', 'Crystal', 'Deuterium', 'Fusion'}
technologies = {'Energy', 'Laser', 'Ion', 'Hyperspacetechno', 'Plasma', 'Spytechno', 'Computer', 'Astrophysics',
                'Network', 'Graviton', 'Combustion', 'Impulsion', 'Hyperspacepropulsion', 'Weapons', 'Shield', 'Protection'}
class Building():
    def __init__(self, item):
        self.nom = item[0]
        self.level = item[1]
        self.category, self.type = self.assign_type()
        self.base = dico[self.nom][3]
        self.multiplier = dico[self.nom][4]

    def create_macro_check_availability(self, dico):
        with open('C:\\Users\\Sam\\Documents\\iMacros\\Macros\\OgameAuto\\Check{}\\Check{}FactoryAvailable.iim'.format(self.type, self.nom), 'w') as imacro:
            imacro.write('VERSION BUILD=10022823\n')
            imacro.write('TAG POS=1 TYPE=SPAN ATTR=TXT:{}\n'.format(self.category))
            imacro.write('TAG POS=1 TYPE=LI ATTR=ID:button{} EXTRACT=HTM\n'.format(dico[self.nom][2]))
            imacro.write('SAVEAS TYPE=EXTRACT FOLDER=C:\\Users\\Sam\\PycharmProjects\\three_in_a_row\\OgameAutomater FILE=developper.txt')

    def needed_ressources(self):
        def add(base_element, multiplier, lvl): return int(base_element * (multiplier ** (lvl - 1)))
        print([add(base_element, self.multiplier, self.level) for base_element in self.base])

    def assign_type(self):
        if self.nom in ressources:
            type = ('Ressources', 'Building')
        elif self.nom in technologies:
            type = ('Recherche', 'Technology')
        else:
            type = ('Installations', 'Building')
        return type


def play_script(w):
    w.iimInit("", 1)
    w.iimPlay("OgameAuto\\ConnexionToAccountTest")
    time.sleep(1)
    w.iimPlay("OgameAuto\\GoToRessource")


def main():

    test_building = Building(('Metal', 15))
    test_building.needed_ressources()


if __name__ == '__main__': main()