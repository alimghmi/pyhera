import json
import random
import threading
import hashlib
from re import match
from time import sleep

class pyhera(object):

    def __init__(self, name, temp, one_process):
        if not isinstance(name, str):
            self.__err__(str)

        if not isinstance(temp, bool):
            self.__err__(bool)

        self.autosave = True
        self.name = name
        self.alive = False
        self.saving = False
        self.expire = {}
        self.status = {}
        self.update = 0
        self.temp = temp
        self.one_process = one_process
        self.funcs = [self.__process__,
                      self.__protector__,
                      self.__backup__]

        self.__run__()

    def __run__(self):
        if self.alive:
            return

        self.alive = True

        if not self.temp:
            self.database = self.__load__()
            if not self.one_process:
                for func in self.funcs:
                    threading.Thread(target=func).start()
                    self.status[func] = True

        else:
            self.database = {}

        return

    def __terminate__(self):
        if not self.temp:
            self.__functor__(1)

        if not self.alive:
            return

        self.alive = False

        if not self.one_process:
            while True:
                terminated = 0
                for func in self.funcs:
                    if self.status[func] == False:
                        terminated += 1

                if terminated == len(self.funcs):
                    break

        del self.database
        return

    def __restart__(self):
        if not self.alive:
            return

        self.__terminate__()
        self.__run__()
        return

    def __lock__(self):
        if self.saving:
            self.saving = False
        else:
            self.saving = True

        return

    def __process__(self):
        if self.one_process:
            return

        while True:
            if not self.alive:
                self.status[self.__process__] = False
                break

            if self.temp:
                break

            if self.update != 0:
                while True:
                    first = self.update
                    sleep(0.1)
                    if first == self.update:
                        if not self.saving:
                            break

                self.__functor__(1)
                self.update = 0

            sleep(1)

    def __protector__(self):
        if self.one_process:
            return

        while True:
            sleep(random.randint(1, 5))

            if not self.alive:
                self.status[self.__protector__] = False
                break

            if self.temp:
                break

            if not self.autosave:
                return

            try:
                if not self.saving:
                    if self.update == 0:
                        if self.database != self.__functor__(0):
                            self.__functor__(1)
            except:
                self.__functor__(1)

    def __loadbak__(self):
        try:
            return json.loads(open("{}.hr".format(self.name), "r").read())
        except:
            return False

    def __savebak__(self):
        open("{}.hr".format(self.name), "w") \
            .write(json.dumps(self.database))

        return

    def __backup__(self):
        if self.one_process:
            return

        if self.__loadbak__() == False:
            if self.len() >= 1:
                self.__savebak__()

        while True:

            try:
                if self.len() != 0:
                    if self.__loadbak__() != self.database:
                        if self.saving != True:
                            if self.update == 0:
                                self.__lock__()
                                self.__savebak__()
                                self.__lock__()
            except:
                continue

            if not self.alive:
                self.status[self.__backup__] = False
                break

            sleep(random.randint(1, 5))

    def __save__(self):
        if not self.temp and self.autosave:
            if not self.one_process:
                self.update += 1
            else:
                self.__functor__(1)

        return

    def __load__(self):
        f = self.__functor__(0)
        if f != False:
            return f

        else:
            b = self.__loadbak__()
            if b != False:
                self.__functor__(1, b)
                return b
            else:
                self.__functor__(1, {})
                return {}

    def __functor__(self, operation, cnt=None):
        if operation == 0:
            try:
                return json.loads(open
                        (self.name, "r").read())
            except:
                return False

        else:
            try:
                if cnt == None:
                    cnt = self.database

                self.__lock__()

                open(self.name, "w").write(
                    json.dumps(cnt))

                self.__lock__()
                return True
            except:
                self.__err__(1004)

    def __sha1__(self, value):
        return hashlib.sha1(hashlib.
                            md5(str(value).encode()).
                            hexdigest().encode()).hexdigest()

    def __err__(self, ty):
        if ty == 1004:
            raise Exception("x1004: Access denied")
            exit()

        raise TypeError(str(ty))

    def __isins__(self, data, type_):
        if not isinstance(type_, list):
            self.__err__(type_)

        for t in type_:
            if isinstance(data, t):
                return True

        return False

    def mcs(self, status):
        if not isinstance(status, bool):
            self.__err__(bool)

        if self.temp:
            return False

        if status and self.autosave:
            self.autosave = False
        elif not status and not self.autosave:
            self.autosave = True
            self.__functor__(1)

        return True

    def flush(self):
        if len(self.database) != 0:
            self.database = {}
            self.__save__()

        return True

    def move(self, key, obj, duplication=True, replace=False):
        if not isinstance(key, str):
            self.__err__(str)

        if not isinstance(obj.database, dict):
            self.__err__(self)

        if self == obj:
            self.__err__(self)

        if self.exist(key):
            if not replace:
                if obj.exist(key):
                    return False

            obj.database[key] = self.database[key]
            obj.__save__()
            if not duplication:
                self.delete(key)

    def revert(self):
        return self.database

    def keys(self, regex=None):
        a = self.database.keys()
        if regex != None:
            b = []
            for i in a:
                if match(regex, i):
                    b.append(i)
            a, b = b, None

        if len(a) == 0:
            return []

        return list(a)

    def len(self):
        return len(self.keys())

    def rnd(self):
        return random.choice(self.keys())

    def exist(self, key):
        if not isinstance(key, str):
            return False

        try:
            var = self.database[key]
            return True
        except:
            return False

    def type(self, key):
        if not isinstance(key, str):
            self.__err__(str)

        if self.exist(key):
            for m in [str, int, dict, list]:
                if isinstance(self.database[key], m):
                    return m

        return False

    def ladd(self, key, data):
        if not isinstance(key, str):
            self.__err__(str)

        if not self.__isins__(data, [int, str, float]):
            self.__err__([str, int, float])

        if not self.exist(key) or not isinstance(self.database[key], list):
            self.database[key] = []

        self.database[key].append(data)
        self.__save__()
        return True

    def ldel(self, key, data):
        if not isinstance(key, str):
            self.__err__(str)

        if not self.__isins__(data, [int, str, float]):
            self.__err__([str, int, float])

        if self.type(key) == list and data in self.database[key]:
            self.database[key].remove(data)
            self.__save__()
            return True
        else:
            return False

    def lret(self, key):
        if not isinstance(key, str):
            self.__err__(str)

        if self.type(key) == list:
            return self.database[key]
        else:
            return False

    def lexist(self, key, data):
        if not isinstance(key, str):
            self.__err__(str)

        if not self.__isins__(data, [int, str, float]):
            self.__err__([str, int, float])

        if self.type(key) == list:
            if data in self.database[key]:
                return True
            else:
                return False
        else:
            return False

    def lrnd(self, key):
        if not isinstance(key, str):
            self.__err__(str)

        if self.type(key) == list:
            return random.choice(self.database[key])
        else:
            return False

    def ldindex(self, key, pos):
        if not isinstance(key, str):
            self.__err__(str)

        if not isinstance(pos, int) or pos < 1:
            self.__err__(int)

        if self.type(key) == list:
            del self.database[key][pos]
            return True
        else:
            return False

    def lindex(self, key, pos):
        if not isinstance(key, str):
            self.__err__(str)

        if not isinstance(pos, int) or pos < 1:
            self.__err__(int)

        return self.lret(key)[pos - 1]

    def lpop(self, key):
        if not isinstance(key, str):
            self.__err__(str)

        if self.type(key) == list:
            a = random.choice(self.database[key])
            self.ldel(key, a)
            return a
        else:
            return False

    def lmove(self, key, data, dst_key):
        if not isinstance(key, str):
            self.__err__(str)

        if not isinstance(dst_key, str):
            self.__err__(str)

        if not self.__isins__(data, [int, str, float]):
            self.__err__([str, int, float])

        if self.exist(key) and self.exist(dst_key):
            if self.lexist(key, data):
                if self.type(dst_key) == list:
                    self.ladd(dst_key, data)
                    self.ldel(key, data)
                    return True
        return False

    def llen(self, key):
        if not isinstance(key, str):
            self.__err__(str)

        if self.type(key) == list:
            try:
                return len(self.database[key])
            except:
                return False
        else:
            return False

    def lscan(self, key, regex):
        if not isinstance(key, str):
            self.__err__(str)

        if not isinstance(regex, str):
            self.__err__(str)

        if self.type(key) == list:
            a = []
            for i in self.lret(key):
                if match(regex, str(i)):
                    a.append(i)

            if len(a) != 0:
                return a
            else:
                return 0

        return False

    def lmls(self, key, data):
        if not isinstance(key, str):
            self.__err__(str)

        if not isinstance(data, list):
            self.__err__(list)

        if not self.exist(key) or self.type(key) == list:
            for i in data:
                if self.__isins__(i, [int, str, float]):
                    self.ladd(key, i)

            return True
        else:
            return False

    def lmld(self, key, data):
        if not isinstance(key, str):
            self.__err__(str)

        if not isinstance(data, list):
            self.__err__(list)

        for i in data:
            if self.__isins__(i, [int, str, float]):
                self.ldel(key, i)

        return True

    def ldiff(self, key, key2, bothside=False):
        if not isinstance(key, str):
            self.__err__(str)

        if not isinstance(key2, str):
            self.__err__(str)

        if not isinstance(bothside, bool):
            self.__err__(bool)

        if self.type(key) != list:
            return False

        if self.type(key2) != list:
            return False

        if self.llen(key) == 0 or self.llen(key2) == 0:
            return False

        diff = set()

        for i in self.database[key]:
            if i not in self.database[key2]:
                diff.add(i)

        if bothside:
            for i in self.database[key2]:
                if i not in self.database[key]:
                    diff.add(i)

        if len(diff) != 0:
            return list(diff)
        else:
            return 0

    def dset(self, key, key2, data, pwd=False):
        if not isinstance(key, str):
            self.__err__(str)

        if not isinstance(key2, str):
            self.__err__(str)

        if not self.__isins__(data, [int, str, float, bool]):
            self.__err__([str, int, float, bool])

        if not self.exist(key) or not isinstance(self.database[key], dict):
            self.database[key] = {}

        if key2.endswith("~~"):
            pwd = True
            key2.replace("~~", "")

        if not pwd:
            self.database[key][key2] = data
        else:
            self.database[key][key2] = self.__sha1__(data)

        self.__save__()
        return True

    def dget(self, key, key2):
        if not isinstance(key, str):
            self.__err__(str)

        if not isinstance(key2, str):
            self.__err__(str)

        if self.type(key) == dict:
            if key2 in self.database[key]:
                return self.database[key][key2]

        return False

    def ddel(self, key, key2):
        if not isinstance(key, str):
            self.__err__(str)

        if not isinstance(key2, str):
            self.__err__(str)

        if self.type(key) == dict:
            if key2 in self.database[key]:
                self.database[key].pop(key2, None)
                self.__save__()
                return True

        return False

    def dlen(self, key):
        if not isinstance(key, str):
            self.__err__(str)

        if self.type(key) == dict:
            return len(self.dkeys(key))

        return False

    def dscan(self, key, regex):
        if not isinstance(key, str):
            self.__err__(str)

        if not isinstance(regex, str):
            self.__err__(str)

        b = []
        if self.type(key) == dict:
            for a in self.dkeys(key):
                t = str(self.dget(key, a))
                if match(regex, str(t)):
                    b.append([key, a, t])

        if len(b) != 0:
            return b
        else:
            return 0

    def dkeys(self, key):
        if not isinstance(key, str):
            self.__err__(str)

        if self.type(key) == dict:
            a = list(self.database[key].keys())
            return a
        else:
            return False

    def dexist(self, key, key2):
        if not isinstance(key, str):
            self.__err__(str)

        if not isinstance(key2, str):
            self.__err__(str)

        if self.type(key) == dict:
            if key2 in self.database[key]:
                return True

        return False

    def dret(self, key):
        if not isinstance(key, str):
            self.__err__(str)

        if self.exist(key) and isinstance(self.database[key], dict):
            return self.database[key]
        else:
            return False

    def dlcr(self, key, key2, amount):
        if not isinstance(key, str):
            self.__err__(str)

        if not isinstance(key2, str):
            self.__err__(str)

        if not self.__isins__(amount, [int, float]):
            self.__err__([int, float])

        if self.dexist(key, key2):
            if self.__isins__(self.database[key][key2], [int, float]):
                self.database[key][key2] += amount
                self.__save__()
                return True

        return False

    def dmls(self, key, data):
        if not isinstance(key, str):
            self.__err__(str)

        if not isinstance(data, dict):
            self.__err__(dict)

        if not self.exist(key) or self.type(key) == dict:
            for k in data:
                if isinstance(k, str):
                    if self.__isins__(data[k], [int, str, float, bool]):
                        self.dset(key, str(k), data[k])

            return True
        return False

    def dmlg(self, key, data):
        if not isinstance(key, str):
            self.__err__(str)

        if not isinstance(data, list):
            self.__err__(list)

        result = {}
        if self.type(key) == dict:
            for item in data:
                t = self.dget(key, item)
                if t:
                    result[item] = t

            return result
        return False

    def dmld(self, key, data):
        if not isinstance(key, str):
            self.__err__(str)

        if not isinstance(data, list):
            self.__err__(list)

        if self.type(key) == dict:
            for i in data:
                self.ddel(key, i)

            return True
        return False

    def dpwd(self, key, key2, input_pwd):
        if not isinstance(key, str):
            self.__err__(str)

        if self.type(key) == dict:
            if self.dexist(key, key2):
                value = self.dget(key, key2)
                if self.__sha1__(input_pwd) == value:
                    return True

        return False

    def dwhere(self, query):
        if not isinstance(query, dict):
            self.__err__(dict)

        a = self.keys()
        b = []
        querykeys = list(query.keys())

        for key in a:
            if self.type(key) == dict:
                dkeys = self.dkeys(key)
                target = True
                for i in querykeys:
                    if not i in dkeys or query[i] != self.dget(key, i):
                        target = False
                        break

                if target:
                    b.append(key)

        return b

    def mls(self, data, replace=False):
        if not isinstance(data, dict):
            self.__err__(dict)

        for item in data:
            if self.exist(item) and not replace:
                return False

            if isinstance(data[item], tuple):
                data[item] = list(data[item])

            elif isinstance(data[item], dict):
                self.dmls(item, data[item])

            elif isinstance(data[item], list):
                self.lmls(item, data[item])

            elif self.__isins__(data[item], [str, int, float, bool]):
                self.set(item, data[item])

        return True

    def mlg(self, data):
        if not isinstance(data, list):
            self.__err__(list)

        result = {}
        for key in data:
            if self.exist(key):
                result[key] = self.database[key]

        return result

    def mld(self, data):
        if not isinstance(data, list):
            self.__err__(list)

        for key in data:
            if self.exist(key):
                self.delete(key)

        return True

    def scan(self, regex, gl=True):
        if not isinstance(regex, str):
            self.__err__(str)

        a = self.keys()
        b = []

        if not gl:
            for i in a:
                q = self.type(i)
                if q == str or q == int:
                    t = self.get(i)
                    if match(regex, str(t)):
                        b.append([i, t])
        else:
            for i in a:
                t = self.type(i)
                if t == str or t == int:
                    t = self.get(i)
                    if match(regex, str(t)):
                        b.append([i, t])

                elif t == list:
                    a = self.lscan(i, str(regex))
                    if a != 0:
                        b.append([i, a])

                else:
                    a = self.dscan(i, str(regex))
                    if a != 0:
                        for item in a:
                            b.append(item)

        if len(b) != 0:
            return b
        else:
            return 0

    def pwd(self, key, input_pwd):
        if not isinstance(key, str):
            self.__err__(str)

        if not isinstance(input_pwd, str) and not isinstance(input_pwd, int):
            self.__err__([str, int])

        if self.exist(key):
            q = self.type(key)
            value = self.get(key)
            if q == str and len(value) == 40:
                _enc = self.__sha1__(input_pwd)
                if _enc == value:
                    return True

        return False

    def set(self, key, data, pwd=False):
        if not isinstance(key, str):
            self.__err__(str)

        if not self.__isins__(data, [int, float, str, bool]):
            self.__err__([int, float, str, bool])

        if key.endswith("~~"):
            pwd = True
            key = key.replace("~~", "")

        if not pwd:
            self.database[key] = data
        else:
            self.database[key] = self.__sha1__(data)

        self.__save__()
        return True

    def setex(self, exp, key, data=None):
        if not isinstance(key, str):
            self.__err__(str)

        if not isinstance(exp, int):
            self.__err__(int)

        if key in self.expire:
            self.expire.pop(key, None)

        proc = threading.Timer(exp / 1000, self.delete, args=[key, True])
        self.expire[key] = proc

        if data != None:
            if not self.__isins__(data, [int, float, str, bool]):
                self.__err__([int, float, str, bool])

            self.database[key] = data

        proc.start()
        self.__save__()
        return True

    def persist(self, key):
        if not isinstance(key, str):
            self.__err__(str)

        if self.exist(key) and key in self.expire:
            self.expire[key].cancel()
            self.expire.pop(key, None)
            return True
        else:
            return False

    def delete(self, key, expire=False):
        if not isinstance(key, str):
            self.__err__(str)

        if self.exist(key):
            if expire and key in self.expire:
                self.expire.pop(key, None)

            self.database.pop(key, None)
            self.__save__()
            return True

        return False

    def get(self, key):
        if not isinstance(key, str):
            self.__err__(str)

        q = self.type(key)
        if q == str or q == int:
            return self.database[key]
        else:
            return False

    def rename(self, key, dst):
        if not isinstance(key, str):
            self.__err__(str)

        if not isinstance(dst, str):
            self.__err__(str)

        if self.exist(key):
            self.database[dst] = self.database[key]
            self.delete(key)
            return True
        else:
            return False

    def getset(self, key, data):
        if not isinstance(key, str):
            self.__err__(str)

        if not self.__isins__(data, [int, float, str, bool]):
            self.__err__([int, float, str, bool])

        q = self.type(key)
        if q == str or q == int:
            a = self.get(key)
            self.set(key, data)
            return a
        else:
            return False

    def getdel(self, key):
        if not isinstance(key, str):
            self.__err__(str)

        q = self.type(key)
        if q == str or q == int:
            a = self.get(key)
            self.delete(key)
            return a
        else:
            return False

    def lcr(self, key, data):
        if not isinstance(key, str):
            self.__err__(str)

        if not self.__isins__(data, [int, float]):
            self.__err__([int, float])

        if self.type(key) in [int, float]:
            self.database[key] += data
            self.__save__()
            return True
        else:
            return False

def Pool(name, temp=False, one_process=False):
    return pyhera(name, temp, one_process)
