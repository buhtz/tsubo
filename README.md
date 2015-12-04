<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [Tsubo](#tsubo)
- [Installation](#installation)
- [Usage](#usage)
  - [Basic](#basic)
  - [`--output-dir`](#--output-dir)
  - [`--input-dir`](#--input-dir)
  - [`--recursive`](#--recursive)
  - [`--action`](#--action)
  - [Extras](#extras)
- [The Name](#the-name)
- [Contact](#contact)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# Tsubo
A commandline tool creating random file names out of existing ones written in Python3.

For example you can use it to shuffle (randomized renaming) mp3-files on a mobile music-player doesn't support _real_ shuffle-play.

# Installation
Currently there is no install routine or process supported. It is on the todo-list. See [this feature request](https://github.com/buhtz/tsubo/issues/4) for details and status.

# Usage
You can see all possible arguments with `./tsubo.py --help`. The following sections will introduce all of them step by step. Don't be scared about losing your files. _Tsubo_ will never touch them if you don't ask im explicit for that!

## Basic
Do this in your music directory (e.g. `/home/user/Music`).
```
user@PC:~/Music$ tsubo.py '*.mp3'
```
It will result in an output like that:
```
/home/user/Music/01 - My Love.mp3;/home/user/Music/i0170.mp3
/home/user/Music/02 - Your Love.mp3;/home/user/Music/i0456.mp3
/home/user/Music/01 - Money.mp3;/home/user/Looser/i0421.mp3
```
_Tsubo_ scanned the current directory for all mp3-files (`'*.mp3'`), created new _random_ names for them. But no file renaming or coping is done here. The result is shown on the standard output - nothing more. The format is `[original-name];[random-name]`. For real renaming see the [`--action`](#--action) argument or pipe the output to another programm. Sub-directories per default are not treated (please see [`--recursive`](#--recursive)).

This include pattern (in the example here `'*.mp3'`) is mandatory. __Enclose it in single quotes to stop bash expanding__.

## `--output-dir`
The default behaviour of _Tsubo_ is to use as output directory the same where it finds the file in. When there are files in different sub-directories (please see [`--recursive`](#--recursive) for details) then this sub-directories will appear in the randomized result, too.

You can specify new path for the random named files.
```
user@PC:~/Music$ tsubo.py '*.mp3' --output-dir /media/myplayer
```
The result:
```
/home/user/Music/Superstar/01 - My Love.mp3;/media/myplayer/i0170.mp3
/home/user/Music/Superstar/02 - Your Love.mp3;/media/myplayer/i0456.mp3
/home/user/Music/Superstar/03 - Love U.mp3;/media/myplayer/i0131.mp3
```
The short form is `-o`.

Please see [`--recursive`](#--recursive) for other output related arguments.

## `--input-dir`

Per default _Tsubo_ use the current working diretory for _input_. Use this option to change that (e.g. when you are in your home directory).
```
user@PC:~/$ tsubo.py '*.mp3' --input-dir Music
```
The short form here would be `-i`.

The sub-directories are not treated here. Pllease see [`--recursive`](#--recursive) to change that.

## `--recursive`
_Tsubo_ normaly doesn't go recursivly through the sub-directories. You can change that like that.
```
user@PC:~/Music$ tsubo.py '*.mp3' --recursive
```
The result:
```
/home/user/Music/Superstar/02 - You Love.mp3;/home/user/Music/Superstar/K02.mp3
/home/user/Music/Superstar/01 - My Love.mp3;/home/user/Music/Superstar/K01.mp3
/home/user/Music/Looser/01 - Money.mp3;/home/user/Music/Looser/K00.mp3
```

You can collect the files from all sub-diretories _but_ use the current working directory for output.
```
user@PC:~/Music$ tsubo.py '*.mp3' --recursive --output-to-cwd
```
The result:
```
/home/user/Music/Superstar/02 - You Love.mp3;/home/user/Musik/r01.mp3
/home/user/Music/Superstar/01 - My Love.mp3;/home/user/Musik/r02.mp3
/home/user/Music/Looser/01 - Money.mp3;/home/user/Musik/r00.mp3
```

When your current working directorie is different from the input diretory this would be a solution.
```
user@PC:~/$ tsubo.py '*.mp3' --recursive --input Music --output-to-input 
```
The result:
```
Music/Superstar/02 - You Love.mp3;Music/v01.mp3
Music/Superstar/01 - My Love.mp3;Music/v00.mp3
Music/Looser/01 - Money.mp3;Music/v02.mp3
```

## `--action`
As described before _Tsubo_ doesn't touch the original files. It just use their names (in the meaning of strings), randomize them the way the user specified and print the to standard output.

You can specify an _action_ like command that would be executed for each pair (the original and the new randomized one) of filenames. The pattern could be described with `<action> 'ORG-FILE' 'RND-FILE'`
```
user@PC:~/Musik/Looser/$ tsubo.py '*.mp3' --action MyScript.sh
```
Will result in a shell execution like that
```
MyScript.sh '/home/user/Musik/test/Looser/01 - Money.mp3' '/home/user/Musik/test/Looser/b00.mp3'
```

_Be carefull_ when you want to use that to remove or rename files.
```
user@PC:~/Musik/Looser/$ tsubo.py '*.mp3' --action mv
ATTENTION: Your action include "mv". You should use that with care.
Are you really sure that you want to execute this action on each file?
The actions is: "mv"
Type "yes" if it is so:
```
_Tsubo_ will always ask you questions like that when your `--action` include `rm` or `mv`.

Please see [Extras](#Extras) to find out how to avaid that questions.

## Extras
To avoid question from _Tsubo_ when you use `rm` or `mv` with the `--action` option that this.
```
user@PC:~$ tsubo.py '*.mp3' --action mv --no-mv-security-question

user@PC:~$ tsubo.py '*.mp3' --action rm --no-rm-security-question
```

# The Name
It is based (not exactly the same) on a japanese word with the meaning of randomizing.

# Contact
Please feel free to ask anything you want or give ideas and wishes about _Tsubo_. You can use my mail but I please try the [Issue](https://github.com/buhtz/tsubo/issues) section of this project website.

Christian Buhtz <c.buhtz@posteo.jp> GnuPGP-Key ID 0751A8EC
