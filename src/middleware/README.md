"""
In this example you will learn how to adapt your bot to different languages
Using built-in middleware I18N.

You need to install babel package 'https://pypi.org/project/Babel/'
Babel provides a command-line interface for working with message catalogs
After installing babel package you have a script called 'pybabel'
Too see all the commands open terminal and type 'pybabel --help'
Full description for pybabel commands can be found here: 'https://babel.pocoo.org/en/latest/cmdline.html'

Create a directory 'locales' where our translations will be stored

First we need to extract texts:
    pybabel extract -o locales/{domain_name}.pot --input-dirs .
{domain_name}.pot - is the file where all translations are saved
The name of this file should be the same as domain which you pass to I18N class
In this example domain_name will be 'messages'

For gettext (singular texts) we use '_' alias and it works perfect
You may also you some alias for ngettext (plural texts) but you can face with a problem that
your plural texts are not being extracted
That is because by default 'pybabel extract' recognizes the following keywords:
 _, gettext, ngettext, ugettext, ungettext, dgettext, dngettext, N_
To add your own keyword you can use '-k' flag
In this example for 'ngettext' i will assign double underscore alias '__'

Full command with pluralization support will look so:
    pybabel extract -o locales/{domain_name}.pot -k __:1,2 --input-dirs .

Then create directories with translations (get list of all locales: 'pybabel --list-locales'):
    pybabel init -i locales/{domain_name}.pot -d locales -l en
    pybabel init -i locales/{domain_name}.pot -d locales -l ru
    pybabel init -i locales/{domain_name}.pot -d locales -l uz_Latn

Now you can translate the texts located in locales/{language}/LC_MESSAGES/{domain_name}.po
After you translated all the texts you need to compile .po files:
    pybabel compile -d locales

When you delete/update your texts you also need to update them in .po files:
    pybabel extract -o locales/{domain_name}.pot -k __:1,2 --input-dirs .
    pybabel update -i locales/{domain_name}.pot -d locales
    - translate
    pybabel compile -d locales

If you have any exceptions check:
    - you have installed babel
    - translations are ready, so you just compiled it
    - in the commands above you replaced {domain_name} to messages
    - you are writing commands from correct path in terminal
"""
