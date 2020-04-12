![banner](https://github.com/lstil/pyhera/raw/master/banner.jpg)

![license](https://img.shields.io/github/license/lstil/pyhera) ![issues](https://img.shields.io/github/issues/lstil/pyhera)
# pyhera

## Introduction
>**pyhera** is a lightweight in-memory database management module written in python. An optimized NoSQL database which is fast. Data are stored in JSON format (key-value) thus created databases can be analyzed by other applications in different platforms.

## Features
* Ease of use. **No complicated syntax**
* Fast because of **multithreading implementation**
* It's secure. **Database is not modifiable from outside** 
* Reliable. **pyhera automatically takes back-up**
* Capable of **handling data in any scale** (As long as the hardware allows)

## Easy Installition
```
pip install pyhera
```

## Quick start
A very basic instance:
```python
import pyhera # Import pyhera module

h = pyhera.Pool('mydb') # Create database object

h.set('foo', 'bar') 
result = h.get('foo') 

print(result) # Print 'bar'
```
To use it in temp mode:
```python
import pyhera

t = pyhera.Pool('mydb', temp=True) # Create temp database object

h.lmls('foo', [1, 2, 3]) # Won't be saved in database file
result = h.lret('foo') # Only stored in memory

print(result) # Print '[1, 2, 3]'
```
## Code samples
To compare X and pyhera:
```python
#X (a key-value series database)

r = connection()

r.dset('foo', 'bar1', 1)
r.dset('foo', 'bar2', 2)
r.dset('foo', 'bar3', 3)
d1 = r.dget('foo', 'bar1')
d2 = r.dget('foo', 'bar2')
d3 = r.dget('foo', 'bar3')

print(d1 + d2 + d3) # 6

#pyhera (Above method is also possible in pyhera)

h = pyhera.Pool('mydb')

h.dmls('foo', {
  'bar1': 1,
  'bar2': 2,
  'bar3': 3
})

d, sum = h.dmlg('foo'), 0
for k, v in d.items():
  sum += v
 
print(sum) # 6
```
## Documentation
> Documentation of pyhera project will be released as soon as possible. 
