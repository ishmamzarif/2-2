import java.util.Scanner;

// ==========================================
// 1. Abstract Products
// ==========================================
interface Letter {
    String getContent();
}

interface Resume {
    String getContent();
}

// ==========================================
// 2. Concrete Products
// ==========================================
class FormalLetter implements Letter {
    @Override
    public String getContent() {
        return "Formal Letter: Dear Sir/Madam, I am writing to formally request...";
    }
}

class InformalLetter implements Letter {
    @Override
    public String getContent() {
        return "Informal Letter: Hey! Just wanted to quickly catch up...";
    }
}

class FormalResume implements Resume {
    @Override
    public String getContent() {
        return "Formal Resume: Professional Experience, Education, and Certifications.";
    }
}

class InformalResume implements Resume {
    @Override
    public String getContent() {
        return "Informal Resume: A creative portfolio and summary of personal projects.";
    }
}

// ==========================================
// 3. Abstract Factory
// ==========================================
interface DocumentFactory {
    Letter createLetter();
    Resume createResume();
}

// ==========================================
// 4. Concrete Factories
// ==========================================
class FormalDocumentFactory implements DocumentFactory {
    @Override
    public Letter createLetter() {
        return new FormalLetter();
    }

    @Override
    public Resume createResume() {
        return new FormalResume();
    }
}

class InformalDocumentFactory implements DocumentFactory {
    @Override
    public Letter createLetter() {
        return new InformalLetter();
    }

    @Override
    public Resume createResume() {
        return new InformalResume();
    }
}

// ==========================================
// 5. Client Application
// ==========================================
class DocumentManager {
    private Letter letter;
    private Resume resume;
    DocumentFactory f;

    // The manager is configured with a specific factory
    public DocumentManager(DocumentFactory factory) {
        this.letter = factory.createLetter();
        this.resume = factory.createResume();
    }

    public DocumentManager(String factoryType) {
        if (factoryType.toLowerCase().equals("formal")) {
            f = new FormalDocumentFactory();
        }
        else if (factoryType.toLowerCase().equals("informal")) {
            f = new InformalDocumentFactory();
        }
        this.letter = f.createLetter();
        this.resume = f.createResume();
    }

    public void generateDocuments() {
        System.out.println("--- Generated Documents ---");
        System.out.println(letter.getContent());
        System.out.println(resume.getContent());
        System.out.println("---------------------------");
    }
}

// ==========================================
// Main Function (User Selection)
// ==========================================
public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.println("Select document mode:");
        System.out.println("1. Professional / Formal");
        System.out.println("2. Informal");
        System.out.print("Enter choice (1 or 2): ");
        
        int choice = scanner.nextInt();
        DocumentFactory factory = null;
        
        if (choice == 1) {
            factory = new FormalDocumentFactory();
        } else if (choice == 2) {
            factory = new InformalDocumentFactory();
        } else {
            System.out.println("Invalid selection.");
            System.exit(0);
        }
        
        // The client creates documents without knowing the exact concrete classes
        DocumentManager manager = new DocumentManager(factory);
        manager.generateDocuments();
        
        scanner.close();
    }
}