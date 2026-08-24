/*
 * CSE 214 - Online on Creational Pattern (Time: 30 minutes)
 *
 * You are developing a document editor that supports 3 types of file formats:
 * .docx, .pdf, and .txt. To handle each file type, you need different document
 * processors. All document processors implement an interface called
 * DocumentProcessor, which contains two methods - LoadDocument and SaveDocument
 * (For now, these may just print a message).
 *
 * Given a file name, your system has to recognize the file type and use the
 * appropriate document processor to load and save a file. The output will be
 * two messages showing that the file was loaded and saved.
 *
 * Design Pattern used: Factory Method (Simple Factory)
 */

interface DocumentProcessor {
    void loadDocument(String fileName);
    void saveDocument(String fileName);
}

class DocxProcessor implements DocumentProcessor {
    public void loadDocument(String fileName) {
        System.out.println("Loading DOCX file: " + fileName);
    }
    public void saveDocument(String fileName) {
        System.out.println("Saving DOCX file: " + fileName);
    }
}

class PdfProcessor implements DocumentProcessor {
    public void loadDocument(String fileName) {
        System.out.println("Loading PDF file: " + fileName);
    }
    public void saveDocument(String fileName) {
        System.out.println("Saving PDF file: " + fileName);
    }
}

class TxtProcessor implements DocumentProcessor {
    public void loadDocument(String fileName) {
        System.out.println("Loading TXT file: " + fileName);
    }
    public void saveDocument(String fileName) {
        System.out.println("Saving TXT file: " + fileName);
    }
}

class DocumentProcessorFactory {
    public static DocumentProcessor getProcessor(String fileName) {
        String extension = getExtension(fileName);
        switch (extension) {
            case "docx":
                return new DocxProcessor();
            case "pdf":
                return new PdfProcessor();
            case "txt":
                return new TxtProcessor();
            default:
                throw new IllegalArgumentException("Unsupported file type: " + extension);
        }
    }

    private static String getExtension(String fileName) {
        int dotIndex = fileName.lastIndexOf('.');
        if (dotIndex == -1 || dotIndex == fileName.length() - 1) {
            throw new IllegalArgumentException("File name has no valid extension: " + fileName);
        }
        return fileName.substring(dotIndex + 1).toLowerCase();
    }
}

public class DocumentEditor {
    public static void main(String[] args) {
        String fileName = "report.pdf"; // try "resume.docx" or "notes.txt" too

        DocumentProcessor processor = DocumentProcessorFactory.getProcessor(fileName);

        processor.loadDocument(fileName);
        processor.saveDocument(fileName);
    }
}
