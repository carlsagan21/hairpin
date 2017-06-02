# env settings

python3 latest(3.6.1) 에서 동작을 확인하였습니다.  
자세한 스펙은 `cat Pipfile` 을 참고하기 바랍니다.  
terminal 에서 python3 커맨드를 사용할 수 있다면, `($PROJECT_ROOT)/main.py DNAseq.fasta` 만으로 실행됩니다.

```
usage: main.py [-h] [-v] [-t] input_file

Hairpin Finder by soo. Please Enjoy!

positional arguments:
  input_file     input file to read a DNA sequence

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  increase output verbosity
  -t, --toy      run with the given toy sequence
```

### FYI

이 프로젝트는 [`pipenv`](https://github.com/kennethreitz/pipenv) 를 사용합니다. 즉 [`Pipfile`](https://github.com/pypa/pipfile) 을 활용하고 있습니다.  
다행이도 서드파티 의존성은 없으므로 신경쓰지 않아도 되지만, 서드파티를 추가할 때는 `Pipfile` 을 활용해 주시기 바랍니다.

# how to run

```commandline
python3 main.py DNAseq.fasta
```

or just excute

```commandline
./run
```
