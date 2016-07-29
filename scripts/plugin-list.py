#!/usr/bin/env python3
"""Parses pom.xml and outputs a Markdown-friendly list of plugins and their
versions.
"""
import os
import xml.etree.ElementTree as ET


def main():
    pom = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../pom.xml')
    tree = ET.parse(pom)
    props = tree.find("{http://maven.apache.org/POM/4.0.0}properties")
    plugins = []

    for plugin in props.getchildren():
        name = plugin.tag.split('}', 1)[1].split('.', 1)[0]
        ver = plugin.text
        plugins.append({'name': name, 'version': ver})

    print('Jenkins plugins:')
    for plugin in sorted(plugins, key=lambda k: k['name']):
        print("  * {} v{}".format(plugin['name'], plugin['version']))


if __name__ == '__main__':
    main()
