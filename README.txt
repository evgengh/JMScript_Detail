JMScript_Detail - программа для работы с файлами скриптов Apache Jmeter.
Данное приложение позволяет собирать и группировать данные форм (сэмплеров),
а также изменять значение параметров форм для всей группы, где встречается нужный 
параметер формы.

Требования: python 3.4 и выше.
Ограничения: - некоторые разрешения экранов (проблемы отрисовки формы наблюдались на 14" на windows 10) 
             - При указание пути к рабочему каталогу в windows использовать прямой слеш "/", python не распознает обратные слеши в пути до каталога. 
             - Внимание!!! При запуске приложения на другом дистрибутиве linux появилась ошибка при работе с пакетом tix из tkinter.
             - Сам пакет стандартно есть в tkinter, он импортируется нормально, а tkinter тоже является стандартным пакетом в python.
               Это баг самого tix.
               Для raspbian (debian) исправилось так:
               sudo apt-get install tix-dev.
               Под windows 10 запустилось корректно. 

Что нового в этой версии?!
    1. Обнаружено что приложение некорректно работает с типами элементов сторонних плагинов (например, загруженных через jmeter plugins).
    Таким образом был изменен механизм работы с элементами xml-дерева. Добавлен каталог с энумерациями стандартных элементов elemsOfType,
    где перечислены классические классы элементов jmeter (используемые в приложении). При наличии в сценарии дополнительных элементов,
    необходимо прописать новые классы в соответствующую энумерацию (например ExtraUltimateThreadGroup = 'kg.apc.jmeter.threads.UltimateThreadGroup').
    Названия класса (testclass=) берется из самого xml, например:
    <kg.apc.jmeter.threads.UltimateThreadGroup guiclass="kg.apc.jmeter.threads.UltimateThreadGroupGui" testclass="kg.apc.jmeter.threads.UltimateThreadGroup" testname="New Threads" enabled="false">

Предыдущие доработки!
    1. Присутствует кнопка _to_be_developed_ - функционал еще не реализован, при нажатии попросить файл out.csv.
    2. Добавлена индикация изменения элементов структуры хранения параметров, полученной из xml-дерева. Данный функционал добавлен
    в целях удобства работы с элементами. См. п. 10.2.
    3. Существенно повышена надежность приложения при работе (отображении и редактировании) с элементами (раб. коллекц.). Теперь выкидывание
    из приложения при нарушениях логики работы с приложением, либо случайных действиях пользователя происходить не должно. Хотя возможно - что-то было 
    пропущено/не попало в тесты.


Недавние доработки и пояснения:
    1. Добавлена возможность получения статистики по изменяемости (волатильности) параметров. См п. 9.1.
    Есть еще некоторые планы по новым фичам в приложении в последующих релизах. А также расширенное тестирования, наверняка есть что фиксить. 
    2. Данная версия - рабочая бета-версия для стандартных форматов jmx-файлов (hashTree, в старой версии используется node). 
    При работе с нестандартными версиями jmx нужно использовать другую версию приложения (будет выложена в отдельную ветку на github).
    --Выложено отдельным файлом в ветку _old_jmx_, т.е. код брать из основной ветки и заменить файл JMScript_Detail для старой.
    3. Добавлены параметры настройки префиксов и разделителя. См. п.1.
    4. Добавлена скозная нумерация сэмплеров в разрезе контроллера, тредгруппы, тестплана.*
    5. Добавлена возможность усечения названий сэмплеров. Т.е. если название произведено от ссылки, то отбросится вся часть
    до крайнего правого "/" (включительно).*
    6. Появилась возможность при восстановлении оригинальных названий сэмплеров сохранить преобразованные в выходном JMX-файле.*
    Тут уже все зависит от предпочтений в конкретной реализации тестового сценария. Т.е. как jmeter будет считать статистику
    по сэмплерам. Если сделать скозную нумерацию в разрезе тестплана, то все сэмплеры во всех тредгруппах будут уникальны.
    И соответсвенно в итоговом отчете, например, среднее время отклика будет высчитано для каждого сэмплера, не смотрю на то, 
    что есть абсолютно одинаковые сэмлеры даже в одном контроллере.
    Здесь нужно внимательно выставлять эти признаки, ну или восстановить оригинальные названия сэмплеров.
    Хотя jmeter и так должен пронумеровать все после генерации сэмплеров.
    Тут нету рекомендаций по работе с праметрами, все зависит от контекста самого теста. Например, две транзакции перехода на главную 
    страницу в тесте обычно считаются как одна операция, выполненная два раза. В тоже время в jmeter две операции, например, 
    http://host1.org/path1/fetch?numRows=all и http://host1.org/path1/fetch?numRows=topTen видимо будут расценены как одна и та же операция,
    если названия совпадают. Но тут больше похоже на то, что есть две кнопки на странице, которые вызызают один и тот же сервис, но время 
    работы сервиса может существенно отличаться для верхних 10 строк и всех строк, и в свою очередь подразумевается, что не каждой роли
    необходимы все строки из выборки. Т.е. две разные операции с точки зренения бизнес-логики. 
    7. Замечена особенность, что на 14" ноутбуке windows 10 немного свободно интерпретирует масштаб отрисовки окон и элементов приложения, 
    что бесследно исчезает ряд с кнопками (а именно Запись в файл и Обновление дерева). На 14" linux не тестировалось, но судя по запуску 
    на одном и том же ноутбуке на разных ОС, linux ведет себя скромнее с размерами элемнтов приложения. 


Краткая инструкция:
    
    1. Необходимо указать в переменной setClassDir класса JMScript_Detail актуальный
    путь к каталогу, где находится данный класс. Также, по желанию, можно изменить символы префикса
    и разделителя перед цифрой (номера элемента), которые добавляются при формировании уникальных имен.
    Важно! Нельзя указывать символ % - он используется для заполнения пробелов в файле дампов.
    
    2. Далее следует перейти в каталог, где лежит данный класс, и запустить приложение 
    инструкцией вида: python runJMScriptDetail.py.
    
    3. В форме необходимо указать путь к каталогу, где находится xml-файл со скриптом (*.jmx)
    
    4. Далее необходимо собрать файлы *.jmx, должен появится список таких файлов.
    
    5. Необходимо указать в поле нужный файл (из списка) для параметризации (можно двойным кликом по файлу из списка).
    
    6. Далее необходимо загрузить (получить) дерево из указанного файла. (При выполнении данного действия можно выбрать опцию*).
    
    7. Нужно указать файл (произвольное название) для сохранения дерева с уникальными названиями 
    ThreadGroup и контроллеров.**
     
    8. Сгенерировать коллекцию с уникальными именами. (При выполнении данного действия можно выбрать опцию*).
    
    9. Выбрать ThreadGroup и аккумулировать рабочую коллекцию.
    
    9.1. После того как рабочая коллекция создана, можно получить статистику волатильности парамтеров, т.е. вывести список волатильных (неволатильных) параметров.
    (См. панель в левом верхнем углу формы). Волатильность параметра означает, что его значение меняется для нескольких/всех сэмплеров. Например, такие параметры,
    как sessionId скорее всего будут неволатильными, поскольку при работе в одной сессии этот id будет передаваться в каждом запросе. Другое дело, - например, 
    в приложении с рест сервисами могут идти запросы на один и тот же url, но с параметром eventName и разными json, соответсвенно. Т.е. это уже разные запросы, 
    которые вызывает разные методы в приложении, но с одинаковым url.
    Данная функциональность добавлена для того, чтобы можно было применять разный подход при работе с параметрами. Неволатильные параметры удобно менять сразу
    всем скопом, выставив одно значения для всех, в то время, как волатильные требуют рассмотрения и анализа каждого параметра.
    Параметры выводятся отсортированными по значимости: неволатильные - по числу сэмплеров, где встречается этот параметр (мощность параметра);
    волатильные - учитывают коэффиент волатильности и мощность параметра, т.е. более важный параметр, который имеет 4 уникальных значения и встречается в 9 сэмплерах, 
    против параметра, который встречается в 2 сэмплерах с разными значениями. Хотя коеффициент волатильности у второго 1 (100%). 
    
    9.2. Важно! При завершении работы с ThreadGroup обязательно нужно обновить дерево, иначе при переходе к следующей ThreadGroup
    потрутся измениния в предыдущей. Также перед сохранением в файл (после редактирования всех ThreadGroup) необходимо обновить дерево.
    
    10.Далее можно работать с основной (рабочей) коллекцией.

    10.1. Есть возможность автовыбора значения из списка элементов, чекбокс Авто выбор/Все знач. позволяет автозаполнять поля для операций 
    с элементами коллекции. Для этого нужно выбрать этот чексбокс и чекбокс элемента, при нажатии кнопки операции значение подтягивается.
    Внимание! В режиме работы правки элементов данный чексбокс служит для выбора всех элементов или отмены выбора. 
    Т.е. если выполнить операцию Все значения по ключу, то из этого списка ничего не будет подтягиваться, поскольку в данном списке отмечаются элементы для изменения.
    Чтобы не запутаться - в списках, где присутствуют значения элементов, автовыбор работать не будет, для остальных работает.
    Также если, например, в списке указаны только контроллеры, который не подходит для автозаполнения, то при автозаполнении просто подтянется ключ для этих котроллеров.

    10.2. В структуре каждому листовому элементу (значению параметра) добавлен признак редактирования. Таким образом после правки элементов и обновления списка в основном окне
    измененные элементы выделяются цветом: а) для листовых элементов вида <Ключ>-<Контроллер>-<Сэмплер> - красным; б) для узловых элементов 
    если не все его листовые подэлементы отредактированы - зеленым, а если все - красным. 
    Внимание! При переключение на другую ТредГруппу все признаки сбросятся, и все элементы будут черными. Поэтому при переключении между ТредГруппами и возвращению 
    к редактированию в прежней ТредГруппе данный функционал будет неэффективен. Напоминание, что необходимо обновлять дерево перед переключением ТредГруппы.      
    
    11.При работе с основной коллекцией обновление элементов списка 
    (отмечены чекбоксами в окне) доступно только в двух режимах: 
    "Все знач. по задан. ключу" и "Значен. для кл.-кнтр.-смпл."
    
    12.После того, как все изменения внесены (можно вносить многократно),
    необходимо обновить xml-дерево.
    
    13.Чтобы сохранить измененное дерево с уникальными именами (см. шаг 7),необходимо 
    записать изменения в файл.
    
    14.Чтобы измененное дерево сохранить с оригинальными названиями необходимо указать 
    файл с восстановленными элементами и нажать восстановление оригинальных имен.
    Т.е. нужно указать выходной файл (произвольно, *.jmx, чтобы потом можно было открыть в Jmeter),
    в последствии приложение вернет оригинальные названия котроллеров и ThreadGroup. (При выполнении данного действия можно выбрать опцию*).
    
    15.Чтобы начать цикл заново нужно заново получить дерево из указанного файла (см. шаг 6).    

-------
*Как это работает (этот пункт для основого текста README) -
 a) - признак Сократ. Url в назв... выставляется перед операцией Получить дерево... Так как выполнится процедура усечения названий
      в дереве и следующая логическая операция все запишет в файл с уникальными названиями;
 b) - признак Скозн. нумерац... выставляется перед операцией Сген. колл... На данном этапе происходит обработка дерева на предмет
      одинаковых элементов внутри одного логического блока (например, одинаковых контроллеров внутри другого контроллера). Выбирается
      сущность, в рамках который пронумеруются сэмплеры;
 c) - признак Не восст. ориг... выставляется перед операцией Восст. ориг. имена. Таким образом можно сохранить производные названия
      сэмплеров (!!!котроллеры и тредгруппы при этом вернут прежние названия) в выходном чистовом файле. Если таковой будет генерироваться 
	  в итоге, т.е. важны названия элементов в загружаемом JMX-файле.
** Jmeter может работать с одинаковыми названиями и котроллеров и групп, чтобы идентифицировать параметр необходимо уникальное название контроллера,
такой механизм предусмотрен в приложении. Для удобства работы можно открыть сгенерированный файл с уникальными названиями в jmeter.
