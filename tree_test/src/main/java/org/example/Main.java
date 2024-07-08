package org.example;

import java.lang.*;
import java.io.*;
import java.nio.file.*;
import com.github.gumtreediff.actions.*;
import com.github.gumtreediff.io.*;
import com.github.gumtreediff.gen.*;
import com.github.gumtreediff.matchers.*;
import com.github.gumtreediff.tree.*;
import com.github.gumtreediff.utils.*;

public class Main {
    public static String FILE_PATH = "src/main/resources/output.txt";
    public static TreeContext generateFromXML(String filepath) throws IOException {
        String content = new String(Files.readAllBytes(Paths.get(filepath)));
        return TreeIoUtils.fromXml().generateFrom().string(content);
    }
    public static void main(String[] args) {
        try {
            TreeContext ctxt = generateFromXML(FILE_PATH);
            Tree t = ctxt.getRoot();
            System.out.println(t.toTreeString());

        } catch (IOException e) {
            e.printStackTrace();
        }

    }
}