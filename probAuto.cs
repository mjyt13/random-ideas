//метод для определения массива вероятностей перехода в состояние и выдачи выхода
private double[] FindProbability(Signal signal, State state)
{
    /* в зависимости от состояния и входного сигнала будет возвращаться массив вероятностей
    соответствующего перехода в новое состояние */

    // состояние - закрыто, сигнал - использовать пропуск
    if (state == State.Closed)
    {
        if (signal == Signal.UsePass) return new double[] { 0.1, 0.6, 0.06, 0.04, 0.15, 0.05 };
        if (signal == Signal.Timeout) return new double[] { 0.05, 0.15, 0, 0.8, 0, 0 };
        if (signal == Signal.NoPassAttempt) return new double[] { 0.11, 0, 0.09, 0.2, 0.1, 0.5 };
    }
    if (state == State.Open)
    {
        if (signal == Signal.UsePass) return new double[] { 0.11, 0.6, 0.1, 0.15, 0.05, 0.09 };
        if (signal == Signal.Timeout) return new double[] { 0.16, 0.09, 0.05, 0.45, 0.14, 0.11 };
        if (signal == Signal.NoPassAttempt) return new double[] { 0.11, 0.6, 0.09, 0.15, 0.05, 0.1 };
    }
    if (state == State.Alarm)
    {
        if (signal == Signal.UsePass) return new double[] { 0.04, 0.6, 0.09, 0.11, 0.06, 0.2 };
        if (signal == Signal.Timeout) return new double[] { 0.05, 0, 0.15, 0.3, 0, 0.5 };
        if (signal == Signal.NoPassAttempt) return new double[] { 0, 0, 0, 0.2, 0.05, 0.75 };
    }
    return new double[] { 0, 0, 0, 0, 0, 0 };
}

//метод для определения, в какое состояние должен перейти автомат и какой выход дать

private int FindOutAndCondition (double[] probabilities)
{
    //сгенерировать случайное число
    double randValue = random.NextDouble();
    // начать проходить по массиву вероятностей
    for (int i = 0; i < probabilities.Length; i++)
    {
        //инициализировать суммы для определения диапазона попадания вероятности
        double prob1 = 0;
        double prob2 = 0;
        //первая сумма - все элементы до выбранного ВКЛЮЧИТЕЛЬНО (от 0 до i все)
        for (int j = 0; j <= i; j++)
        {
            prob1 += probabilities[j];
        }
        //вторая сумма - все элементы до выбранного (полагаю, можно сказать, исключительно)
        for (int j = 0; j < i; j++)
        {
            //например, при первой итерации цикла for относительно i  эта сумма будет равняться нулю
            prob2 += probabilities[j];
        }
        //ну, и если случайное число попало в промежуток, надо понять к какой "ячейке" это будет относиться
        if (randValue <= prob1 && randValue > prob2)
        {
            return i;
        }
    }
    return -1;
 }
