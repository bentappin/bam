# encoding: utf-8
from random import choice
import textwrap

import clint
from clint.textui import colored, indent, puts

from storage import DataStore
from platform import Platform


DELETE_OPTION = "--delete"
INDENT = 2
INDENT_LARGE = 4


class Command(object):

    def __init__(self, *args, **kwargs):
        self.storage = DataStore()
        self.platform = Platform()

    def _app_string(self):
        return colored.cyan('Bam!')

    def all(self):
        lists = self.storage.get_all_lists()
        for list_name, values in lists.iteritems():
            with indent(INDENT):
                puts(list_name)
                for k, v in values.iteritems():
                    with indent(INDENT):
                        puts('{}:\t\t{}'.format(k, v))

    def overview(self):
        lists = self.storage.get_all_lists()
        if lists:
            for list_name, values in lists.iteritems():
                with indent(INDENT):
                    puts("{} ({})".format(list_name, len(values)))
        else:
            self.help()

    def create_list(self, list_name, item_name=None, item_value=None):
        self.storage.create_list(list_name)
        print '{} Created a new list called {}.'.format(
            self._app_string(),
            colored.yellow(list_name)
        )
        if item_name and item_value:
            self.add_item(list_name, item_name, item_value)

    def detail_list(self, list_name):
        if self.storage.list_exists(list_name):
            for k, v in self.storage.get_list(list_name).iteritems():
                with indent(INDENT_LARGE):
                    puts('{}:\t\t{}'.format(k, v))
        else:
            print 'Cannot find list "{}".'.format(list_name)

    def delete_list(self, list_name):
        answer = raw_input(
            "You sure you want to delete everything in {}? (y/n): ".format(
                colored.yellow(list_name))
            )
        if answer.strip().lower() == 'y':
            self.storage.delete_list(list_name)
            print "{} Deleted all your {}.".format(
                self._app_string(),
                colored.yellow(list_name)
            )
        else:
            print "Just kidding then."

    def add_item(self, list_name, name, value):
        self.storage.add_item(list_name, name, value)
        print '{} {} in {} is {}. Got it.'.format(
            self._app_string(),
            colored.yellow(name),
            colored.yellow(list_name),
            colored.yellow(value)
        )

    def search_list_for_item(self, list_name, name):
        value = self.storage.get_item(name, list_name=list_name)
        print "{} We just copied {} to your clipboard.".format(
            self._app_string(),
            colored.yellow(self.platform.copy(value))
        )


    def search_items(self, name):
        value = self.storage.get_item(name)
        
        print "We just copied {} to your clipboard.".format(
            colored.yellow(self.platform.copy(value))
        )

    def delete_item(self, list_name, name):
        if self.storage.list_exists(list_name):
            try:
                self.storage.delete_item(list_name, name)
                print "{} {} is gone forever.".format(
                    self._app_string(),
                    colored.yellow(name)
                )
            except KeyError:
                print "{} {} {}.".format(
                    colored.yellow(name),
                    colored.red("not found in"),
                    colored.yellow(list_name)
                )
        else:
            print "We cound't find that list."

    def echo(self, major, minor=None):
        list_name = list_name = None
        if minor:
            list_name, item_name = major, minor
        else:
            item_name = major
            
        output = self.storage.get_item(item_name, list_name=list_name)
        if not output:
            if list_name and item_name:
                output = "{} {} {}".format(
                    colored.yellow(item_name),
                    colored.red("not found in"),
                    colored.yellow(list_name)
                )
            else:
                output = "{} {}".format(
                    colored.yellow(item_name),
                    colored.red("not found")
                )
        print output

    def edit(self):
        print "{} {}".format(
            self._app_string(),
            self.platform.edit(self.storage.data_path)
        )

    def open(self, major, minor):
        noun = None
        if self.storage.list_exists(major):
            the_list = self.storage.get_list(major)

            if minor:
                value = self.storage.get_item(minor, list_name=major)
                if value:
                    self.platform.open(value)
                    output = "{} We just opened {} for you."
                    noun = value
            else:
                for value in the_list.values():
                    self.platform.open(value)
                output = "{} We just opened all of {} for you."
                noun = major
        else:
            value = self.storage.get_item(major)
            if value:
                self.platform.open(value)
                output = "{} We just opened {} for you."
                noun = value
                
        print output.format(
            self._app_string(),
            colored.yellow(noun)
        )

    def random(self, major):
        if major and self.storage.list_exists(major):
            values = self.storage.get_list(major).values()
        else:
            values = self.storage.get_values()
        print "{} We just opened {} for you.".format(
            self._app_string(),
            colored.yellow(self.platform.open(choice(values)))
        )

    def execute(self):
        command = clint.args.get(0)
        major = clint.args.get(1)
        minor = clint.args.get(2)
        if not command:
            return self.overview()
        self.delegate(command, major, minor)

    def delegate(self, command, major, minor):
        if command == 'all':
            return self.all()
        elif command == 'help' or command[0] == '-':
            return self.help()
        elif command in ['echo', 'e']:
            return self.echo(major, minor)
        elif command == 'edit':
            return self.edit()
        elif command in ['open', 'o']:
            return self.open(major, minor)
        elif command in ['random', 'rand', 'r']:
            return self.random(major)

        if self.storage.list_exists(command):
            if major == DELETE_OPTION:
                return self.delete_list(command)
            if not major:
                return self.detail_list(command)
            if minor != DELETE_OPTION:
                if minor:
                    return self.add_item(command, major, minor)
                return self.search_list_for_item(command, major)

        if minor == DELETE_OPTION and self.storage.item_exists(major):
            return self.delete_item(command, major)

        if self.storage.item_exists(command) and not major:
            return self.search_items(command)

        return self.create_list(command, item_name=major, item_value=minor)

    def empty(self):
        text = """
            You don't have anything yet! To start out, create a new list:
              $ bam <list-name>
            And then add something to your list!
              $ bam <list-name> <item-name> <item-value>
            You can then grab your new item:
              $ bam <item-name>"""[1:]
        print textwrap.dedent(text)

    def help(self):
        text = """
            - bam: help ---------------------------------------------------

            bam                          display high-level overview
            bam all                      show all items in all lists
            bam edit                     edit the bam JSON file in $EDITOR
            bam help                     this help text

            bam <list>                   create a new list
            bam <list>                   show items for a list
            bam <list> --delete          deletes a list

            bam <list> <name> <value>    create a new list item
            bam <name>                   copy item's value to clipboard
            bam <list> <name>            copy item's value to clipboard
            bam open <name>              open item's url in browser
            bam open <list> <name>       open all item's url in browser for a list
            bam random                   open a random item's url in browser
            bam random <list>            open a random item's url for a list in browser
            bam echo <name>              echo the item's value without copying
            bam echo <list> <name>       echo the item's value without copying
            bam <list> <name> --delete   deletes an item
        """
        with indent(INDENT):
            puts(textwrap.dedent(text))


def main():
    Command().execute()


if __name__ == '__main__':
    main()
