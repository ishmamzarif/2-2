import java.util.ArrayList;
import java.util.List;

interface Observer {
    void update(double price);
}

class TickerTape implements Observer {
    public void update(double price) {
        System.out.println("Ticker Tape: scrolling new price " + price);
    }
}

class Graph implements Observer {
    public void update(double price) {
        System.out.println("Graph: plotting new data point " + price);
    }
}

class BuySellBot implements Observer {
    public void update(double price) {
        if (price > 100) {
            System.out.println("Buy/Sell Bot: price " + price + " triggers SELL");
        } else {
            System.out.println("Buy/Sell Bot: price " + price + " triggers BUY");
        }
    }
}

class StockData {
    private List<Observer> observers = new ArrayList<>();

    void addObserver(Observer o) {
        observers.add(o);
    }

    void removeObserver(Observer o) {
        observers.remove(o);
    }

    void setPrice(double price) {
        System.out.println("New stock price: " + price);
        for (Observer o : observers) {
            o.update(price);
        }
    }
}

public class _22C2 {
    public static void main(String[] args) {
        StockData stock = new StockData();
        Observer ticker = new TickerTape();
        Observer graph = new Graph();
        Observer bot = new BuySellBot();

        stock.addObserver(ticker);
        stock.addObserver(graph);
        stock.addObserver(bot);

        stock.setPrice(95.5);

        stock.removeObserver(graph);
        stock.setPrice(102.75);
    }
}