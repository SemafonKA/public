# Zapret и поиск подходящего конфига

Для удобства поиска работающего конфига в Zapret, есть дефолтный скрипт
`blockcheck.sh`. Данный скрипт прогоняет множество возможных конфигов для
указанных пользователем доменов. Но на выходе со скрипта получается просто
большой список вида "домен - сработавший для него параметр". Для упрощения
анализа данного вывода я написал небольшой скрипт, группирующий сработавшие
параметры и сортирующий их в порядке количества сработавших параметров.

## Запуск скрипта

Скрипт советую запускать следующим образом:

```bash
sudo ./blockcheck.sh | tee blockcheck-out.txt
```

В результате исполнения такой команды будет создан файл, в который будет
записан весь вывод скрипта. Данный файл затем будет использован скриптом
анализатора.

При запуске программы, советую выбирать много разных доменов, интересующих для
разблокировки. Также, советую выполнять несколько прогонов (например, по 5)
для каждого параметра (об этом скрипт также спросит).

> [!WARNING]
> Скрипт может работать ооочень долго, скорее всего около 3-5 часов. Поэтому
> нужно запасаться терпением)

## После запуска

После завершения работы скрипта, необходимо запустить скрипт [analyze.py](./analyze.py)
(важно, чтобы файл `blockcheck-out.txt` находился в той же директории).
Результат работы скрипта будет выведен в консоль, но его также можно
перенаправить в файл следующим образом:

```bash
python analyze.py > out.txt
```

Таким образом, в файле `out.txt` будет записана информация примерно следующего
содержания:

```
********************************************
*** Parameters with  5 working hosts ***
********************************************

Params: nfqws --dpi-desync=multisplit --dpi-desync-split-pos=2 --dpi-desync-split-seqovl=336 --dpi-desync-split-seqovl-pattern=/home/semafonka/Downloads/zapret-v69.9/files/fake/tls_clienthello_iana_org.bin
  ipv:       ipv4
  conn_type: curl_test_https_tls12
  hosts: 
   - rutracker.org
   - ntc.party
   - rutor.info
   - youtube.com
   - discord.com

Params: nfqws --dpi-desync=syndata,multisplit --dpi-desync-fake-syndata=/home/semafonka/Downloads/zapret-v69.9/files/fake/tls_clienthello_iana_org.bin --dpi-desync-split-pos=1
  ipv:       ipv4
  conn_type: curl_test_https_tls12
  hosts: 
   - rutracker.org
   - ntc.party
   - rutor.info
   - youtube.com
   - discord.com

Params: tpws --split-pos=2 --oob
  ipv:       ipv4
  conn_type: curl_test_https_tls13
  hosts: 
   - rutracker.org
   - ntc.party
   - rutor.info
   - youtube.com
   - discord.com

Params: tpws --split-pos=2 --disorder
  ipv:       ipv4
  conn_type: curl_test_https_tls13
  hosts: 
   - rutracker.org
   - ntc.party
   - rutor.info
   - youtube.com
   - discord.com
...
```

Данные стратегии можно вставлять в `/opt/zapret/config`, держа в голове
следующее:

- `--filter-tcp=80` - это `curl_test_http`
- `--filter-tcp=443` - это `curl_test_http_tls1x`
- `--filter-udp=443` - это QUIC (не знаю как его определять)

Пример моего конфига приложен в [config](./config)
