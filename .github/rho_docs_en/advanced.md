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

+ `seed_offset`   
**Default: 123.**

+ `log_path`   
**Default: None.**

+ `iter_count`   
**Default: 3000.**

<sup>[&uarr;Table of contents](#tablecontents)</sup>
