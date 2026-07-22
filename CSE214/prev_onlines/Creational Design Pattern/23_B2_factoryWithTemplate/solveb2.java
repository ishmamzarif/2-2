interface Report {
    void open();
    Report generate();
}

class Word implements Report {
    Word() {
        System.out.println("Word created");
    }
    public void open() {
        System.out.println("Word opened");
    }
    public Report generate() {
        System.out.println("Word generated");
        return this;
    }
}

class HTML implements Report {
    HTML() {
        System.out.println("HTML Created");
    }
    public void open() {
        System.out.println("HTML opened");
    }
    public Report generate() {
        System.out.println("HTML generated");
        return this;
    }

}

class Pdf implements Report {
    Pdf() {
        System.out.println("PDF created");
    }
    public void open() {
        System.out.println("PDF Opened");
    }
    public Report generate() {
        System.out.println("pdf generated");
        return this;
    }

}
 
abstract class ReportProcessor {
    public abstract Report createReport();
    public final void ProcessReport() {
        Report r = createReport();
        r.open();
        r.generate();
        System.out.println("Report Processing compelted");
    }
}

class WordProcessor extends ReportProcessor {
    public Report createReport() {
        return new Word();
    }
}

class PdfProcessor extends ReportProcessor {
    public Report createReport() {
        return new Pdf();
    }
}

class HTMLProcessor extends ReportProcessor {
    public Report createReport() {
        return new HTML();
    }
}

public class solveb2 {
    public static void main(String[] args) {
        WordProcessor wp =  new WordProcessor();
        wp.ProcessReport();
        HTMLProcessor hp = new HTMLProcessor();
        hp.ProcessReport();
        PdfProcessor pp = new PdfProcessor();
        pp.ProcessReport();
    }
}