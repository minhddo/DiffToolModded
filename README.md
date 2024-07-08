## Introduction
This folder aims to use the GumTree tool to generate a parse tree for an Isabelle term, from the XML representation of that term
## Set up
Have a look on how to set up gradle for gumtreediff in the project you are using
## Structure and implementation
Folder `tree_test` is for implementing this. We use the API from the GumTree tool
Generating a `TreeContext` object (defined in `gumtreediff/tree/TreeContext.java`) from a Java's `String` object in XML format, using the `TreeIoUtils` class defined in `gumtreediff/tree/TreeIoUtils.java`, then obtain a `Tree` object (defined in `gumtreediff/tree/Tree.java`)
```
String xml = ".....";

# This line get the TreeContext object from xml content
TreeContext ctxt = TreeIoUtils.fromXml().generateFrom().string(xml);

# This line get the actual Tree object from a TreeContext object, that can be further manipulated for tree diffing
Tree t = ctxt.getRoot();
```