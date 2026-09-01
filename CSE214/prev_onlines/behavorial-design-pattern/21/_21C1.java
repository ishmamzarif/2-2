import java.util.ArrayList;
import java.util.List;

interface StockObserver {
    void update(String stockName, double price);
}

class Stock {
    private String name;
    private double price;
    private List<StockObserver> observers = new ArrayList<>();

    Stock(String name, double price) {
        this.name = name;
        this.price = price;
    }

    void follow(StockObserver observer) {
        observers.add(observer);
    }

    void unfollow(StockObserver observer) {
        observers.remove(observer);
    }

    void setPrice(double price) {
        this.price = price;
        for (StockObserver o : observers) {
            o.update(name, price);
        }
    }
}

class User implements StockObserver {
    private String name;

    User(String name) {
        this.name = name;
    }

    public void update(String stockName, double price) {
        System.out.println(name + " has been notified: The price of " + stockName + " is now " + price);
    }
}

public class _21C1 {
    public static void main(String[] args) {
        Stock googleStock = new Stock("Google", 1500);
        Stock appleStock = new Stock("Apple", 1200);

        User user1 = new User("Alice");
        User user2 = new User("Bob");

        googleStock.follow(user1);
        googleStock.follow(user2);
        appleStock.follow(user1);

        System.out.println("Updating Google stock price...");
        googleStock.setPrice(1550);

        System.out.println("\nUpdating Apple stock price...");
        appleStock.setPrice(1250);

        googleStock.unfollow(user1);

        System.out.println("\nUpdating Google stock price again...");
        googleStock.setPrice(1600);
    }
}