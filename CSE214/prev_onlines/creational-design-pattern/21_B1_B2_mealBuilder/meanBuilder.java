import java.util.Scanner;

// ==========================================
// 1. Product Class (Final Meal)
// ==========================================
class Meal {
    private String starter = "None";
    private String mainDish = "None";
    private String dessert = "None";

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
// 2. Abstract Builder Interface / Abstract Class
// ==========================================
abstract class MealBuilder {
    protected Meal meal = new Meal();

    public abstract void buildStarter();
    public abstract void buildMainDish();
    public abstract void buildDessert();

    // Fluent interface methods for Custom Meal creation (prevents constructor explosion)
    public MealBuilder addStarter(String starter) {
        meal.setStarter(starter);
        return this;
    }

    public MealBuilder addMainDish(String mainDish) {
        meal.setMainDish(mainDish);
        return this;
    }

    public MealBuilder addDessert(String dessert) {
        meal.setDessert(dessert);
        return this;
    }

    public Meal getMeal() {
        return this.meal;
    }
}

// ==========================================
// 3. Concrete Builders
// ==========================================
class BengaliMealBuilder extends MealBuilder {
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
}

class ChineseMealBuilder extends MealBuilder {
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
}

class CustomMealBuilder extends MealBuilder {
    @Override
    public void buildStarter() {}
    @Override
    public void buildMainDish() {}
    @Override
    public void buildDessert() {}
}

// ==========================================
// 4. Director (Handles Menu Selection Logic)
// ==========================================
class Director {
    public Meal createMeal(int choice) {
        MealBuilder builder;

        switch (choice) {
            case 1:
                builder = new BengaliMealBuilder();
                break;
            case 2:
                builder = new ChineseMealBuilder();
                break;
            default:
                System.out.println("Invalid selection.");
                return null;
        }

        builder.buildStarter();
        builder.buildMainDish();
        builder.buildDessert();
        return builder.getMeal();
    }
}

// ==========================================
// 5. Main Class
// ==========================================
public class meanBuilder {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        Director director = new Director();

        System.out.println("Select preferred meal type:");
        System.out.println("1. Bengali Meal");
        System.out.println("2. Chinese Meal");
        System.out.println("3. Custom Meal");
        System.out.print("Enter choice (1, 2, or 3): ");

        int choice = scanner.nextInt();
        scanner.nextLine(); // consume newline

        if (choice == 1 || choice == 2) {
            // Direct build handled inside Director without if-else chain in client
            Meal myMeal = director.createMeal(choice);
            if (myMeal != null) {
                myMeal.showMeal();
            }
        } else if (choice == 3) {
            // Custom Meal built fluently step-by-step without constructor explosion
            System.out.print("Enter Starter: ");
            String starter = scanner.nextLine();
            
            System.out.print("Enter Main Dish: ");
            String mainDish = scanner.nextLine();
            
            System.out.print("Enter Dessert: ");
            String dessert = scanner.nextLine();

            Meal customMeal = new CustomMealBuilder()
                    .addStarter(starter)
                    .addMainDish(mainDish)
                    .addDessert(dessert)
                    .getMeal();

            customMeal.showMeal();
        } else {
            System.out.println("Invalid selection.");
        }

        scanner.close();
    }
}