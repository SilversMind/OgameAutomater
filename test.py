#! /usr/bin/python
# -*- coding: utf-8 -*-

def needed_ressources(building):
    base, multiplier = (60, 15, 0), 1.5
    lvl = 8
    add = lambda base_element, multiplier, lvl: base_element*(multiplier**(lvl - 1))
    print([add(base_element, multiplier, lvl) for base_element in base])

if __name__ == '__main__': main()