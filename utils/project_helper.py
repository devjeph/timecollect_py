# project_helper.py


def project_dict(data):
    """
    Converts raw project data into a list of dictionaries, each representing a project.

    Args:
        data (list): A list containing three sublists: project codes, project names, and project clients.

    Returns:
        list: A list of dictionaries, where each dictionary represents a project with keys
              "Project Code", "Project Name", and "Project Client".
    """
    project_datasets = []
    for project in data:
        project_datasets.append(
            {
                "Project Code": project[0],
                "Project Name": project[1],
                "Project Client": project[2],
            }
        )

    return project_datasets


def get_client(project_code, project_data):
    """
    Retrieves the client associated with a given project code from a list of project dictionaries.

    Args:
        project_code (str): The code of the project to search for.
        project_datasets (list): A list of project dictionary

    Returns:
        str: The client of the project if found, otherwise None.
    """
    project_datasets = project_dict(project_data)
    for index, project in enumerate(
        project_datasets
    ):  # Iterate directly through the dictionaries

        if project_code == project["Project Code"]:
            return project_datasets[index]["Project Client"]

    return "YTP"
