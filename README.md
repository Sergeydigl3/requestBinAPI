# RequestBinAPI
> Lib for parsing https://requestb.in/

## Example
```sh
import requestBinAPI

reader=requestBinAPI.Request('https://requestb.in/****?inspect')
reader.check(save_result=True)

def prog(before, after, new):
    print(new)

reader.on_update(fn=prog)
reader.polling(none_stop=True, delay=5)
```

## Installation from PYPI
> pip install requestBinAPI (pip3 install requestBinAPI)

## Installation from GitHub
> pip install git+https://github.com/Sergeydigl3/requestBinAPI.git