class Lines:
    ip: str = "ipv4"  # Ip standart (like ipv4 or ipv6)
    hosts: list[str] = []  # list of hosts (like ['google.com', 'yandex.ru', ...])
    conn_type: str = ""  # connection type (like http, https, ...)
    command_params: str = ""  # console params like nfqws --split-pos=2 --oob


def main():
    structs: dict[str, Lines] = {}

    with open("blockcheck-out.txt") as f:
        lines = f.readlines()

        # Find the begin of summary
        beginIndex = -1
        for i in range(len(lines) - 1, -1, -1):
            if lines[i].startswith("* SUMMARY"):
                beginIndex = i
                break

        if beginIndex == -1:
            print("There is no summary in file")
            return -1

        # remove unneccesary entities
        lines = lines[beginIndex + 1 :]

        for line in lines:
            if not line.strip():
                break

            splitted = line.split(" ")
            ipv = splitted[0]
            host = splitted[1]
            conn_type = splitted[2]
            command_param = " ".join(splitted[4:])
            key = ipv + conn_type + command_param

            if key in structs:
                structs[key].hosts += [host]
            else:
                lineObj = Lines()
                lineObj.ip = ipv
                lineObj.hosts = [host]
                lineObj.conn_type = conn_type
                lineObj.command_params = command_param

                structs[key] = lineObj

    # group items by its hosts.size
    max_host_size = 0
    groupedLines: dict[int, list[Lines]] = {}
    for key, line in structs.items():
        hosts_size = len(line.hosts)
        if hosts_size not in groupedLines:
            groupedLines[hosts_size] = []

        groupedLines[hosts_size] += [line]
        if hosts_size > max_host_size:
            max_host_size = hosts_size

    # Print items into terminal
    for key in range(max_host_size, -1, -1):
        if key not in groupedLines:
            continue

        lines = groupedLines[key]

        print()
        print("********************************************")
        print(f"*** Parameters with {key:2} working hosts ***")
        print("********************************************")
        print()

        for line in lines:
            print(f"Params: {line.command_params[:-1]}")
            print(f"  ipv:       {line.ip}")
            print(f"  conn_type: {line.conn_type}")
            print("  hosts: ")
            for host in line.hosts:
                print(f"   - {host}")

            print()

    return 0


if __name__ == "__main__":
    main()
