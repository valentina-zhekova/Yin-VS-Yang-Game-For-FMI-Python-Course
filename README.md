Игра "Yin VS Yang"

Правила:
На дъска NxN участват 2-ма играчи съответно с бели и черни пулове.
Първоначално всеки разполага с k*N пула разположени аналогично на
шахматна дъска или с по 1 пул разположени в диагонално-противоположни
ъгли. На всеки ход играч мести един от пуловете си върху свободно поле,
като има 2 възможности:
    1. стъпка "клониране" - при оказване на съседно поле се поставя
                            нов пул (първоначалния запазва позицията си)
    2. стъпка "скок" - позволено е преместване в радиус до 2 съседни полета,
                       като могат да се прескачат противниковите пулове
Под съседно поле се разбира съседно по хоризонтал, вертикал или диагонал.
Във всички случай при извършен ход, противниковите пулове съседни на
обозначеното място биват превземани (сменят принадлежността си).
Играта приключва, когато не останат свободни полета по дъската
или някой от играчите няма повече позволени ходове, в този случай
останалите свободни полета автоматично стават собственост на другия
играч. Печели, този който е заел повече територия.

Функционалност:
- Играе се срещу компютъра, като има 2 нива на сложност:
  - easy - мести на произволно поле измежду позволените
  - hard - играе по алгоритъм
- Играчът може да избира:
  - класическа дъска: размер 7х7 и всеки играч започва с по 14 пула
  - адаптирана дъска:
    - големина на дъската: 4 <= N <= 16
    - първоначален брой пулове: 1 или k*N , като 1 <= k <= (N - 2) // 2
  - дали да започне първи или втори
  - "Yin" or "Yang" (с кои пулове да играе)
- Може да се регистрират различни играчи чрез потребителско име и парола,
  като съответно в база данни се пази инфромация за брой победи, брой загуби
  при сложност easy/hard.
- Също така по време на дадена партия играча може да се отпише чрез запазване
  на текущото състояние и при последващо вписване да продължи откъдето е
  стигнал (състоянието се пази в базата)
- Може да се играе и като гост (няма право да запазва състояние)
- По всяко време може да се излезе от играта, да се започне нова
  или да се запази състоянието и да се излезе
- Преди започването на нова игра може да се провери статистика на топ 3
  играчите и състоянието на текущия играч
- Конзолен интерфейс (евентуално и графичен)
