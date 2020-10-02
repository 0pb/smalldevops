
# SmallDevops

Small continuous developpement for python (currently for unittest only).
It consist in a python module/script that get information from your script and of a website that display those informations.

## **Requirements**

- Linux
- Python3 (only the module require it, you can still launch your own script in Python2.7 if you wish)

---

## **How it looks like** 

Commit with 3 failures in test : 
![website](example/smalldevops.png)

- "Passing test" refers to amount of test failed / total amount of test.
- "Timing (program)" come from the usr/bin/time command available on linux.

Right column 

- top : commit - date - index of commit - total amount of test - button to make the graph full size
- middle : Author and Commit message
- List error : Grid of test case; It refer to name of the test case (when you write `class Test_main(unittest.TestCase):` for example)
- List error (message) : Errors messages

---

## **How to use it**

- `pip install SmallDevops`
- `git init` in the folder you want (or you may want to use an already existing project)

### Basic : 

- `python -m SmallDevops create_website` will create a "file.html" in the current folder
- `python -m SmallDevops "python3.6 script.py"` will execute "python3.6 script.py" and create a file "output.js" in the current folder

Just open the file.html in your browser and voila.

This command `python -m SmallDevops "python3.6 script.py"` need to be run every time you commit, which mean you either need to type the command each time or you can use a post-commit hooks (like this [one](example/post-commit)) to automatically execute the script.

### Fully automatic : 

- `python -m SmallDevops create_website /path/where/you/want/the/website` will create a "file.html" in the folder indicated
- get the folder where you want to execute a script (let's say : "/path/to/script")
- create a hook post-commit or post-receive (if you put it on a server) in your .git/hooks folder with this command : `exec python -m SmallDevops "python script.py" -dir=/path/to/script -output=/path/where/you/want/the/website`

Now every you commit the script will run automatically and update the data accordingly.

### If you want to execute your script in python2.7 : 

Add `-template=unittest_timing_git_python27`.

---

## **How to add your own test class from the template**

First, what are those test class : It is the class used by the script in order to recover the data from your script.

Here is an example for [unittest](SmallDevops/template_class/unittest_timing_git.py) and here is the [base template](SmallDevops/template_class/base_class_test.py)

You can get the data however you want. Let's say you wish to use a particular program to time your function instead of the \time I use.
You just need to copy the example and modify the function that execute the \time function, as well as the function that process the data recovered.

Once you do that, you can either re-build the package, or you can use the `-template` and `-template_path option` to specify which test class you want to use.

--- 

## List of arguments (from devop.py) : 

```
python -m SmallDevops "[command to execute]"|create_website [list arg]
            -dir
            -show
            -output
            -nooutput
            -template
            -path_template

list argument possible =
    "-dir" : cd inside that dir for executing the script given as command
             is required if you execute a script from another folder
        ex: -dir=/relative/path/script
            -dir=/absolute/path/to/different/script

    "-show" : show the output from the command executed, ex a script that print
            "hello" to the console will then print "hello
                                                    json created
                                                    devop script done"
    ex: -show

    "-output" : create the output file in the corresponding folder
                if the output is a path (/absolute/path/), then a output.js will be created at that
                location
                if the output is a path with a file name (/absolute/path/filename.js) which mean an
                extension, then the file "filename.js" will be created at that path
                if the output is simply a file name (filename.js) the file "filename.js" will be
                created in the folder where the SmallDevops script has been executed, NOT in the folder
                in the "-dir" option
        ex: -output=/absolute/path/folder/
            -output=/relative/path/data.js
            -output=/relative/path/data.random_ext
            -output=data.output

    "-nooutput" : doesn't create an output file
        ex: -nooutput

    "-template" : use the corresponding template, require -path_template
        ex: -template=pytest_timing_git

    "-path_template" : fetch the corresponding template, require -template
        ex: -path_external_template=/absolute/path/to/template
```

---

## **Features**

- Lots of options for customisation.
- Great looking graph and informations.
- Self-sufficient, doesn't require node.js or any specific python library.
- Doesn't modify your project in any way, doesn't require special file or line to be added to your project.
- graph showing amount of test failed on the entire lifetime of a project.
- graph showing the time it take to execute your program on the entire lifetime of a project.
- Can be used to simply get json file from a set of tests.
- Can be easily modified to suit a server and an ajax request.
- You can easily add your own "test class" (let's say you use something else than unittest or pytest, you can easily create a class template for your specific test class).
- Quick (1000+ entry data doesn't slow down the site), js file is around 1Mb~ for 550 entry (=550 commits).

---

## Issues

- Work on latest Firefox, didn't test on chrome, opera or IE.
- Work on ubuntu, didn't test on other distro or windows. The biggest problem that could arise would be the time function and the stdout not being recognized.
- Only support unittest by default for now.

---

## **Specification & why**

This project use : [Bootstrap](https://getbootstrap.com/), [chartjs](https://www.chartjs.org/), [jquery](https://jquery.com/), [luxon](https://moment.github.io/luxon/) as javascript library.

I wish to work in devops so this project was interesting to make. It also highlighted many problems in devops (how to make sure the programs is running correctly, which data to recover, ..).

If possible I will improve this project for including pytest and other test suite. I could also improve the data recovered.

---

## **How to build the package**

Use `python setup.py sdist bdist_wheel` (change to python3.7 or whatever you want).
Don't forget to check with twine afterward.