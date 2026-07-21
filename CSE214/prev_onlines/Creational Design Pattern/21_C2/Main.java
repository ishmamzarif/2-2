public class Main {
    
}

interface Doc {
    public void print();
}

class FormalReport implements Doc {
    @Override
    public void print() {
        System.out.println("format report...");
    }
}

class FormalLetter implements Doc {
    @Override
    public void print() {
        System.out.println("formal letter...");
    }
}

class InformalReport implements Doc {
    @Override
    public void print() {
        System.out.println("informal report...");
    }
}

class InformalLetter implements Doc {
    @Override
    public void print() {
        System.out.println("informal letter...");
    }
}

interface Creator {
    public Doc createLetter();
    public Doc createReport();
}