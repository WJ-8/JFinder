# JFinder
implementation of JFinder
## data preparation
We take the CWE dataset as an example and put the dataset into `./data/raw directory`
We operate on`./process` via pyCharm and IDEA .
### slice dataset
```console
run slice_dataset.py
```
### build ast
```console
on IDEA
run GenerateAST/Main.java
run build_ast.py
```
### build cfg&dfg
```console
run build_cfgdfg.py
```
### build y
```console
run bulid_y.py
```
### build css
```console
run css_slice.py
run specialword.py
run build_css.py
```
### split dataset
```console
run slice.py
```
## train
```console
run train.py
```
