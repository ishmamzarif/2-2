import java.util.ArrayList;
import java.util.List;

interface Observer {
    void update(String message);
}

class Commander implements Observer {
    public void update(String message) {
        System.out.println("Commander received: " + message);
    }
}

class Scouts implements Observer {
    public void update(String message) {
        System.out.println("Scouts received: " + message + " -> Dispatch riders!");
    }
}

class SupplyTeam implements Observer {
    public void update(String message) {
        System.out.println("Supply Team received: " + message + " -> Update inventory!");
    }
}

class RavenBoard {
    private List<Observer> observers = new ArrayList<>();

    void subscribe(Observer o) {
        observers.add(o);
    }

    void unsubscribe(Observer o) {
        observers.remove(o);
    }

    void postMessage(String message) {
        System.out.println("New scroll: \"" + message + "\"");
        for (Observer o : observers) {
            o.update(message);
        }
    }
}

public class _22A2 {ß
    public static void main(String[] args) {
        RavenBoard board = new RavenBoard();
        Observer commander = new Commander();
        Observer scouts = new Scouts();
        Observer supplyTeam = new SupplyTeam();

        board.subscribe(commander);
        board.subscribe(scouts);
        board.subscribe(supplyTeam);

        board.postMessage("Enemy spotted near the river");

        board.unsubscribe(scouts);
        board.postMessage("Winter supplies running low");

        board.subscribe(scouts);
        board.unsubscribe(supplyTeam);
        board.postMessage("Ships seen in the east");
    }
}