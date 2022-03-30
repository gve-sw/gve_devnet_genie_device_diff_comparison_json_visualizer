""" Copyright (c) 2021 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
           https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied. 
"""

from django.shortcuts import render, HttpResponse
from django import forms
import json
import glob
import os
from graphviz import Digraph

ROOT_DIR = os.path.abspath(os.curdir)
JSONS_DIR = ROOT_DIR + '/json_files/*'
VISUALIZATION_DIR = ROOT_DIR + '/json_output/'

json_files = glob.glob(JSONS_DIR)


def json_to_image(data=None,name=None):
    u = Digraph(name, format='png',
                node_attr={'color': 'lightblue2', 'style': 'filled'},
                engine='dot')
    colors = {"int": '#d25f76',
              "float": 'orange',
              "list": '#6c42c1',
              "<class 'tuple'>": '#6c42c1',
              "dict": '#ae8f65',
              "str": '#96abff'}

    def get_type(var):
        return type(var).__name__

    def get_edges(treedict, parent=None, Clabel=None):
        for key in treedict.keys():
            # key_type = type(treedict[key])
            if parent:
                u.edge(parent, key, label=str(treedict[key]) ,fontcolor=colors[get_type(treedict[key])], color=colors[get_type(treedict[key])])
            if type(treedict[key]) not in [dict, list]:
                pass
                # u.edge(key,get_type(treedict[key]),label=get_type(treedict[key]))
            elif type(treedict[key]) is dict:
                # u.node(key)
                get_edges(treedict[key], parent=key,
                          Clabel=str(treedict[key]))
            elif type(treedict[key]) is list:
                # u.edge(parent,key,label="list")
                for i in treedict[key][:1]:
                    if type(i) not in [str, int, float]:
                        get_edges(i, parent=key, Clabel=str(i))
                    else:
                        u.edge(key, get_type(i), label=str(
                            i),fontcolor=colors[get_type(i)], color=colors[get_type(i)])

    if type(data) is list:
        for i, x in enumerate(data):
            if i < 1:
                get_edges(x,"List")
    elif type(data) is dict:
        main_ = "Response"
        u.node(main_)
        with u.subgraph() as s:
            s.attr(rank="same")
            for i in data.keys():
                s.node(i)
                s.edge(main_, i, label=str(data[i]), fontcolor=colors[get_type(data[i])],color=colors[get_type(data[i])])
        get_edges(data)
    return u.render(directory=VISUALIZATION_DIR)


class front_end(forms.Form):
    response = forms.JSONField()


def check(json,name):
    try:
        data = json_to_image(json,name)
    except Exception as e:
        print(e)
        return e

    return 0


if __name__ == "__main__":

    for json_file in json_files:

        striped_file_name = json_file.split('/')[-1].strip('.json')
        output_file_name = striped_file_name + '_tree'
        # Opening JSON file
        f = open(json_file)
        
        # returns JSON object as
        # a dictionary
        data = json.load(f)
        check(data,output_file_name)
