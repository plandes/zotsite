# Usage

**Important:** You _must_ shut down [Zotero] before you invoking this script.
Nothing goes wrong when you don't.  However, the script uses an SQLite file
that the program (pessimistically) locks.

The program has two modes: show configuration (a good first step) and create
the web site.


## Show Structure

You can see what the program is parsing from your [Zotero] library:

```bash
zotsite print
```


## Website Creation

Run the program (without the angle brackets):

```bash
zotsite export -o <sitedir>
```

After the program runs, `sitedir` will be where the tool creates/generates the
the new site.  Note you can also give a `--datadir` to tell the program where
your [Zotero] library is.  This can also be configured in
your [configuration file](#configuration-file).

The website will work as served from either a website or from the local file
system.  You can pass `levels` as a URL encoded parameter to produce the number
of levels when the page is loaded.

On the left you can click on the tree to select collections or attachments.
You have to drill all the way down to the leaf level in the tree to get at your
attachements and notes.  At the leaf level you can select and unselect a node
but all other nodes are note *selectable*.

By clicking on a non-leaf node it expands or collapses everything *and* gives
the meta data for that collection.  Note that this behavior was decided more by
the way [Tree View] works more than anything else since it is designed to show
the entire tree list at once.


## Subcollections

The folder directory structure in [Zotero] are called *collections*.  You can
export and print only collections given a regular expression with the
`--collection` flag.

To export only collections with the *Deep* and *Learning*, use the following.
```bash
zotsite export --collection '.*Deep\s*Learning.*'
```

This option is handy if you want to hand off a particular set of collection(s)
to a colleague or shared project etc.  To include entries at the time level
(i.e. find those actual papers by name), see the `match_children` configuration
in the [configuration file].

The [Python regular expression] syntax.  One gotcha is a `.*` is needed at the
front of a string to match anything.


## Database Filtering

The [configuration file] provides a way to give a database `where like` clause
to filter collections.  By default this is set to `%%` (a double percent is
need as the percent sign itself is used to escape).


## Configuration File

All command line parameters you provide can also be given in a `ini` style
configuration file, for example:

```ini
[default]
data_dir = ${env:home}/Zotero
```

tells the program where the [Zotero] data directory is located in the user's
home directory with name `.zotero` (this defaults to the Zotero default).

You can indicate where the program configuration file is with the `ZOTSITERC`
environment variable or use the `--config` command line program.

See the [test case configuration file] for example of all options.  A few
important options include:

* **data_dir**: the directory where the Zotero DB files live
* **match_children**: when using --collection, match on items as well
* **file_mapping**: one of: item or long
* **id_mapping**: one of: `none`, `betterbib`
* **sort**: whether or not to sort items `none` or `case` (non-case might be
  added later)
* **library_id**: the library used to generate the site, which defaults to the
  Personal


## Keeping the Website In Sync With Zotero

Currently there is no way to do this (contributions are welcome).  However
there is a [synchronization script] I use to synchronize the output of the
website with a remote host.


## Platform

This project uses the SQLite Python library and should run on other platforms
but assumes a directory structure that's been tested on OSX.


## URL Parameters

The generated website takes the following URL encoded parameters:

* **levels**: The number of levels to display in the left navigation tree.
* **id**: The document ID used to display and navigate when the page loads.
* **isView**: if `1`, go directly to the PDF rather than the information page.


## Robust File System Access

If one file copy from the Zotero storage fails, the program will dump a stack
trace and terminate.  However, there might be cases where the database might
have out-of-sync entries from the storage files, but you still want to export
those entries that are available.

To change this behavior and robustly deal with missing entries, add the
following to the [configuration file]:

```ini
[site_creator]
robust_fs = True
```

This tells the program to continue to try to export even when encountering file
system copy issues.  However, you'll get a lot of verbose error output if there
is some larger issue.


<!-- links -->
[configuration file]: #configuration-file
[Zotero]: https://www.zotero.org
[test case configuration file]: https://github.com/plandes/zotsite/blob/master/test-resources/zotsite.conf
[synchronization script]: https://github.com/plandes/zotsite/blob/master/src/sh/zotsync.sh
