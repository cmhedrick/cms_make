#!/usr/bin/env python

import subprocess
import sys
import os


class Project(object):

    def __init__(self):
        self.project = sys.argv[1]
        self.host = raw_input("Username for webfaction: ")
        self.dir = './{pro_name}/{pro_name}/'.format(pro_name=self.project)
        self.settings = self.dir + 'settings.py'
        self.install()
        self.version = self.django_check()
        self.mod_settings()
        self.replace_settings()
        self.resync()
        self.make_requirements()

    def install(self):
        subprocess.call(['virtualenv', 'venv'])
        subprocess.call(['venv/bin/pip', 'install', 'djangocms-installer'])
        print 'Django CMS Installer Installed'
        subprocess.call(['./cms_make.sh', self.project])
        subprocess.call(['venv/bin/pip', 'install', 'djangocms-snippet'])
        print 'Django CMS Snippets Installed'

    def django_check(self):
        version = subprocess.check_output(
            ['venv/bin/django-admin.py', 'version']
        ).strip('\n').split('.')[0:2]
        return version

    def mod_settings(self):
        i = 0
        with open(self.settings, 'r') as f:
            with open((self.settings + '.back'), 'w') as f2:
                if self.version == ['1', '6']:
                    for line in f:
                        i += 1
                        if i == 142:
                            f2.write(line.strip('\n') + ',\n')
                            f2.write('    \'djangocms_snippet\'\n')
                        elif i == 181:
                            f2.write(
                                (
                                    "        {\'ENGINE\':"
                                    "\'django.db.backends.sqlite3\', \'NAME\'"
                                    ": os.path.join(BASE_DIR,\'project.db\'), "
                                    "\'HOST\': \'localhost\', \'USER\': \'\',"
                                    " \'PASSWORD\': \'\', \'PORT\': \'\'}\n"
                                )
                            )
                        else:
                            f2.write(line)
                else:
                    for line in f:
                        i += 1
                        if i == 141:
                            f2.write(line.strip('\n') + ',\n')
                            f2.write('    \'djangocms_snippet\'\n')
                        elif i == 180:
                            f2.write(
                                (
                                    "        {\'ENGINE\':"
                                    "\'django.db.backends.sqlite3\', \'NAME\'"
                                    ": os.path.join(BASE_DIR,\'project.db\'), "
                                    "\'HOST\': \'localhost\', \'USER\': \'\',"
                                    " \'PASSWORD\': \'\', \'PORT\': \'\'}\n"
                                )
                            )
                        elif i == 196:
                            f2.write(line.strip('\n') + ',\n')
                            f2.write(
                                (
                                    "    \'djangocms_snippet\':"
                                    " \'djangocms_snippet.migrations_django\'\n"
                                )
                            )
                        else:
                            f2.write(line)
                f2.write('\n')
                f2.write('import site\n')
                f2.write('PRODUCTION = False\n')
                f2.write('\n')
                f2.write('if PRODUCTION:\n')
                f2.write('    # venv site packages\n')
                f2.write(
                    (
                        "    site.addsitedir(\'/home/" + self.host +
                        "/webapps/" + self.project +
                        "/" + self.project +
                        "/venv/lib/python2.7/site-packages\')"
                        "\n"
                    )
                )
                f2.write('\n')
                f2.write('    # venv activate this\n')
                f2.write(
                    (
                        "    activate_this = os.path.expanduser(\'"
                        "/home/" + self.host +
                        "/webapps/" + self.project +
                        "/" + self.project +
                        "/venv/bin/"
                        "activate_this.py\')\n"
                    )
                )
                f2.write(
                    (
                        "    DATABASES = {\n"
                        "        \'default\': {\n"
                        "        \'ENGINE\': \'django.db.backends.postgresql"
                        "_psycopg2\',\n"
                        "        \'NAME\': \'\',\n"
                        "        \'USER\': \'\',\n"
                        "        \'PASSWORD\': \'\',\n"
                        "        \'HOST\': \'\',\n"
                        "        \'PORT\': \'\',\n"
                        "        }\n"
                        "    }\n"
                    )
                )
                f2.write(
                    (
                        "    MEDIA_ROOT = \'/home/" + self.host +
                        "/webapps/" + (self.project + "_media") + "/\'\n" +
                        "    STATIC_ROOT = \'/home/" + self.host +
                        "/webapps/" + (self.project + "_static") + "/\'\n"
                    )
                )

    def replace_settings(self):
        subprocess.call(['rm', self.settings])
        subprocess.call(['mv', (self.settings + '.back'), self.settings])

    def resync(self):
        subprocess.call(['rm', (self.project + '/project.db')])
        if self.version == ['1', '6']:
            subprocess.call(
                [
                    'venv/bin/python',
                    (self.project + '/manage.py'),
                    'syncdb',
                    '--all'
                ]
            )
            print 'Synced the DB'
            subprocess.call(
                [
                    'venv/bin/python',
                    (self.project + '/manage.py'),
                    'migrate',
                    '--all',
                    '--fake'
                ]
            )
            print 'Migrated'
        else:
            subprocess.call(
                [
                    'venv/bin/python',
                    (self.project + '/manage.py'),
                    'migrate'
                ]
            )
            print 'Migrated'
            subprocess.call(
                [
                    'venv/bin/python',
                    (self.project + '/manage.py'),
                    'createsuperuser'
                ]
            )

    def make_requirements(self):
        os.system('venv/bin/pip freeze > ' + self.project + '/requirements.txt')
        subprocess.call(
            [
                'cp',
                (self.project + '/requirements.txt'),
                (self.project + '/requirements_pro.txt')
            ]
        )
        os.system(
            (
                'echo \'psycopg2\' >>'  + self.project + '/requirements_pro.txt'
            )
        )
        print 'Requirement Files Made'

Project()

