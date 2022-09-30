# task

mini program to handle tasks written in python

# todo
	- db port to sqlite3
	- add help
	- colorized output?
    - add project, and show by project, and list projects


# instalation

just need to run following line
```
>> python3 -m pip install git+https://github.com/venomega/task
```

Config file is located on `$HOME/.task.json`. No need to create it


# usage

## first run

```
>> python3 -m task
  #  |    id   | Note
```

## add new entries
```
>> python3 -m task add needs to make some delivery
>> python3 -m task add look some random info later
```

## show current entries
```
>> python3 -m task
  #  |    id   | Note
  1  |  197429 | needs to make some delivery
  2  |  493525 | look some random info later
```

## mark as done some entry
```
>> python3 -m task done 197429
```

## remove some entry
```
>> python3 -m task del 493525
```

## show unfinished & finished tasks
```
>> python3 -m task show all
  1  |  197429 | needs to make some delivery
```
