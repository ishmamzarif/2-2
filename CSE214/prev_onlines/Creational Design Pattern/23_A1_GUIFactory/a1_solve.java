class apk{
    Theme thm;
    Button button;
    TextField textField;
    DialogBox dialogBox;
    apk(Theme th) {
        thm = th;
        button = thm.createButton();
        textField = thm.createTextField();
        dialogBox = thm.createDialogBox();
    }
    void buttonPress() {
        button.render();
    }
    void GiveTextField() {
        textField.render();
    }
    void ShowDialogBox() {
        dialogBox.render();
    }
}

interface Button {
    void render();
}

interface TextField {
    void render();
}

interface DialogBox {
    void render();
}

class DarkButton implements Button {
    public void render() {
        System.out.println("Dark button");
    }
}

class LightTextField implements TextField {
    public void render() {
        System.out.println("Ligth textfield");
    }
}

class LightDialogBox implements DialogBox {
    public void render() {
        System.out.println("Light dialogbox");
    }
}

class LightButton implements Button {
    public void render() {
        System.out.println("light button");
    }
}

class DarkTextField implements TextField {
    public void render() {
        System.out.println("Dark textfield");
    }
}

class DarkDialogBox implements DialogBox {
    public void render() {
        System.out.println("Dark dialogbox");
    }
}

interface Theme {
    Button createButton();
    TextField createTextField();
    DialogBox createDialogBox();
}

class Dark implements Theme{
    public Button createButton() {
        return new DarkButton();
    }
    public TextField createTextField() {
        return new DarkTextField();
    }
    public DialogBox createDialogBox() {
        return new DarkDialogBox();
    }
}

class Light implements Theme{
    @Override
    public Button createButton() {
        return new LightButton();
    }
    public TextField createTextField() {
        return new LightTextField();
    }
    public DialogBox createDialogBox() {
        return new LightDialogBox();
    }
}



public class a1_solve{
    public static void main(String[] args) {
        apk a1 = new apk(new Dark());
        a1.buttonPress();
        a1.ShowDialogBox();
        a1.GiveTextField();
        apk a2 = new apk(new Light());
        a2.buttonPress();
        a2.ShowDialogBox();
        a2.GiveTextField();
    }
}