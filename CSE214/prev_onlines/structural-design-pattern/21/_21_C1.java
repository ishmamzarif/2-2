import java.util.ArrayList;

import java.util.List;
import java.util.Scanner;

interface Coffee {
    public String getIngredients();
    public int getCost();
}

class BasicBlackCoffee implements Coffee {
    @Override
    public String getIngredients() {
        return "Water + Grinded Coffee Beans";
    }
    @Override
    public int getCost() {
        return 100 + 30;
    }
}

class BasicMilkCoffee implements Coffee {
    @Override
    public String getIngredients() {
        return "Milk + Grinded Coffee Beans";
    }
    @Override
    public int getCost() {
        return 100 + 50 + 30;
    }
}

abstract class CoffeeType implements Coffee {
    protected Coffee c;

    public CoffeeType(Coffee coffee) {
        this.c = coffee;
    }
    public String getIngredients() {
        return c.getIngredients();
    }
    public int getCost() {
        return c.getCost();
    }
}

class Americano extends CoffeeType {
    public Americano(Coffee c) {
        super(c);
    }
    public String getIngredients() {
        return super.getIngredients();
    }
    public int getCost() {
        return c.getCost() + 30;
    }
}

class Cappuccino extends CoffeeType {
    public Cappuccino(Coffee c) {
        super(c);
    }
    
    public String getIngredients() {
        return super.getIngredients();
    }
    public int getCost() {
        return c.getCost() + 50;
    }
}

// Order class to handle multiple coffee orders
class Order {
    private List<Coffee> coffees = new ArrayList<>();

    public void addCoffee(Coffee coffee) {
        coffees.add(coffee);
    }

    public void printOrderDetails() {
        int totalCost = 0;
        int coffeeCount = 1;
        for (Coffee coffee : coffees) {
            System.out.println("Coffee " + coffeeCount + ":");
            System.out.println("Ingredients: " + coffee.getIngredients());
            System.out.println("Cost: " + coffee.getCost() + " taka");
            System.out.println();
            totalCost += coffee.getCost();
            coffeeCount++;
        }
        System.out.println("Total Cost for Order: " + totalCost + " taka");
    }
}

// Main Class
public class _21_C1 {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        Order order = new Order();
        while (true) {
            System.out.println("Select coffee type (1: Americano, 2: Espresso, 3: Cappuccino, 4:Mocha, 0: Finish): ");
            int choice = scanner.nextInt();
            if (choice == 0) 
                break;
            Coffee coffee;
            switch (choice) {
                case 1:
                    coffee = new Americano(new BasicBlackCoffee());
                    break;
                case 3:
                    coffee = new Cappuccino(new BasicMilkCoffee());
                    break;
                default:
                    System.out.println("Invalid choice.");
                    continue;
            }
            order.addCoffee(coffee);
        }
        order.printOrderDetails();
        scanner.close();
    }
}