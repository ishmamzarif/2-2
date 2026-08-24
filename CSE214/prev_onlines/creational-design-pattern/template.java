// Abstract Products
interface Button {
    void render();
}

interface Checkbox {
    void render();
}

// Concrete Products Family A (e.g., Mac Style)
class MacButton implements Button {
    public void render() {
        System.out.println("Mac Button");
    }
}

class MacCheckbox implements Checkbox {
    public void render() {
        System.out.println("Mac Checkbox");
    }
}

// Concrete Products Family B (e.g., Windows Style)
class WinButton implements Button {
    public void render() {
        System.out.println("Win Button");
    }
}

class WinCheckbox implements Checkbox {
    public void render() {
        System.out.println("Win Checkbox");
    }
}

// Abstract Factory Interface
interface GUIFactory {
    Button createButton();

    Checkbox createCheckbox();
}

// Concrete Factories
class MacFactory implements GUIFactory {
    public Button createButton() {
        return new MacButton();
    }

    public Checkbox createCheckbox() {
        return new MacCheckbox();
    }
}

class WinFactory implements GUIFactory {
    public Button createButton() {
        return new WinButton();
    }

    public Checkbox createCheckbox() {
        return new WinCheckbox();
    }
}

class apk {
    GUIFactory gf;
    Button bt;
    Checkbox cb;

    apk(GUIFactory g) {
        gf = g;
        bt = g.createButton();
        cb = g.createCheckbox();
    }

    void renderButton() {
        bt.render();
    }

    void renderCheckbox() {
        cb.render();
    }
}

public class template {
    public static void main(String[] args) {
        MacFactory mf = new MacFactory();
        apk a1 = new apk(mf);
        apk a2 = new apk(new WinFactory());
        a1.renderButton();
        a1.renderCheckbox();
        a2.renderButton();
        a2.renderCheckbox();
    }
}