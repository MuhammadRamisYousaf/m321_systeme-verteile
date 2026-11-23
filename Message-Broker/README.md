# Message Broker mit RabbitMQ

Ein Producer sendet jede Sekunde eine nummerierte `Hello World`-Nachricht. Die Consumer A und B geben empfangene Nachrichten im Terminal aus.

## Nachrichtenfluss

```text
Round Robin
                                         ┌─ #1, #3 → Consumer A
Producer → gemeinsame Queue in RabbitMQ ─┤
                                         └─ #2, #4 → Consumer B

Fanout
                                    ┌─ #1, #2 → Queue A → Consumer A
Producer → RabbitMQ Fanout-Exchange ┤
                                    └─ #1, #2 → Queue B → Consumer B
```

Bei **Round Robin** teilen sich beide Consumer eine Queue. Sind beide aktiv, verteilt RabbitMQ die Nachrichten abwechselnd. Bei **Fanout** legt der Exchange eine Kopie jeder Nachricht in jede der beiden Queues.

## Starten

Im Ordner `Message-Broker` ausführen. Benötigt werden Python und ein Container-Tool.

```powershell
python -m pip install -r requirements.txt
podman machine start
podman run -d --rm --name m321-rabbitmq -p 127.0.0.1:5672:5672 docker.io/library/rabbitmq:4
```

Unter Windows setzt `podman machine start` eine eingerichtete Podman-Maschine voraus. Mit Docker Desktop stattdessen `docker run` verwenden und den Befehl für die Podman-Maschine weglassen. RabbitMQ braucht nach dem Start einen Moment.

In drei Terminals jeweils einen Befehl starten, zuerst die beiden Consumer.

| Terminal | Round Robin | Fanout |
| --- | --- | --- |
| Consumer A | `python messaging.py round-robin consumer A` | `python messaging.py fanout consumer A` |
| Consumer B | `python messaging.py round-robin consumer B` | `python messaging.py fanout consumer B` |
| Producer | `python messaging.py round-robin producer` | `python messaging.py fanout producer` |

Mit `Ctrl+C` stoppst du den jeweiligen Prozess. Stoppe vor dem Wechsel des Routing-Modells alle drei Prozesse. Wenn du fertig bist, beendest du den Broker mit `podman stop m321-rabbitmq` oder `docker stop m321-rabbitmq`.

## Leitfragen

| Versuch | Round Robin | Fanout |
| --- | --- | --- |
| Producer stoppen | Die Consumer lesen noch vorhandene Nachrichten und warten danach. | Beide Consumer leeren ihre jeweilige Queue und warten danach. |
| Beide Consumer stoppen, Producer weiterlaufen lassen | Neue Nachrichten sammeln sich in der gemeinsamen Queue. | Eine Kopie jeder neuen Nachricht sammelt sich in jeder der beiden Queues. |
| Einen oder beide Consumer wieder starten | Ein Consumer kann den Rückstau allein abarbeiten. Sind beide aktiv, teilen sie sich die Zustellung. | Jeder neu gestartete Consumer liest den Rückstau seiner eigenen Queue. Die andere Queue behält ihre Nachrichten, bis ihr Consumer wieder läuft. |

Die Beobachtungen gelten, solange RabbitMQ läuft. Die beiden Fanout-Queues werden beim Start eines beliebigen Demo-Prozesses angelegt und bleiben beim Stoppen der Consumer bestehen.

[Verteilung über eine gemeinsame Queue](https://www.rabbitmq.com/tutorials/tutorial-two-python) · [Fanout-Exchange und Bindings](https://www.rabbitmq.com/tutorials/tutorial-three-python)
