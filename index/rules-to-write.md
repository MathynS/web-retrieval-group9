# Rules to deal with non-informative text
To deal with text that provides not information at all we should apply the following rules<br\>

* Delete tokens composed of several mathematical symbols like for example, `)w(S)`, `{~k}`, or `r------l...-`
* Delete tokens that contain no alphanumerical symbols
* Remove links and email accounts
* Strip the following characters `[,],(,),',?,!,&,|,` from the start and the end of a sentence.
* Replace consecutive and repeated symbols for one instance of it for the following symbols `., ',', -, +,_, =, :, ;, ?, ~, !, *, <, >`
* Split tokens that contain the symbols `-,=,?` in between

<br\>Some interesting tokens that appear in the top 1000 most frequent tokens for the whole collection of papers are: `'\x01', '?)', ';', '[9]', '\x10', '[0,', '(8)', and '2005.'`<br\>
Some interesting tokens that appear in the top 1000 least frequent tokens for the whole collection of papers are: `'}i?I?', "$$'", 'MSR-TR-2006-61', 'http://arxiv.org/abs/', 'g(l:t-l)=', '/:2\x15>\x0f', 'R\x05:\x07\x1a\x0e', 's--+Yxlsx', '........'`<\br>

When looking at the top 1000 least frequent tokens we observe rare examples. To test the effect of our cleaner we can observe the results of the top 1000 most frequent tokens and the top 1000 least frequent tokens.

# Files that don't contain references
* 62-cycles-a-simulation-tool-for-studying-cyclic-neural-networks.pdf
* 6597-optimal-binary-classifier-aggregation-for-general-losses.pdf
* 68-schema-for-motor-control-utilizing-a-network-model-of-the-cerebellum.pdf
* 76-a-dynamical-approach-to-temporal-pattern-processing.pdf
* 6524
* 167
* 170 (content and reference don't have an explicit boundary)
* 173 (just a portion of the paper was converted from pdf to text)
* 198 (just a portion of the paper was converted from pdf to text)
* 218 (content does not contain references)
* 219 (content and reference don't have an explicit boundary)
* 361 (content and references are mixed almost at the end of the document)
* 405 (just a portion of the paper was converted from pdf to text)
* 558 (all the text appears to have issues with the encoding)
* 591 (the pdf was poorly converted to text. There is an explicit references section but it is not worth trying to find it automatically)
* 644 (all the text appears to have issues with the encoding)
* 709 (doesn't contain a reference section)
* 734 (doesn't contain a reference section)
* 760 (content and reference don't have an explicit boundary)
* 795 (reference section contained but it doesn't make sense to detect it automatically)
* 797 (just a portion of the paper was converted from pdf to text)
* 799 (just a portion of the paper was converted from pdf to text)
* 807 (just a portion of the paper was converted from pdf to text)
* 870 (just a portion of the paper was converted from pdf to text)
* 873 (the content appears to have issues with the encoding)
* 905 (the content appears to have issues with the encoding)
* 940 (the content appears to have issues with the encoding)
* 984 (just a portion of the paper was converted from pdf to text)
* 992 (just a portion of the paper was converted from pdf to text)
* 1085 (the content appears to have issues with the encoding)
* 1090 (the content appears to have issues with the encoding)
* 1142 (no reference section)
* 1148 (encoding issues)
* 1150 (incomplete paper)
* 1174 (encoding issues)
* 1289 (no reference section)
* 1294 (imcomplete paper)
* 1501 (content and references not explicitly separated)
* 1533 (incomplete paper)
* 1612 (no references)
* 1616 (encoding issues)
* 1617 (content and references not explictly separated)
