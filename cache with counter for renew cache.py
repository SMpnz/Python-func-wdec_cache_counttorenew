import functools
def cacheN(iter=1):
    """Кэширует предыдущие вызовы функции указанное в iter кол-во раз"""
    def cache(func):
        """Кэширует предыдущие вызовы функции"""
        @functools.wraps(func) #возвращает на место свойства основной функции
        def wrapper_cache(*args, **kwargs):
            #сохраняем аргументы функции для идентификации в словаре кеша
            cache_key = args + tuple(kwargs.items())
            #конвертируем tuple в list для использония 
            counter_key = 'counter '+ str(cache_key)
            if  (counter_key) not in wrapper_cache.cache:
                #str(list(cache_key)) для красивого отображения параметров функции
                #следующий print - служебная информация, при использовании - убрать
                print ("Присвоили счетчик 0. Ключ запуска функции: " 
                + func.__name__  + str(list(cache_key)))

                wrapper_cache.cache.update({counter_key: 0 })
            if (cache_key not in wrapper_cache.cache 
                or wrapper_cache.cache[counter_key]  >= iter):
                #проверка на количество запусков функции 
                #с предельным числом хранения в кеше
                if wrapper_cache.cache[counter_key]  >= iter:
                    #следующий print - служебная информация, при использовании - убрать
                    print("Кеш устарел, вычисляем заново. Ключ запуска функции: " 
                    + func.__name__ + str(list(cache_key)))

                    wrapper_cache.cache[counter_key]  = 0
                wrapper_cache.cache[cache_key] = func(*args, **kwargs)        
            wrapper_cache.cache[counter_key]  += 1

            #следующий print - служебная информация, при использовании - убрать
            print("Увеличили счетчик на 1. Ключ запуска функции: "
            + func.__name__+ str(list(cache_key)) 
            + " Значение счетчика: " + str(wrapper_cache.cache[counter_key]))  

            return wrapper_cache.cache[cache_key]
        wrapper_cache.cache = dict()
        return wrapper_cache
    return cache


def main():
    @cacheN(4)
    def heavy(num=0, num2=0, str_arg='3-й аргумент'):
        print('Сложные вычисления при первом запуске функции: ' 
        + str(num) + ' ' + str(num2) + ' и ' + str_arg)
        return "Результат: "+ str(num + num2) + ' и ' + str_arg

    for i in range(1,7):
        print(heavy(1,1))
        print(heavy(1))
        print(heavy(2,1))
        print(heavy())

    @cacheN(5)
    def heavy_second():
        print('Сложные вычисления при первом запуске функции')
        return "Результат"

    for i in range(1,7):
        print(heavy_second())

        
if __name__ == "__main__":
    main()        