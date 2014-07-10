/* Create the document similarity matrix */
select a.docid, b.docid, sum(a.count * b.count) as similarity
from frequency_search a, frequency_search b
where a.term = b.term and a.docid < b.docid 
    and a.docid = '10080_txt_crude' and b.docid = '17035_txt_earn' /* Shortening the query specifically for the assignment */
group by a.docid, b.docid ;

/* Run the document search query
 - the docid 'q' contains all search terms
 - the query is a subset of the similarity matrix above
 */
select b.docid, sum(a.count * b.count) as similarity 
from frequency_search a, frequency_search b
where a.term = b.term and a.docid = 'q'
group by b.docid ;

