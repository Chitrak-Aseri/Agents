def merge_sort(arr):
    """Sorts an array using the merge sort algorithm.
    
    Args:
        arr: List of elements to be sorted.
        
    Returns:
        List: A new list containing all elements from arr in sorted order.
    """
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    return merge(left, right)

def merge(left, right):
    """Merges two sorted lists into one sorted list.
    
    Args:
        left: First sorted list.
        right: Second sorted list.
        
    Returns:
        List: A new list containing all elements from left and right in sorted order.
    """
    result = []
    while left and right:
        if left[0] < right[0]:
            result.append(left.pop(0))
        else:
            result.append(right.pop(0))
    
    # Add remaining elements from whichever list isn't empty
    result.extend(left or right)
    return result