# CMS Make
An automation script to act as an extension of the djangocms-installer to streamline the process of setting up a developing and production ready cms instance for Webfaction.

### How To Use
  1. Run obtain a copy of the files
 ```sh
 git clone https://github.com/cmhedrick/cms_make.git
 ```
  2. Copy the files into your project directory
```sh
cp cms_make/cms_make.py cms_make/cms_make.sh project/
```
  3. Change into your project directory
```sh
cd project
```
  4. Use python to run the cms_make.py followed by the name of the project
```sh
python cms_make.py project
```
  5. You'll be given a series of prompts. Pay attention and fill out accordingly!

### Couple Assumptions (My Standards)
This code was mainly used to scratch my own itch and works off the standards in which I have made when it comes to setting up projects on webfaction.
1. The project name is the same as the project directory
2. The web apps or folders to handle static content or named:
```sh
project_static
```
and
```sh
project_media
```
where "project" is the name of your project

*Maybe one day I'll make it more flexible to go off the user input. Though I will admit one of my aims is to make it "simple" for people to do and sometimes simplification comes with standardization*


(Un)License
----

Unlicence 
