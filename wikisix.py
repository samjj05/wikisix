import os, readchar, pywikibot
from collections import deque

site = pywikibot.Site("en", "wikipedia")

def handle_disambiguation_pages(page: pywikibot.Page) -> pywikibot.Page:
    os.system("cls")
    print("The page you have asked for is a disambiguation page.")
    print("Meaning wikipedia is not certain of the page you want to use.")
    print("Press any key to see your page options.")
    readchar.readkey()
    print(f"Please select the page you meant by your title input: {page.title()}\n")
    page_links = list(page.linkedPages())
    page_links = [link for link in page_links if "disambiguation" not in link.title().lower()]
    while True:
        try:
            for i in range(len(page_links)):
                print(f"{i+1}: {page_links[i].title()}")
            selection = int(input("Enter number here: "))
            if selection < 1 or selection > len(page_links):
                show_error_message("Input out of valid range.")
                continue
            selected = page_links[selection-1]
            print(f"You have selected page title '{selected.title()}'. Press enter to continue.")
            readchar.readkey()
            return selected.title()
        except: 
            show_error_message("Non-integer input.")

def turn_into_page(title: str):
    while True:
        page = pywikibot.Page(site, title)
        if not page.exists(): return None
        if page.isRedirectPage(): page = page.getRedirectTarget()
        if not page.isDisambig(): return page.title()
        return handle_disambiguation_pages(page)

def show_error_message(message: str):
    os.system("cls")
    print(message)
    print("Press any key to continue.")
    readchar.readkey()

def input_title(prompt: str):
    while True:
        os.system("cls")
        title = input(prompt).strip()
        if not title: show_error_message("Title cannot be empty.")
        else:
            page = turn_into_page(title)
            return page

def get_backlinks_to_page(title: str):
    page = pywikibot.Page(site, title)
    incoming = []
    for ref in page.getReferences(follow_redirects=False):
        if ref.namespace() != 0:
            continue
        t = ref.title()
        incoming.append(t)
    return incoming
        
def get_links_from_page(title: str):
    page = pywikibot.Page(site, title)
    outgoing = []
    for ol in page.linkedPages():
        if ol.namespace() != 0:
            continue
        t = ol.title()
        outgoing.append(t)
    return outgoing
        
def get_neighbours(flag, current: str):
    if flag == 0: return get_links_from_page(current)
    else: return get_backlinks_to_page(current)

def build_path(parent_from_start, parent_from_target, meeting_point):
    path_start = []
    node = meeting_point
    while node:
        path_start.append(node)
        node = parent_from_start[node]
    path_start.reverse()

    path_target = []
    node = parent_from_target[meeting_point]
    while node:
        path_target.append(node)
        node = parent_from_target[node]

    return path_start + path_target
        
def find_meeting_point(flag: int, q: deque, visited: set, parent: dict, visited2):
    current = q.popleft()
    for neighbour in get_neighbours(flag, current):
        if neighbour in visited:
            continue
        visited.add(neighbour)
        parent[neighbour] = current
        if neighbour in visited2:
            return neighbour
        q.append(neighbour)
    return None  
        
def bidirectional_bfs(start: str, target: str):
    if start == target:
        return [start]

    start_frontier, target_frontier = deque([start]), deque([target])
    parent_from_start, parent_from_target = {start: None}, {target: None}
    start_visited, target_visited = {start}, {target}

    meeting_point = None

    while start_frontier and target_frontier:
        if len(start_frontier) <= len(target_frontier):
            meeting_point = find_meeting_point(0, start_frontier, start_visited, parent_from_start, target_visited)
        else:
            meeting_point = find_meeting_point(1, target_frontier, target_visited, parent_from_target, start_visited)

        if meeting_point:
            break

    if not meeting_point:
        return None

    return build_path(parent_from_start, parent_from_target, meeting_point)


def output_results(start: str, target: str):
    final_path = bidirectional_bfs(start, target)
    print("Results:\n")
    print(f"There were {len(final_path) - 1} necessary clicks to go from '{final_path[0]}' to '{final_path[-1]}'.\n")
    print("Path shown below:\n")
    print(" -> ".join(final_path))

def make_valid_page(prompt: str):
    while True:
        page = input_title(prompt)
        if not page:
            show_error_message("Wikipedia does not recognise that page.")
        else:
            return page
    
def greeting():
    print("Welcome to WikiSix!")
    print("""This tool analyses the shortest path you take by internal links from one Wikipedia page to another,
testing the popular idea that any two pages will have at most six degrees of separation.
\nThis path finder will see how many clicks it takes to get from the start to target page, and will also
output that path to you.""")
    print("\nPlease press any key when you have understood and wish to continue.")
    readchar.readkey()

def main():
    while True:
        os.system("cls")
        print("Press any key to enter the first page.")
        readchar.readkey()
        page1 = make_valid_page("Enter starting page's title: ")
        print("Press any key to enter the second page.")
        readchar.readkey()
        page2 = make_valid_page("Enter target page's title: ")
        os.system("cls")
        output_results(page1, page2)
        end = input("\nPress 1 to exit.")
        if end == 1:
            break
    
if __name__ == "__main__":
    main()