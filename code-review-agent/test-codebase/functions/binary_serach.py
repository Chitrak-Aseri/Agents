def binary_search(arr, target):
    """Perform binary search on a sorted array to find the target value.

    Args:
        arr: A sorted list of elements to search through.
        target: The value to search for in the array.

    Returns:
        int: The index of the target if found, otherwise -1.
    """
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = left + (right - left) // 2  # Prevents potential overflow vs. (left + right)//2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1