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

Разработка поддерживается исследовательским центром «Сильный искусственный интеллект в промышленности» Университета ИТМО.

<img src='https://gitlab.actcognitive.org/itmo-sai-code/organ/-/raw/main/docs/AIM-Strong_Sign_Norm-01_Colors.svg' width='200'>

## Документация

Документация компонента доступна [здесь](https://evoguess-ai.readthedocs.io/) и включает в себя инструкцию по установке и руководство по использованию.
