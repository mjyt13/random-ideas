using System;
class Program
{
    static void Main(string[] args)
    {
        // Ввод количества касс
        Console.Write("Введите количество касс: ");
        int numberOfCashiers = int.Parse(Console.ReadLine());
        // Ввод времени обработки заказа
        Console.Write("Введите время обработки заказа (в минутах): ");
        double processingTime = double.Parse(Console.ReadLine());
        // Ввод среднего времени появления следующего покупателя
        Console.Write("Введите среднее время появления следующего покупателя (в минутах): ");
        double averageArrivalTime = double.Parse(Console.ReadLine());
        // Ввод количества итераций (длительность моделирования в минутах)
        Console.Write("Введите количество итераций (моделируемое время в минутах): ");
        double totalSimulationTime = double.Parse(Console.ReadLine());
        var results = SimulateCheckout(numberOfCashiers, processingTime, averageArrivalTime,
totalSimulationTime);
        // Вывод результатов
        Console.WriteLine("\nСреднее количество обслуженных клиентов на каждую кассу:");
        for (int i = 0; i < numberOfCashiers; i++)
        {
            Console.WriteLine($"Касса {i + 1}: {results.Item1[i]:F7}");
        }
        Console.WriteLine($"Количество потерянных клиентов: {results.Item2}");
    }
    static (double[], double) SimulateCheckout(int nCashiers, double processingTime, double
avgInterarrivalTime, double totalSimulationTime)
    {
        int[] serviced = new int[nCashiers];  // Количество обслуженных клиентов на каждой кассе
        int lostCustomers = 0;  // Количество потерянных клиентов
        double[] cashierAvailableAt = new double[nCashiers];  // Когда каждая касса будет свободна
        double currentTime = 0;  // Текущее время симуляции
        double nextCustomerArrival = GenerateExponentialRandom(avgInterarrivalTime);  // Первое время появления покупателя

        double daysNumber = 1500;
        for(int j = 0; j < daysNumber; j++)
        {
            currentTime = 0;
            while (currentTime < totalSimulationTime)
            {
                // Если следующий клиент приходит после завершения текущей симуляции
                if (nextCustomerArrival > totalSimulationTime)
                    break;
                // Поиск доступной кассы
                int? availableCashier = null;
                for (int i = 0; i < nCashiers; i++)
                {
                    if (cashierAvailableAt[i] <= nextCustomerArrival)
                    {
                        availableCashier = i;
                        break;
                    }
                }
                // Обработка клиента
                if (availableCashier.HasValue)
                {
                    serviced[availableCashier.Value]++;  // Увеличиваем счетчик обслуженных клиентов
                    cashierAvailableAt[availableCashier.Value] = nextCustomerArrival + processingTime; //Обновляем время, когда касса освободится
                }
                else
                {
                    lostCustomers++;  // Клиент уходит, если все кассы заняты
                }
                // Обновляем текущее время до времени прихода следующего клиента
                currentTime = nextCustomerArrival;
                // Генерируем время прихода следующего покупателя
                nextCustomerArrival += GenerateExponentialRandom(avgInterarrivalTime);
            }
        }

        // Подсчет средних значений для каждой кассы
        double[] averageServiced = new double[nCashiers];
        for (int i = 0; i < nCashiers; i++)
        {
            averageServiced[i] = (double)serviced[i]/daysNumber;
        }
        double avgLostCustomers = (double)lostCustomers/daysNumber; 
        return (averageServiced, avgLostCustomers);
    }
    // Генерация случайного времени по экспоненциальному закону
    static double GenerateExponentialRandom(double a)
    {
        Random rand = new();
        double u = rand.NextDouble();
        return -Math.Log(1 - u) * a;
    }
}
