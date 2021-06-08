import matplotlib.pyplot as plt
import random
import Erlang as Erlang
import Task
import SMO
import numpy

a = []
lam = 1
k = 2
E = Erlang.ErlangDistribution(k, lam)

# Generate a task queue with Erlang creation time and normal completion time
def GenerateQ():
    Q = []
    i = 0
    time = GenerateTime()
    while i < 10000:
        i += E.GenerateNextInternal() * 8
        t = Task.Task(i, time)
        Q.append(t)
    return Q

# Normal distribution, 10% Rxx, 10% Rxy, 30% Dx, 50% Mx
def GenerateTime():
    rnd = random.random()
    if rnd < 0.3:
        ans = random.randrange(7)  # Rxy
    elif 0.3 <= rnd < 0.6:
        ans = random.randrange(5)  # Rxx
    elif 0.6 <= rnd < 0.8:
        ans = random.randrange(3)  # Dx
    else:
        ans = random.randrange(2)  # Mx
    return ans + 40


if __name__ == "__main__":

    QuFIFO = []
    QuEDF = []
    QuRM = []

    FIFOs = []
    EDFs = []
    RMs = []

    for lam in numpy.arange(1, 20, 0.5):
        E.ChangeLambda(lam)
        temp = GenerateQ()
        QuFIFO.append(temp)

    QuRM = QuFIFO[:]
    QuEDF = QuFIFO[:]

    for i in range(len(QuFIFO)):
        FIFOs.append(SMO.FIFO(QuFIFO[i]))
        RMs.append(SMO.RM(QuRM[i]))
        EDFs.append(SMO.EDF(QuEDF[i]))

    buf1 = []
    buf2 = []
    buf3 = []

    def calculate(arr, name):
        Tw = []
        Tww = []
        Tn = []

        faults = []
        faultschange = []
        Tnchange = []
        Twchange = []
        FullWaitTime = []

        for elem in arr:
            elem.work()
            buf1 = elem.GetFaults()
            buf2 = elem.GetWaitTimes()
            buf3 = elem.GetProcessorFreeTime()
            faults.append(buf1[:])
            Tw.append(buf2[:])
            Tn.append(buf3[:])

        for elem in range(len(arr)):
            faultschange.append(faults[elem][9999])
            Tnchange.append(Tn[elem][9999])

        for o in range(len(arr)):
            time = 0
            for elem in range(10000):
                time += Tw[o][elem]
            FullWaitTime.append(time)

        for elem in range(len(arr)):
            Tww.append(FullWaitTime[elem])

        plt.plot(Tnchange, 'r')
        plt.title(name)
        plt.show()
        plt.plot(faultschange, 'g')
        plt.title(name)
        plt.show()
        plt.plot(Tww, 'k')
        plt.title(name)
        plt.show()

        buf1.clear()
        buf2.clear()
        buf3.clear()

        Tw.clear()
        Tn.clear()
        faults.clear()
        faultschange.clear()
        Tnchange.clear()
        Twchange.clear()
        Tww.clear()

    calculate(FIFOs, "FIFO")
    calculate(EDFs, "EDF")
    calculate(RMs, "RM")




