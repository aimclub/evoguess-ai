# EvoGuessAI
[![SAI](https://github.com/ITMO-NSS-team/open-source-ops/blob/master/badges/SAI_badge_flat.svg)](https://sai.itmo.ru/)
[![ITMO](https://github.com/ITMO-NSS-team/open-source-ops/blob/master/badges/ITMO_badge_flat_rus.svg)](https://en.itmo.ru/en/)

[![license](https://img.shields.io/github/license/aimclub/evoguess-ai)](https://github.com/aimclub/evoguess-ai/blob/master/LICENSE)
[![Eng](https://img.shields.io/badge/lang-ru-yellow.svg)](/README.md)
[![Mirror](https://img.shields.io/badge/mirror-GitLab-orange)](https://gitlab.actcognitive.org/itmo-sai-code/evoguess-ai)

## Table of contents <a name="tablecontents"></a>
1. [Introduction](intro.md)
2. [Installation](installation.md)
3. [Preliminaries](theory.md)
4. [Basic usage](basic.md)
5. [Advanced usage](advanced.md)
6. [Examples](examples.md)

## Advanced usage

### Advanced parameters

EvoguessAI is affected by several parameters controlled from 
the startup script rather than from the command line.

Launching the solution in this script looks as follows:
```python
    report = solve(problem=problem,
                   runs=nof_ea_runs,
                   measure=measure,
                   seed_offset=123,
                   max_workers=workers,
                   bd_size=bds,
                   limit=lim,
                   log_path=None,
                   iter_count=3000)
```
Such parameters as `problem`, `runs`, `max_workers`, `bd_size` and 
`limit` in this fragment of the startup script are command-line 
controlled and described in [Basic usage](basic.md).

Advanced parameters are set empirically by default, 
but the user can control them directly by editing the script if needed.

List of advanced parameters:

+ `seed_offset` Initial seed for an evolutionary algorithm. 
Obviously, this parameter can influence the search for backdoors, 
but there is little possibility to change it in a meaningful way. 
In any case, in case of unsatisfactory backdoor search results, 
or for research purposes, the user can directly change this parameter 
and evaluate the resulting effect.  
**Default: 123.**


+ `log_path` Path to save the logs of EvoguessAI work. 
If the parameter is not specified explicitly, the directory 
**"./examples/logs/rho_solve/*date_time_start_date_time_finish*"**
is created for each EvoguessAI start (for example: 
**"./examples/logs/rho_solve/2024.04.10-11&#xb7;25&#xb7;
40_2024.04.10-11&#xb7;26&#xb7;22/"**). 
Information about EvoguessAI operation during a particular 
run is contained in a file named **meta.json** inside 
the created directory.  
**Default value: None.**


+ `iter_count` The number of iterations of the 
evolutionary algorithm (by iterations we mean mutations). 
This parameter directly affects the backdoor search process. 
Its increase will lead to slower backdoor search phase, 
but to more successful backdoor search, i.e. to 
finding backdoors with higher ρ-value. 
The default value was chosen empirically.  
**Default: 3000.**

[//]: # (Тут нужно добавить, что при нахождении бэкдора с одной 
хардтаской и выделения из неё юнитов, происходит перезапуск 
эволюционки \(в рамках того же "запуска"\), но число итераций 
сохраняется на все такие перезапуски.)




<sup>[&uarr;Table of contents](#tablecontents)</sup>
