[![SAI](https://github.com/ITMO-NSS-team/open-source-ops/blob/master/badges/SAI_badge_flat.svg)](https://sai.itmo.ru/)
[![ITMO](https://github.com/ITMO-NSS-team/open-source-ops/blob/master/badges/ITMO_badge_flat_rus.svg)](https://en.itmo.ru/en/)

[![license](https://img.shields.io/github/license/aimclub/evoguess-ai)](https://github.com/aimclub/evoguess-ai/blob/master/LICENSE)
[![Eng](https://img.shields.io/badge/lang-ru-yellow.svg)](/README.md)
[![Mirror](https://camo.githubusercontent.com/9bd7b8c5b418f1364e72110a83629772729b29e8f3393b6c86bff237a6b784f6/68747470733a2f2f62616467656e2e6e65742f62616467652f6769746c61622f6d6972726f722f6f72616e67653f69636f6e3d6769746c6162)](https://gitlab.actcognitive.org/itmo-sai-code/evoguess-ai)

# EvoGuessAI

Компонент EvoGuessAI предназначен для поиска декомпозиционных множеств и оценки сложности для вариантов задач булевой выполнимости. Поиск декомпозиционных множеств осуществляется посредством оптимизации специальной псевдобулевой "black-box" функции, которая оценивает сложность декомпозиции в соответствии используемому методу декомпозиции и рассматриваемому множеству. Для оптимизации значения таких функций используются метаэвристические алгоритмы, в частности, эволюционные.

## Установка

```shell script
git clone git@gitlab.actcognitive.org:itmo-sai-code/evoguess-ai.git
cd evoguess-ai
pip install -r requirements.txt
```

Чтобы использовать EvoGuessAI в MPI режиме, также необходимо установить:

```shell script
pip install -r requirements-mpi.txt
```

### Запуск в MPI режиме

Компонент EvoGuessAI может быть запущен в MPI режиме следующим образом:

```shell script
mpiexec -n <workers> -perhost <perhost> python3 -m mpi4py.futures main.py
```

где **perhost** - это число рабочих процессов MPI на одной ноде, и **workers** - это общее число рабочих процессов MPI на всех выделенных нодах.

## Примеры использования

Пример [поиска вероятностных лазеек](https://gitlab.actcognitive.org/itmo-sai-code/evoguess-ai/-/blob/master/examples/pvs_search_example.py) для решения задачи проверки эквивалентности двух булевых схем, реализующих различные алгоритмы, на примере кодировки PvS 7x4 (Pancake vs Selection sort).

```python
root_path = WorkPath('examples')
data_path = root_path.to_path('data')
cnf_file = data_path.to_file('pvs_4_7.cnf', 'sort')
logs_path = root_path.to_path('logs', 'pvs_4_7')
solution = Optimize(
    space=RhoSubset(
        by_mask=[],
        of_size=200,
        variables=Interval(start=1, length=1213)
    ),
    instance=Instance(
        encoding=CNF(from_file=cnf_file)
    ),
    executor=ProcessExecutor(max_workers=16),
    sampling=Const(size=8192, split_into=2048),
    function=RhoFunction(
        penalty_power=2 ** 20,
        measure=Propagations(),
        solver=pysat.Glucose3()
    ),
    algorithm=Elitism(
        elites_count=2,
        population_size=6,
        mutation=Doer(),
        crossover=TwoPoint(),
        selection=Roulette(),
        min_update_size=6
    ),
    limitation=WallTime(from_string='02:00:00'),
    comparator=MinValueMaxSize(),
    logger=OptimizeLogger(logs_path),
).launch()
```

Далее соответствующая задача проверки эквивалентности двух булевых схем на примере кодировки PvS 7x4 может быть [решена c использованием найденных лазеек](https://gitlab.actcognitive.org/itmo-sai-code/evoguess-ai/-/blob/master/examples/pvs_solve_example.py) следующим образом:

```python
root_path = WorkPath('examples')
data_path = root_path.to_path('data')
cnf_file = data_path.to_file('pvs_4_7.cnf', 'sort')
logs_path = root_path.to_path('logs', 'pvs_4_7_comb')
estimation = Combine(
    instance=Instance(
        encoding=CNF(from_file=cnf_file)
    ),
    measure=SolvingTime(),
    solver=pysat.Glucose3(),
    logger=OptimizeLogger(logs_path),
    executor=ProcessExecutor(max_workers=16)
).launch(*backdoors)
```

Другие примеры можно найти в директории [examples](https://gitlab.actcognitive.org/itmo-sai-code/evoguess-ai/-/tree/master/examples) проекта.

## При поддержке

Исследование проводится при поддержке [Исследовательского центра сильного искусственного интеллекта в промышленности](<https://sai.itmo.ru/>) [Университета ИТМО](https://itmo.ru) в рамках мероприятия программы центра: Разработка и испытания экспериментального образца библиотеки алгоритмов сильного ИИ в части решения задачи выполнимости булевой формулы посредством эвристик работы с ограничениями и переменными, поиска вероятностных лазеек и инверсных полиномиальных лазеек.

## Документация

Документация компонента доступна [здесь](https://evoguess-ai.readthedocs.io/) и включает в себя инструкцию по установке и руководство по использованию.
