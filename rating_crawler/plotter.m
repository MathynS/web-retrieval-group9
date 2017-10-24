load author_rating_manual_filtered.csv
author_rating_manual = author_rating_manual_filtered
figure; 
plot(author_rating_manual(:, 1))
hold on; 
plot(author_rating_manual(:, 2))
hold on; 
plot(author_rating_manual(:, 3))
hold on; 
plot(author_rating_manual(:, 4))
hold on; 
plot(author_rating_manual(:, 5)*500000)
title('Authors index comparison') 
legend('h-index', 'h-index 5 years', 'i10-index', 'i10-index 5 years', 'PageRank*5e5')