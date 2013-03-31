# Bam

A Python port of Zach Holman's boom tool (https://github.com/holman/boom).

## Wut?

Boom is a tool that lets you store and access text snippets from the command line. Bam is a Python port.

For example:

```
$ bam gifs trektennis http://i.imgur.com/xuzRj.gif
Bam! trektennis in gifs is http://i.imgur.com/xuzRj.gif. Got it.

$ bam trektennis
We just copied http://i.imgur.com/xuzRj.gif to your clipboard.
```

## How do get my hands on that?

Well, you could install Zach's Ruby gem.

But if you want this Python port run:

```
$ pip install git+git://github.com/mrben/bam.git
```

## Commands

```
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
```