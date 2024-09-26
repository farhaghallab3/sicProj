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

