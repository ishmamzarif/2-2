import java.util.Scanner;

// ==========================================
// 1. Abstract Products
// ==========================================
interface Processor {
    String getSpecs();
}

interface Display {
    String getSpecs();
}

// ==========================================
// 2. Concrete Products
// ==========================================
class IntelXeonProcessor implements Processor {
    @Override
    public String getSpecs() {
        return "Intel Xeon Processor (High Performance)";
    }
}

class ARMProcessor implements Processor {
    @Override
    public String getSpecs() {
        return "ARM Processor (Energy Efficient)";
    }
}

class IPSDisplay implements Display {
    @Override
    public String getSpecs() {
        return "IPS Display (High Color Accuracy)";
    }
}

class OLEDDisplay implements Display {
    @Override
    public String getSpecs() {
        return "OLED Display (High Contrast, Lightweight)";
    }
}

// ==========================================
// 3. Abstract Factory
// ==========================================
interface ComputerFactory {
    Processor createProcessor();
    Display createDisplay();
}

// ==========================================
// 4. Concrete Factories
// ==========================================
class WorkProFactory implements ComputerFactory {
    @Override
    public Processor createProcessor() {
        return new IntelXeonProcessor();
    }

    @Override
    public Display createDisplay() {
        return new IPSDisplay();
    }
}

class LiteMaxFactory implements ComputerFactory {
    @Override
    public Processor createProcessor() {
        return new ARMProcessor();
    }

    @Override
    public Display createDisplay() {
        return new OLEDDisplay();
    }
}

// ==========================================
// 5. Computer Class (Client)
// ==========================================
class Computer {
    private String modelName;
    private Processor processor;
    private Display display;

    // The computer is constructed by passing in the desired factory
    public Computer(String modelName, ComputerFactory factory) {
        this.modelName = modelName;
        this.processor = factory.createProcessor();
        this.display = factory.createDisplay();
    }

    public void printDescription() {
        System.out.println("--------------------------------------");
        System.out.println("Model: " + modelName);
        System.out.println("Processor: " + processor.getSpecs());
        System.out.println("Display: " + display.getSpecs());
        System.out.println("--------------------------------------");
    }
}

// ==========================================
// Main Function (User Selection)
// ==========================================
public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.println("Select your preferred model:");
        System.out.println("1. WorkPro (Professional)");
        System.out.println("2. LiteMax (Lightweight)");
        System.out.print("Enter choice (1 or 2): ");
        
        int choice = scanner.nextInt();
        
        if (choice == 1) {
            ComputerFactory workProFactory = new WorkProFactory();
            Computer myComputer = new Computer("WorkPro", workProFactory);
            myComputer.printDescription();
        } else if (choice == 2) {
            ComputerFactory liteMaxFactory = new LiteMaxFactory();
            Computer myComputer = new Computer("LiteMax", liteMaxFactory);
            myComputer.printDescription();
        } else {
            System.out.println("Invalid selection.");
        }
        
        scanner.close();
    }
}