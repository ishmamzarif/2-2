import java.util.ArrayList;
import java.util.List;

class Logger {
    List<String> logs = new ArrayList<>();
    // private constructor
    private Logger() {

    }

    //private singular object
    // we could also do a direct EAGER initialization here
    // in that case the if (logger == null) would not be needed
    private static Logger logger = null;

    public static Logger getInstance() {
        if (logger == null) {
            logger = new Logger();
        }
        return logger;
    }

    public void writeLog(String s) {
        logs.add(s);
    }

    public void showLog() {
        System.out.println("Showing the entire Log:");
        for (int i = 0; i < logs.size(); i++) {
            System.out.println(String.valueOf(logs.get(i)));
        }
    }
}

class Tester1 {
    public void doSomething() {
        System.out.println("Tester1 is doing something");
        Logger logger = Logger.getInstance();
        logger.writeLog("Tester1 did something");

        // printing this for removing any doubt
        System.out.println("hashCode of logger in Tester1 " + logger.hashCode());
    }
}

class Tester2 {
    public void doSomething() {
        System.out.println("Tester2 is doing something");
        Logger logger = Logger.getInstance();
        logger.writeLog("Tester2 did something");

        // printing this for removing any doubt
        System.out.println("hashCode of logger in Tester2 " + logger.hashCode());
    }
}

public class Main {
    public static void main(String[] args) {
        Tester1 t1 = new Tester1();
        t1.doSomething();
        
        Tester2 t2 = new Tester2();
        t2.doSomething();

        Logger logger = Logger.getInstance();
        logger.showLog();
    }
}

