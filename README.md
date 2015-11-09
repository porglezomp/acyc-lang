# Acyc
[![Build status](https://travis-ci.org/porglezomp/acyc-lang.svg?branch=master)](https://travis-ci.org/porglezomp/acyc-lang)

An experimental reference counted strict functional language

## Dependencies
Requires the LLVM C libraries. On linux, they can probably be installed with
```
$ sudo apt-get install llvm-3.3-dev
```
It also depends on llvmpy, which you can get with
```
$ sudo pip install llvmpy
```
You may have to create a symlink for `llvm-config` before llvmpy will install successfully.
I had to run
```
$ sudo ln -s /usr/bin/llvm-config-3.3 /usr/bin/llvm-config
```

Unit tests require nosetests. Install nose with
```
$ sudo pip install nose
```
