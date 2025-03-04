# ODW solution repo

This directory contains encrypted solutions to the quizzes and challenges on this repo.
To be able to see the solutions, you need a secret key.
With it, run the following command to produce all solutions.

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

