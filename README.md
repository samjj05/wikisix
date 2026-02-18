# wikisix
This tool finds the shortest path between two Wikipedia articles, showcases said path, and outputs the number of clicks 

## Future features
 - This system is terminal-based. When I go deeper into web development, I feel this tool will be much more useful as a web application.
 - Caching could be implemented, so that a page and its neighbours are stored. During the search, this could be pulled from the database, resulting in a much faster search. This could be done using SQLite.
 - I could involve more search metrics, which would be better for analysis. If a cache is delivered, I could output cache hits. A 'time taken' metric could be an easy metric to put in too. Additionally, it could be useful for a 'nodes visited' metric.

## Time considerations when using the tool
The direction from the starting page will explore its outgoing links, while the direction from the target page will explore its backlinks. Since the outgoing and especially incoming links for a page such as 'United Kingdom' will be massive, the search may take longer time to work. When using this tool, please be mindful of this. This can definitely be improved later on through features such as caching, but for now, it is a trade-off for a pretty cool working system.

## How the search works
The search is done through a bi-directional breadth-first search, which allowed me to treat the collection of Wikipedia articles like an unweighted graph. The primary reason why I chose this compared to an ordinary BFS is that, since Wikipedia is so immensely dense, using the latter choice could result in some searches taking minutes at a time.
For a normal BFS, the graph grows at b^d (branching factor^solution depth). However, for a bi-directional BFS, the graph grows at b^d/2. For example, if a page links to 100 Wikipedia articles, and the solution is 4 clicks away, 100^4 (100,000,000) pages will be explored in the search. For the bi-directional approach, 100^2 (10,000) pages will be explored. This saves an incredible amount of time.
In the searching algorithm, the shortest frontier queue is used first. This is also a time-saving feature, as it ensures the most time-efficient approach is taken each iteration. Since the target page examines its backlinks, a page like 'Poland' will have numerous backlinks compared to the outgoing links from a page such as 'Pet door'.

![Waiting for the search to complete](images/waiting)
![Search results for 'The Mercury (South Africa)' to '4 Vesta'](images/results)

## How redirect pages are handled
Redirect pages are handled instantly at the point of input. Pywikibot has Page methods to allow me to check if it is a redirect page or not. If it is, it is instantly turned into its redirect target. 

## How ambiguous pages are handled
Should a user input a page title such as 'Mercury' (which could mean the planet, element, etc.), the system will allow the user to select the specific page they meant. 

![Inputting 'Mercury' as starting page](images/mercury_input)
![Message output when input lands on an ambiguous page](images/mercury_input_message)
![Selecting a main article page from an ambiguous page](images/mercury_possibilities)




