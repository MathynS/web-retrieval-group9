# Rules to deal with non-informative text
To deal with text that provides not information at all we should apply the following rules<br\>

* Delete tokens composed of several mathematical symbols like for example, `)w(S)`, `{~k}`, or `r------l...-`
* Delete tokens that contain no alphanumerical symbols
* Remove links and email accounts
* Strip the following characters `[,],(,),',?,!,&,|,` from the start and the end of a sentence.
* Replace consecutive and repeated symbols for one instance of it for the following symbols `., ',', -, +,_, =, :, ;, ?, ~, !, *, <, >`
* Split tokens that contain the symbols `-,=,?` in between

<br\>Some interesting tokens that appear in the top 1000 most frequent tokens for the whole collection of papers are: `'\x01', '?)', ';', '[9]', '\x10', '[0,', '(8)', and '2005.'`<br\>
Some interesting tokens that appear in the top 1000 least frequent tokens for the whole collection of papers are: `'}i?I?', "$$'", 'MSR-TR-2006-61', 'http://arxiv.org/abs/', 'g(l:t-l)=', '/:2\x15>\x0f', 'R\x05:\x07\x1a\x0e', 's--+Yxlsx', '........'`<br\>

When looking at the top 1000 least frequent tokens we observe rare examples. To test the effect of our cleaner we can observe the results of the top 1000 most frequent tokens and the top 1000 least frequent tokens.

# Issues with eference section
The following are some of the papers that have issues with the references section

## No explicit separation between content and references
* 76 (Content and references separation does not exist)
* 170 (content and reference don't have an explicit boundary)
* 219 (content and reference don't have an explicit boundary)
* 361 (content and references are mixed almost at the end of the document)
* 760 (content and reference don't have an explicit boundary)
* 1501 (content and references not explicitly separated)
* 1617 (content and references not explictly separated)
* 4172 (content and reference not explicitly separated)
* 2410 (content and references not explicitly separated)

## Reference section poorly defined
* 591 (the pdf was poorly converted to text. There is an explicit references section but it is not worth trying to find it automatically)
* 795 (reference section contained but it doesn't make sense to detect it automatically)
* 2040 (references section defined as 'Literature cited')
* 2047 (references section defined as 'Ref erences')
* 2283 (references section defined as 'Refel~ences')
* 2329 (references section defined as 'Refe ren ces')
* 2946 (references section defined as 'R e f e r e n c e s')
* 3443 (references section defined as 'R e f e r e n c e s')
* 3547 (references section defined as 'R e f e r e n c e s')
* 3651 (references section defined as 'R e f e re n c e s')
* 3727 (references section defined as 'R e fer e nces')
* 3858 (references section defined as 'R e f e re n c e s')
* 3979 (references section defined as 'R e f e re n c e s')
* 3989 (references section defined as 'R e f e re n c e s')
* 4016 (references section defined as 'R ef erence s')
* 4694 (references section defined as 'R e f e re n c e s')
* 5948 (references section defined as 'Refrences')
* 68 (Rerences section defined as RJ:I'J:RJ:HCJ:S)

## Encoding issues
* 558 (all the text appears to have issues with the encoding)
* 644 (all the text appears to have issues with the encoding)
* 873 (the content appears to have issues with the encoding)
* 905 (the content appears to have issues with the encoding)
* 940 (the content appears to have issues with the encoding)
* 1085 (the content appears to have issues with the encoding)
* 1090 (the content appears to have issues with the encoding)
* 1148 (encoding issues)
* 1174 (encoding issues)
* 1616 (encoding issues)
* 1866 (encoding issues)
* 5820 (encoding issues)

## Paper is too short
* 167 (paper is too short)
* 6178 (warning: this paper is way too short)
* 6260 (warning: this paper is way too short)
* 797 (just a portion of the paper was converted from pdf to text)
* 799 (just a portion of the paper was converted from pdf to text)
* 807 (just a portion of the paper was converted from pdf to text)
* 870 (just a portion of the paper was converted from pdf to text)
* 984 (just a portion of the paper was converted from pdf to text)
* 992 (just a portion of the paper was converted from pdf to text)
* 2703 (small paper and no references)
* 173 (just a portion of the paper was converted from pdf to text)
* 198 (just a portion of the paper was converted from pdf to text)
* 405 (just a portion of the paper was converted from pdf to text)
* 1150 (incomplete paper)
* 1294 (imcomplete paper)
* 1533 (incomplete paper)
* 1774 (imcomplete paper)
* 1842 (imcomplete paper)
* 6113 (incomplete paper)
* 6114 (incomplete paper)


## No references section
* 218 (content does not contain references)
* 62 (no references section)
* 709 (doesn't contain a reference section)
* 734 (doesn't contain a reference section)
* 1142 (no reference section)
* 1289 (no reference section)
* 1612 (no references)
* 1669 (no references)
* 1778 (no references)
* 1874 (no references)
* 1912 (no references)
* 1937 (no references)
* 3407 (no references)
* 5823 (no references section)
* 6524 (no references section)
* 6597 (no references section)
