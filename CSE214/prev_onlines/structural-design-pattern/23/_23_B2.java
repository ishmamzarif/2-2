import java.util.ArrayList;
import java.util.List;

interface OrderItem {
    public int getPrice();
    public void print(String msg);
}

class Food implements OrderItem {
    private int price;
    private String name;

    public Food(String name, int price) {
        this.name = name;
        this.price = price;
    }

    @Override
    public int getPrice() {
        return this.price;
    }

    @Override
    public void print(String msg) {
        System.out.printf("%sFood: %s (£%.2f)%n", msg, name, (double) price);
    }
}

class SetMenu implements OrderItem {
    List<Food> foods = new ArrayList<>();
    private String name;

    public SetMenu(String name) {
        this.name = name;
    }

    @Override
    public int getPrice() {
        int total = 0;
        for (Food food : foods) {
            total += food.getPrice();
        }
        return total;
    }

    @Override
    public void print(String msg) {
        System.out.println(msg + "Set Menu: " + name);
        for (Food food : foods) {
            food.print(msg + "  ");
        }
    }

    public void addFood(Food food) {
        foods.add(food);
    }
}

class Grocery implements OrderItem {
    private int price;
    private String name;

    public Grocery(String name, int price) {
        this.name = name;
        this.price = price;
    }

    @Override
    public int getPrice() {
        return this.price;
    }

    @Override
    public void print(String msg) {
        System.out.printf("%sGrocery: %s (£%.2f)%n", msg, name, (double) price);
    }
}

class GroceryPackage implements OrderItem {
    List<OrderItem> groceries = new ArrayList<>();
    private String name;

    public GroceryPackage(String name) {
        this.name = name;
    }

    @Override
    public int getPrice() {
        int total = 0;
        for (OrderItem grocery : groceries) {
            total += grocery.getPrice();
        }
        return total;
    }

    @Override
    public void print(String msg) {
        System.out.println(msg + "Package: " + name);
        for (OrderItem item : groceries) {
            item.print(msg + "  ");
        }
    }

    public void add(OrderItem grocery) {
        groceries.add(grocery);
    }
}

class Order {
    private List<OrderItem> items = new ArrayList<>();

    public void add(OrderItem item) {
        items.add(item);
    }

    public double getTotalPrice() {
        double total = 0;
        for (OrderItem item : items) {
            total += item.getPrice();
        }
        return total;
    }

    public void printReceipt() {
        System.out.println("========== RECEIPT ==========");
        for (OrderItem item : items) {
            item.print("");
            System.out.println();
        }
        System.out.println("-----------------------------");
        System.out.printf("Total Bill: £%.2f%n", getTotalPrice());
    }
}

public class _23_B2 {
    public static void main(String[] args) {
        Food burger = new Food("Burger", 8);
        Food pizza = new Food("Pizza", 10);
        Food fries = new Food("French Fries", 3);
        SetMenu lunch = new SetMenu("Lunch Combo");
        lunch.addFood(burger);
        lunch.addFood(fries);
        Grocery rice = new Grocery("Rice", 20);
        Grocery oil = new Grocery("Cooking Oil", 12);
        Grocery eggs = new Grocery("Eggs", 6);
        Grocery sugar = new Grocery("Sugar", 5);
        GroceryPackage breakfastPack = new GroceryPackage("Breakfast Pack");
        breakfastPack.add(eggs);
        breakfastPack.add(sugar);
        GroceryPackage monthlyPack = new GroceryPackage("Monthly Essentials");
        monthlyPack.add(rice);
        monthlyPack.add(oil);
        monthlyPack.add(breakfastPack);
        Order order = new Order();
        order.add(pizza);
        order.add(lunch);
        order.add(rice);
        order.add(monthlyPack);
        order.printReceipt();
    }
}