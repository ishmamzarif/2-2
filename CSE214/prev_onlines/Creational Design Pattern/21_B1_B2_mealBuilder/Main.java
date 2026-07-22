import java.util.Scanner;

// ==========================================
// 1. Product Class (Final Meal)
// ==========================================
class Meal {
    private String starter;
    private String mainDish;
    private String dessert;

    public void setStarter(String starter) {
        this.starter = starter;
    }

    public void setMainDish(String mainDish) {
        this.mainDish = mainDish;
    }

    public void setDessert(String dessert) {
        this.dessert = dessert;
    }

    public void showMeal() {
        System.out.println("--- Meal Description ---");
        System.out.println("Starter   : " + starter);
        System.out.println("Main Dish : " + mainDish);
        System.out.println("Dessert   : " + dessert);
        System.out.println("------------------------");
    }
}

// ==========================================
// 2. Abstract Builder Interface
// ==========================================
interface MealBuilder {
    void buildStarter();
    void buildMainDish();
    void buildDessert();
    Meal getMeal();
}

// ==========================================
// 3. Concrete Builders
// ==========================================
class BengaliMealBuilder implements MealBuilder {
    private Meal meal = new Meal();

    @Override
    public void buildStarter() {
        meal.setStarter("Vegetable");
    }

    @Override
    public void buildMainDish() {
        meal.setMainDish("Chicken Curry");
    }

    @Override
    public void buildDessert() {
        meal.setDessert("Sweet Curd");
    }

    @Override
    public Meal getMeal() {
        return this.meal;
    }
}

class ChineseMealBuilder implements MealBuilder {
    private Meal meal = new Meal();

    @Override
    public void buildStarter() {
        meal.setStarter("Soup");
    }

    @Override
    public void buildMainDish() {
        meal.setMainDish("Peking Duck");
    }

    @Override
    public void buildDessert() {
        meal.setDessert("Pudding");
    }

    @Override
    public Meal getMeal() {
        return this.meal;
    }
}

// ==========================================
// 4. Director
// ==========================================
class Director {
    public Meal construct(MealBuilder builder) {
        builder.buildStarter();
        builder.buildMainDish();
        builder.buildDessert();
        return builder.getMeal();
    }
}

// ==========================================
// 5. Main Class (User Selection)
// ==========================================
public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.println("Select preferred meal type:");
        System.out.println("1. Bengali Meal");
        System.out.println("2. Chinese Meal");
        System.out.print("Enter choice (1 or 2): ");

        int choice = scanner.nextInt();
        MealBuilder builder = null;

        if (choice == 1) {
            builder = new BengaliMealBuilder();
        } else if (choice == 2) {
            builder = new ChineseMealBuilder();
        } else {
            System.out.println("Invalid selection.");
            scanner.close();
            return;
        }

        Director director = new Director();
        Meal myMeal = director.construct(builder);
        myMeal.showMeal();

        scanner.close();
    }
}
