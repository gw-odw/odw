# ODW solution repo

This repository contains the encrypted solutions to the quizzes and challenges proposed at the [ODW7, 2024](https://github.com/gw-odw/odw-2024). To see the solutions, you need to be in possession of the secret key. Once you have this, you can run
```
$ gpg -d solutions.tar.gz.gpg | tar -xvzf -
```
to produce all solutions.

You can add solution in the form of text or mardown file, if they require just a few explanation sentences or lines of code. Otherwise, feel free to create and upload a Jupyter notebook. Use the same environment of the workshop to create it.

To add a new solution, or edit an existing solution. First, unpack the solutions as above. Then, run
```
$ tar -cvzf - Solutions_Tuto* | gpg -c > solutions.tar.gz.gpg
```
Then finally git add the `solutions.tar.gz.gpg` and commit in the usual way.

