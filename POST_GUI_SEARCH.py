#Global search function

def binary_search(data, target, key, ascending=True):
    left = 0
    right = len(data) - 1

    while left <= right:
        mid = (left + right) // 2
        mid_value = data[mid][key]

        if isinstance(mid_value, str) and isinstance(target, str):
            mid_value = mid_value.lower()
            target = target.lower()

        if mid_value == target:
            return mid
        elif (mid_value < target and ascending) or (mid_value > target and not ascending):
            left = mid + 1
        else:
            right = mid - 1

    return -1  # Target msh mwgood


'''
gwa class user

def search_user_by_name(users, target_name):
    index = binary_search(users, target_name, key='name', ascending=True)
    if index != -1:
        return users[index]
    return None


'''


'''class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        return None

    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        return None

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)
'''


'''class NavigationBar:
    def __init__(self):
        self.back_stack = Stack()
        self.forward_stack = Stack()
         self.current_page = None

    def navigate_to(self, new_page):
        if self.current_page:
            self.back_stack.push(self.current_page)
        self.current_page = new_page
        self.forward_stack = Stack()  # Clear forward stack when navigating to a new page

    def go_back(self):
        if self.back_stack.size() > 1:
            self.forward_stack.push(self.current_page)
            self.current_page = self.back_stack.pop()
            return self.current_page
        return None

    def go_forward(self):
        if not self.forward_stack.is_empty():
            self.back_stack.push(self.current_page)
            self.current_page = self.forward_stack.pop()
            return self.current_page
        return None

    def get_current_page(self):
        return self.current_page
'''


# sorting part
def sorting_quick_sort(items, key='date', ascending=True):
    if len(items) < 2:
        return items

    pivot = items[0]
    start = []
    end = []

    for item in items[1:]:
        if ascending:
            if item[key] <= pivot[key]:
                start.append(item)
            else:
                end.append(item)
        else:
            if item[key] >= pivot[key]:
                start.append(item)
            else:
                end.append(item)

    return sorting_quick_sort(start, key, ascending) + [pivot] + sorting_quick_sort(end, key, ascending)
def sort_posts(posts, ascending=True):
    sorted_posts = sorting_quick_sort(posts, key='date', ascending=ascending)
    display_items(sorted_posts)


def sort_comments_by_likes(comments, ascending=True):
    sorted_comments = sorting_quick_sort(comments, key='likes', ascending=ascending)
    display_items(sorted_comments)





