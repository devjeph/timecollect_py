# utils/clean_data.py


def delete_columns(raw_2d_data, column_indexes):
    """
    Deletes specified columns from a 2D list.

    Args:
        raw_2d_data (list of lists): The 2D list to remove columns from.
        column_indexes (list of int): A list of column indices to delete.

    Returns:
        list of lists: A new 2D list with the specified columns removed.
    """
    result = []

    for row in raw_2d_data:
        new_row = []
        for i, value in enumerate(row):
            if i not in column_indexes:
                new_row.append(value)
        result.append(new_row)

    return result


if __name__ == "__main__":
    data = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [10, 11, 12, 13, 14, 15, 16, 17, 18, 19]]
    columns = [3, 4, 5]
    print(delete_columns(data, columns))
